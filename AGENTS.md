# Local Codex setup

This checkout uses the connected `robinhood-trading` MCP server in Codex.
Read `risk_rules.json` fresh on every run. Follow `PHASE_A_TASK.md` for
screening and `PHASE_B_TASK.md` for risk checks and logging.

## Local execution

- Initial deployment should use `dry_run`. Scheduling does not authorize
  live trading. Never change execution mode or risk thresholds during a run.
- The configured account is the only account for portfolio management.
  `wash_sale_avoidance.linked_accounts` are additional read-only inputs for
  the wash-sale check, not additional accounts to trade.
- The watchlist contains mixed assets. Use only items whose `object_type`
  is `instrument`; this strategy is for equities. Log skipped non-equities.
- Use actual dates and times in `America/Chicago` from the system clock.
  Normal cadence is weekdays 03:00 America/Los_Angeles for A, before the
  opening bell, and 08:35 America/Chicago (06:35 Pacific) for B. Skip
  exchange holidays and wait until five minutes after the actual open for B.
- Phase A has no order permission, including order previews and cancellations.
  Phase B may preview equity orders in dry-run mode, but must never place,
  replace, cancel, or exercise orders while in that mode.
- Preserve the task specs' risk math, logging formats, idempotency and minimum
  dry-run day count. Do not invent proposals or completed cycles during setup.
- Save state in this checkout. The cloud templates' automatic git push is
  not configured here: do not push, pull/rebase or publish account data.
  After an authorized manual or scheduled phase run, local commits of that phase's
  generated artifacts are permitted to preserve the thesis history required
  by Phase A. Stage only those artifacts, never `git add .` or account config.
- Keep `trade_log.jsonl` append-only; do not replace it with template records.
- A local Orca deployment uses two weekday automations with fresh Codex
  sessions in the existing checkout: Phase A at 03:00 Pacific and Phase B at
  06:35 Pacific. Do not create duplicate schedules. They are dry-run only.
- Scheduled runs require `scripts/schedule_precheck.py` to reserve the shared
  scheduler lock before launch. Read `logs/scheduler/active/owner.json` and
  verify its phase and current Central date before doing phase work. Release
  the lock with `.venv-scheduler/bin/python scripts/schedule_precheck.py A --finish`
  (or B) in final cleanup, even if phase work fails. Never delete a different
  run's lock. If an agent crashes, a retained lock deliberately blocks later
  runs until inspected; do not automatically expire it or retry the same date.

## Before running

Verify `get_accounts` still permits this agent to access the configured
account. Resolve the configured watchlist by name and verify the saved scan
exists. If required account or market data is unavailable, report the exact
failure and halt affected entries, as specified in Phase B.

The full account identifiers in `risk_rules.json` are local personal data.
Do not commit or push this file with its populated identifiers.
