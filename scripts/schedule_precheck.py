#!/usr/bin/env python3
"""Gate local dry-run automations by market session, time and exclusive claim."""

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import exchange_calendars as xcals


ROOT = Path(__file__).resolve().parents[1]
CENTRAL = ZoneInfo("America/Chicago")
PACIFIC = ZoneInfo("America/Los_Angeles")


def eligibility(phase, now, rules, calendar):
    if rules["execution"]["mode"] != "dry_run":
        return False, "scheduled execution is restricted to dry_run"
    local = now.astimezone(CENTRAL)
    day = local.date().isoformat()
    if not calendar.is_session(day):
        return False, "not an XNYS trading session"
    market_open = calendar.session_open(day).to_pydatetime()
    market_close = calendar.session_close(day).to_pydatetime()
    if phase == "A":
        target = now.astimezone(PACIFIC).replace(
            hour=3, minute=0, second=0, microsecond=0
        )
    else:
        target = market_open + timedelta(minutes=5)
    if not target <= now <= target + timedelta(minutes=15):
        return False, "outside the phase's 15-minute start window"
    if phase == "A" and now >= market_open:
        return False, "Phase A must finish its start window before market open"
    if phase == "B" and now >= market_close:
        return False, "market is closed"
    return True, "eligible"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["A", "B"])
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--finish", action="store_true")
    args = parser.parse_args()
    state = ROOT / "logs" / "scheduler"
    lock = state / "active"
    if args.finish:
        owner = json.loads((lock / "owner.json").read_text())
        if owner["phase"] != args.phase:
            raise RuntimeError("the active lock belongs to the other phase")
        owner["finished_at"] = datetime.now(timezone.utc).isoformat()
        (state / f'{owner["date"]}-{args.phase}.json').write_text(
            json.dumps(owner) + "\n")
        (lock / "owner.json").unlink()
        lock.rmdir()
        print("Released scheduler lock; daily claim retained.")
        return 0

    now = datetime.now(timezone.utc)
    rules = json.loads((ROOT / "risk_rules.json").read_text())
    calendar = xcals.get_calendar("XNYS")
    allowed, reason = eligibility(args.phase, now, rules, calendar)
    if not allowed:
        print(f"SKIP: {reason}")
        return 1
    day = now.astimezone(CENTRAL).date().isoformat()
    claim = state / f"{day}-{args.phase}.json"
    if lock.exists() or claim.exists():
        print("SKIP: an active run or an existing daily claim was found")
        return 1
    if args.check_only:
        print("Eligible; no claim created.")
        return 0
    state.mkdir(parents=True, exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError:
        print("SKIP: another phase acquired the scheduler lock")
        return 1
    owner = {"phase": args.phase, "date": day, "started_at": now.isoformat()}
    # Leave evidence and fail closed if a launch or agent run crashes.
    (lock / "owner.json").write_text(json.dumps(owner) + "\n")
    try:
        with claim.open("x") as stream:
            stream.write(json.dumps(owner) + "\n")
    except FileExistsError:
        (lock / "owner.json").unlink()
        lock.rmdir()
        print("SKIP: this phase already has a daily claim")
        return 1
    print(json.dumps(owner))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
