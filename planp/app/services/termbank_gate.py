"""termbank is reachable ONLY through plan.pdhc (operator rule, 2026-11-20/21).

termbank listens on 127.0.0.1 with no vhost, so every path to it runs through
plan. Plan's termbank-backed lookups are for the PLATFORM, not the internet.
Each such path calls `refusal()` first:

  * a logged-in plan session (any role) passes -- plan's own pages;
  * a valid service key of any other module passes -- "all other modules
    should be able to reach the terms in the plan module for lookup";
  * an invalid key gets 403, and anyone else (anonymous, crawlers) 401.

That is exactly `requires_role('read_only')`. Plan's LOCAL CodeSystem lookups
never reach termbank and are not gated here.
"""
from __future__ import annotations


def refusal():
    """None when this request may reach termbank, else a Flask response."""
    from app.api.auth import requires_role
    return requires_role('read_only')(lambda: None)()
