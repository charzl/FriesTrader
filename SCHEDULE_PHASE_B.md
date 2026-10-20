Work only in the configured checkout. Verify its absolute working directory before reading or writing state.

Run the authorized local weekday Phase B dry-run automation in this checkout.

Read AGENTS.md, risk_rules.json and PHASE_B_TASK.md fresh. Follow Phase B
Steps 0 and 4–9 with the connected Robinhood MCP. This automation is dry-run
only, regardless of any live-trading language in the generic task spec. Never
place, replace, cancel or exercise orders, and never modify risk_rules.json.
Equity order previews are permitted. No delegation or sub-agents are needed.

Before phase work, read logs/scheduler/active/owner.json. It must name phase B
and today's actual America/Chicago date; otherwise stop without changing the
lock. Require execution.mode to still be dry_run. Determine the actual date,
weekday and time via the system clock and use the spec's logging formats.
Read proposals and the append-only trade log fresh. Verify account access.
Do not synthesize proposals or fabricate required account, P&L or price data.
Honor the task spec's response to missing or empty proposals.

Use the deterministic Python risk scripts exactly as prescribed, with fresh
data and unchanged thresholds. Honor per-proposal idempotency, sell-before-buy
processing, all entry guards and loss limits. The other linked accounts are
read-only wash-sale inputs. Preserve the append-only trade log; write the
daily recap and the spec's cycle_summary. Count dry-run days as specified,
never manufacturing completed cycles. Do not call real execution tools even
if ten dry-run dates have accumulated.

Use local persistence, overriding the task spec's cloud publishing steps.
Stage only trade_log.jsonl and trade_log_recent.md and commit locally when
output is complete. Do not include account configuration, do not push, and
do not pull/rebase. Report commit failure without discarding output. Never
reset, stash or force-push.

Finally, even on an error, release this run's scheduler lock using:
.venv-scheduler/bin/python scripts/schedule_precheck.py B --finish
Only do this if you verified the lock belongs to this phase and date.
End with a concise Chinese summary of checks, simulated orders, errors and
the local commit result, clearly stating that no real orders were placed.
