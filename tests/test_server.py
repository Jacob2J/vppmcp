"""Claims regression tests. If one of these fails, something unapproved can reach the public."""

import asyncio
import sys
from pathlib import Path

import pytest
from fastmcp import Client

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import knowledge as k  # noqa: E402
from server import mcp  # noqa: E402


def call(tool, **args):
    async def run():
        async with Client(mcp) as client:
            return (await client.call_tool(tool, args)).data
    return asyncio.run(run())


def test_every_fact_passes_its_own_lint():
    for fact in k.FACTS:
        result = call("check_reply", draft=fact["text"], channel="dm", person_asked_about_credit=True)
        assert result["ok"], (fact["id"], result["blocks"])


def test_every_example_reply_passes_as_a_public_comment():
    for intent in k.INTENTS:
        if not intent["example"]:
            continue
        result = call("check_reply", draft=intent["example"], channel="public_comment")
        assert result["ok"], (intent["id"], result["blocks"])
        assert not result["warnings"], (intent["id"], result["warnings"])


def test_intent_claims_point_at_real_facts():
    ids = {f["id"] for f in k.FACTS}
    for intent in k.INTENTS:
        assert set(intent["claims"]) <= ids, intent["id"]


# Lines that were said on real calls or are the obvious ways to get it wrong.
@pytest.mark.parametrize("draft", [
    "You pay 12 cents a kilowatt hour, all in, which includes delivery and taxes.",
    "It's 12.9 cents all-in, nothing else.",
    "You'll always have power no matter how long the outage is.",
    "The battery lasts two days.",
    "You'll never lose power again.",
    "Most people save $100 a month.",
    "You won't find anything cheaper than what we're doing.",
    "Base Power charges 14.7 cents, we're lower.",
    "Legally, your HOA cannot prevent you from putting solar up.",
    "You can claim the tax credit on it.",
    "It's a government program.",
    "You'll own the batteries at the end.",
    "You can buy out after year five.",
    "You get credit for excess power you send back.",
    "Your provider would be Light Energy.",
    "We can have it installed in 2 weeks.",
    "Install takes about 30 days.",
    "We've helped 500 families.",
    "Great to have you on board, Dave.",
    "It's a 3% increase, which is tops, guaranteed.",
])
def test_unapproved_claims_are_blocked(draft):
    assert not call("check_reply", draft=draft, channel="dm")["ok"]


def test_approved_negations_are_not_blocked():
    for draft in ["It isn't a government program. It's a business.",
                  "There's no separate net-metering credit on this plan.",
                  "You don't own the batteries. We do.",
                  "About 45 days once everything's approved."]:
        assert call("check_reply", draft=draft, channel="dm")["ok"], draft


def test_public_comment_length_limit():
    assert not call("check_reply", draft="word " * 60, channel="public_comment")["ok"]


def test_credit_is_never_volunteered():
    assert "credit" not in call("about_vpp_texas")["about"].lower()
    assert "credit check" not in str(call("list_approved_facts")).lower()
    assert "credit" in str(call("find_approved_answer", question="Is there a credit check?")["facts"]).lower()
    assert call("check_reply", draft="No hard credit check.", channel="dm")["warnings"]
    assert not call("check_reply", draft="No hard credit check.", channel="dm",
                    person_asked_about_credit=True)["warnings"]


@pytest.mark.parametrize("question,route", [
    ("How much will I save a month?", "savings"),
    ("Will this run my AC during an outage?", "system_design"),
    ("What does it cost to buy out the system?", "contract_mechanics"),
    ("Can I get the tax credit?", "legal_tax_finance"),
    ("Base Power quoted me cheaper, what's their rate?", "competitors"),
    ("I signed up in June and nobody called me back", "existing_customer"),
])
def test_unanswerable_questions_route(question, route):
    result = call("find_approved_answer", question=question)
    assert result["status"] == "route"
    assert route in [r["id"] for r in result["routes"]]


@pytest.mark.parametrize("question,fact", [
    ("How much is it?", "production_rate"),
    ("How long does the battery last in an outage?", "backup_runtime"),
    ("Do you have to put panels on my roof?", "solar_required"),
    ("What's the catch?", "the_catch"),
    ("How long is the contract?", "term"),
    ("How long have you been in business?", "company_age"),
])
def test_common_questions_get_the_approved_fact(question, fact):
    result = call("find_approved_answer", question=question)
    assert result["status"] == "approved"
    assert fact in [f["id"] for f in result["facts"]]


def test_price_answer_always_carries_the_grid_piece():
    ids = [f["id"] for f in call("find_approved_answer", question="How much is it?")["facts"]]
    assert "grid_top_up" in ids


def test_unknown_question_is_not_approved():
    assert call("find_approved_answer", question="What colour is the inverter?")["status"] == "not_approved"


def test_fit_never_says_qualified():
    result = call("check_general_fit", is_homeowner=True, can_choose_electricity_provider=True,
                  has_indoor_space_for_batteries=True, open_to_roof_solar=True)
    assert result["result"] == "worth_a_call"
    assert "you qualify" not in result["summary"].lower()
    assert call("check_general_fit", is_homeowner=False)["result"] == "not_a_fit"
    assert call("check_general_fit", is_homeowner=True)["result"] == "need_more"


def test_nothing_internal_or_stale_is_published():
    async def dump():
        async with Client(mcp) as client:
            parts = [str((await client.call_tool("list_approved_facts", {})).data),
                     str((await client.call_tool("get_reply_guide", {})).data)]
            for intent in k.INTENTS:
                parts.append(str((await client.call_tool("get_reply_guidance", {"intent": intent["id"]})).data))
            for resource in await client.list_resources():
                parts.append(str(await client.read_resource(resource.uri)))
            return " ".join(parts).lower()
    text = asyncio.run(dump())
    for banned in ["light energy", "abundance", "12 cents", "40,000", "forty thousand",
                   "11.18", "13.6", "600", "setter", "show rate"]:
        assert banned not in text, banned
