Work only in the configured checkout. Verify its absolute working directory before reading or writing state.

Run the authorized local weekday Phase A dry-run automation in this checkout.
The standing time is 03:00 America/Los_Angeles on NYSE trading days. At this
time the regular session has not opened. Use the latest completed official
regular-session close as the price anchor, as Phase A specifies; do not use
pre-market or overnight trades as the thesis price. Fetch fundamentals and
historicals fresh and record the close date.

Read AGENTS.md, risk_rules.json and PHASE_A_TASK.md fresh. Use the connected
Robinhood MCP and follow Phase A Steps 1–3 exactly. Do not use any order,
order-preview, cancellation or other account-changing tool. Do not modify
risk_rules.json. No delegation or sub-agents are needed.

Before phase work, read logs/scheduler/active/owner.json. It must name phase A
and today's actual America/Chicago date; otherwise stop without changing the
lock. Also require execution.mode to still be dry_run. Determine the actual
date, weekday and time via the system clock, and use the spec's date/time
formats. If required MCP data or web/news research cannot be obtained, report
the failure; do not invent data or reuse an older run's data as current.

The mixed watchlist supplies only object_type=instrument items. Overwrite
pending_proposals.jsonl with this run's records. Leave trade_log.jsonl alone.
Keep every risk and screening threshold as configured. Report empty scan
results normally; do not relax filters. Existing holdings are always included
as prescribed by the spec.

Use local persistence, overriding the README cloud template's publishing
steps. When phase output is complete, stage only pending_proposals.jsonl and
commit locally so the next run can inspect prior theses. Do not include
account configuration, do not push, and do not pull/rebase. Report commit
failure without discarding output. Never reset, stash or force-push.

Finally, even on an error, release this run's scheduler lock using:
.venv-scheduler/bin/python scripts/schedule_precheck.py A --finish
Only do this if you verified the lock belongs to this phase and date.
End with a concise Chinese summary of screening, proposals, errors and the
local commit result. This schedule never authorizes real trades.
