"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import json

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.runtime import dispatch, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        budget = Budget()
        trace = Trace(make_run_id("single", claim_id, seed))

        # This initial tool read is deliberately allowlisted by get_claim_view.
        claim = dispatch(conn, budget, "get_claim_view", {"claim_id": claim_id}, worker=True)
        safe_claim = {key: claim[key] for key in ("found", "claim_id", "order_id") if key in claim}
        trace.add("claim_view", safe_claim)
        if not claim.get("found"):
            trace.add("decision", {"status": "failed", "reason": "unknown_claim"})
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="failed", proposal_amount=0, budget=budget,
                          trace=trace, error_reason="unknown_claim")
        if not claim.get("order_id"):
            complete(budget, seed=seed, purpose="decide", prompt="missing_order_id")
            trace.add("decision", {"status": "needs_info"})
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="needs_info", proposal_amount=0, budget=budget,
                          trace=trace, error_reason="missing_order_id")

        # The agent gets only the safe claim identifiers; it reasons from order
        # and compensation tools, never from the customer's ticket assertions.
        observation = {"claim": {"claim_id": claim_id, "order_id": claim["order_id"],
                                 "principal_id": claim["principal_id"]}}

        order_result: dict = {}

        def decide(seen: dict) -> dict:
            complete(budget, seed=seed, purpose="decide",
                     prompt=json.dumps(seen, sort_keys=True, ensure_ascii=False))
            if "last_tool" not in seen:
                return {"tool": "lookup_order", "args": {
                    "order_id": claim["order_id"], "principal_id": claim["principal_id"]}}
            name, result = seen["last_tool"], seen.get("last_result", {})
            if name == "lookup_order":
                if not result.get("visible"):
                    return {"final": {"status": "escalated", "error_reason": result.get("reason")}}
                order_result.update(result)
                return {"tool": "lookup_refund_history", "args": {
                    "order_id": claim["order_id"], "principal_id": claim["principal_id"]}}
            if name == "lookup_refund_history":
                return {"tool": "compute_compensation", "args": {"order": order_result["order"]}}
            if name == "compute_compensation":
                return {"final": {"status": "quoted", "quote": result}}
            return {"final": {"status": "failed", "error_reason": "unexpected_tool_result"}}

        loop = run_react(conn, budget, observation=observation, decide=decide,
                         max_steps=8, worker=True)
        trace.add("react", {"stopped": loop["stopped"], "final": loop["final"]})
        final = loop["final"]
        if final.get("status") == "escalated":
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="escalated", proposal_amount=0, budget=budget,
                          trace=trace, error_reason=final.get("error_reason"))
        if final.get("status") != "quoted":
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="failed", proposal_amount=0, budget=budget,
                          trace=trace, error_reason=final.get("error_reason", "step_cap"))

        quote = final["quote"]
        proposal = int(quote.get("amount_vnd", 0))
        trace.add("quote", safe_dump(quote))
        if proposal <= 0:
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="denied", proposal_amount=0, budget=budget,
                          trace=trace, error_reason=quote.get("reason"))

        # Host is the sole writer and receives the full quote. crash_at is
        # forwarded for CP3 durability behavior; InjectedCrash must propagate.
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
        trace.add("write_attempt", {"proposal_amount": proposal, "ok": outcome["ok"],
                                    "reason": outcome["reason"]})
        if not outcome["ok"]:
            return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                          status="failed" if outcome["conflict"] else "denied",
                          proposal_amount=proposal, budget=budget, trace=trace,
                          error_reason=outcome["reason"])
        return finish(conn, shape="single", claim_id=claim_id, seed=seed,
                      status="resolved", proposal_amount=proposal, budget=budget,
                      trace=trace)
    finally:
        conn.close()
