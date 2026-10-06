"""VPP Texas public MCP server.

A read-only guide to the company and its offer for people, crawlers and LLMs,
and the reply guide for anyone answering comments on the company's behalf.

Run locally:   fastmcp run server.py:mcp
Run over HTTP: fastmcp run server.py:mcp --transport http --port 8000
"""

import re
from typing import Literal

from fastmcp import FastMCP
from starlette.responses import PlainTextResponse

import knowledge as k

Channel = Literal["public_comment", "dm", "sms"]

mcp = FastMCP(
    name="VPP Texas",
    instructions=(
        "The official guide to VPP Texas: who we are, what the offer is, and how to "
        "reply to comments about it. Rules for any model using this server: "
        "1) State only what these tools return. If a claim about the offer isn't in "
        "the approved facts, it isn't approved, so say you don't know and point to an "
        "engineer call. Never infer, round or restate a number more helpfully. "
        "2) Never give a savings figure, a blended rate, a competitor's numbers, a "
        "buyout or exit cost, or legal, tax or credit advice. "
        "3) Before posting a reply on the company's behalf, run it through check_reply. "
        "A clean result is a floor, not an approval."
    ),
)

READ_ONLY = {"readOnlyHint": True, "openWorldHint": False}


def _public(fact):
    return {key: fact[key] for key in ("id", "topic", "text")} | (
        {"only_if_asked": True} if fact.get("only_if_asked") else {}
    )


def _hits(text, keywords):
    # Whole words only, so "base" doesn't match "based" and "rent" doesn't match "current".
    return sum(1 for kw in keywords if re.search(rf"(?<!\w){re.escape(kw.strip())}(?!\w)", text))


def _booking():
    return {
        "next_step": "A Google Meet with an engineer, about 40 minutes. Nobody visits the house for this call and there's no commitment on it.",
        "bring": "A recent electric bill. The engineer works from it.",
        "where": k.BOOKING_URL,
        "note": "Not every home qualifies, which is why we check first.",
    }


@mcp.tool(annotations=READ_ONLY)
def about_vpp_texas() -> dict:
    """Who VPP Texas is, what the offer is, and how it's paid for. Start here."""
    return {
        "about": k.ABOUT,
        "website": k.WEBSITE,
        "facts_verified": k.CLAIMS_VERIFIED,
        "topics": sorted({f["topic"] for f in k.FACTS if not f.get("only_if_asked")}),
    }


@mcp.tool(annotations=READ_ONLY)
def list_approved_facts(topic: str | None = None) -> dict:
    """Every fact that may be stated about the offer, optionally filtered by topic.

    Topics: price, agreement, equipment, backup, how_it_works, company,
    eligibility, process. Anything not in this list is not approved.
    Facts that are only answered when someone asks (credit) are left out here.
    Use find_approved_answer for those.
    """
    facts = [_public(f) for f in k.FACTS
             if (topic is None or f["topic"] == topic) and not f.get("only_if_asked")]
    return {"facts_verified": k.CLAIMS_VERIFIED, "count": len(facts), "facts": facts}


@mcp.tool(annotations=READ_ONLY)
def find_approved_answer(question: str) -> dict:
    """Look up the approved answer to a question about VPP Texas or its offer.

    Returns the matching approved facts, or a routing instruction when the
    question is one that only an engineer or a person can answer (savings,
    system sizing, buyout, legal, tax, competitors, existing-customer issues).
    If nothing matches, the answer is that it isn't approved to state.
    """
    q = " " + question.lower() + " "
    routes = [
        {"id": r["id"], "say": r["say"], "route_to": r["to"], "why": r["why"]}
        for r in k.ROUTES if _hits(q, r["keywords"])
    ]
    scored = sorted(
        ((_hits(q, f["keywords"]), f) for f in k.FACTS), key=lambda pair: -pair[0]
    )
    facts = [_public(f) for score, f in scored if score > 0][:4]

    if routes:
        status = "route"
        note = "Don't answer this part directly. Use the routing line. Related approved facts are included for context only."
    elif facts:
        status = "approved"
        note = "State these as written. Don't add figures or detail that isn't here."
    else:
        status = "not_approved"
        note = "Nothing approved covers this. Say you don't know and offer the engineer call."
    return {
        "status": status,
        "note": note,
        "routes": routes,
        "facts": facts,
        "booking": _booking(),
        "facts_verified": k.CLAIMS_VERIFIED,
    }


@mcp.tool(annotations=READ_ONLY)
def check_general_fit(
    is_homeowner: bool | None = None,
    can_choose_electricity_provider: bool | None = None,
    has_indoor_space_for_batteries: bool | None = None,
    open_to_roof_solar: bool | None = None,
) -> dict:
    """A general first read on whether the program could fit a home.

    This never says a home qualifies. Only the engineer call and the free site
    survey decide that. Leave a value out if it isn't known.
    """
    gates = [
        (is_homeowner, "You'd need to be the homeowner.", "Are you the homeowner?"),
        (can_choose_electricity_provider,
         "We can only help where you can choose your electricity provider. On an electric co-op or a regulated utility we can't.",
         "Who's your electricity provider? A co-op or regulated utility means we can't help."),
        (has_indoor_space_for_batteries,
         "The batteries have to go indoors, usually a garage. They can't sit outside.",
         "Is there indoor space for the batteries, like a garage?"),
        (open_to_roof_solar,
         "Solar on the roof isn't optional. It's the reason the equipment is free.",
         "Are you open to solar panels on the roof?"),
    ]
    blockers = [why for value, why, _ in gates if value is False]
    unknown = [ask for value, _, ask in gates if value is None]
    if blockers:
        result = "not_a_fit"
        summary = "Based on that, this isn't a fit right now."
    elif unknown:
        result = "need_more"
        summary = "Can't tell yet. Ask these one at a time."
    else:
        result = "worth_a_call"
        summary = "Nothing here rules it out. The engineer call and the free site survey decide whether the home qualifies. Not every home does."
    return {"result": result, "summary": summary, "blockers": blockers, "still_to_ask": unknown,
            "booking": _booking() if result == "worth_a_call" else None}


@mcp.tool(annotations=READ_ONLY)
def how_to_book() -> dict:
    """The next step for someone who wants to move forward."""
    return _booking()


@mcp.tool(annotations=READ_ONLY)
def get_reply_guide(channel: Channel = "public_comment") -> dict:
    """The voice, conduct rules and limits for replying to a comment, DM or SMS."""
    return {
        "channel": channel,
        "voice": k.VOICE,
        "channel_rules": k.CHANNELS[channel],
        "never_say": k.NEVER_SAY,
        "always_escalate": k.ALWAYS_ESCALATE,
        "escalation_acknowledgement": k.ESCALATION_ACK,
        "review": "Every drafted reply should be approved by a person before it posts.",
    }


@mcp.tool(annotations=READ_ONLY)
def list_comment_intents() -> list[dict]:
    """The triage list: every kind of incoming comment and what to do with it.

    Classify a comment into one of these before drafting anything. If you can't
    classify it with confidence, the intent is `unclear` and it goes to a person.
    """
    return [{key: i[key] for key in ("id", "looks_like", "action")} for i in k.INTENTS]


@mcp.tool(annotations=READ_ONLY)
def get_reply_guidance(intent: str, channel: Channel = "public_comment") -> dict:
    """How to handle one comment intent: the action, the approved facts to use, and an example reply.

    `intent` is an id from list_comment_intents.
    """
    match = next((i for i in k.INTENTS if i["id"] == intent), None)
    if match is None:
        return {"error": f"Unknown intent '{intent}'.", "valid": [i["id"] for i in k.INTENTS],
                "fallback": "If it can't be classified, treat it as `unclear` and hand it to a person."}
    facts = [_public(f) for f in k.FACTS if f["id"] in match["claims"]]
    return {
        "intent": match["id"],
        "action": match["action"],
        "guidance": match["guidance"],
        "approved_facts": facts,
        "example_public_reply": match["example"],
        "channel_rules": k.CHANNELS[channel],
        "then": "Run the draft through check_reply before it goes anywhere.",
    }


@mcp.tool(annotations=READ_ONLY)
def check_reply(draft: str, channel: Channel = "public_comment",
                person_asked_about_credit: bool = False) -> dict:
    """Check a drafted reply against the claims that may never be made and the channel limits.

    `blocks` must be fixed before the reply ships. `warnings` need a second look.
    This is keyword matching, so it misses paraphrase: a clean result is a floor,
    not an approval, and a person should still review the reply.
    """
    sentences = re.split(r"(?<=[.!?])\s+", draft)
    negated = re.compile(r"\b(no|not|without)\b|n['’]t\b", re.IGNORECASE)

    blocks = []
    for pattern, message, *rest in k.BLOCKS:
        negatable = bool(rest and rest[0])
        hit = next((s for s in sentences if pattern.search(s)), None)
        if hit and not (negatable and negated.search(hit)):
            blocks.append({"issue": message, "in": hit.strip()})

    for number, unit in re.findall(r"(\d+)\s*(day|week)s?\b", draft, re.IGNORECASE):
        if int(number) * (7 if unit.lower() == "week" else 1) < 45:
            blocks.append({"issue": "Timeline tighter than about 45 days once approved.", "in": f"{number} {unit}s"})

    warnings = []
    for pattern, message in k.WARNINGS:
        if pattern.search(draft):
            if message.startswith("Mentions credit") and person_asked_about_credit:
                continue
            warnings.append(message)
    if re.search(r"\bfree\b", draft, re.IGNORECASE) and not re.search(r"equipment|install|survey", draft, re.IGNORECASE):
        warnings.append("\"Free\" should be tied to the equipment or the survey. The energy is paid for.")

    limit = k.CHANNELS[channel]["max_chars"]
    if limit and len(draft) > limit:
        blocks.append({"issue": f"Too long for {channel}: {len(draft)} characters, limit {limit}.", "in": ""})

    return {
        "ok": not blocks,
        "blocks": blocks,
        "warnings": warnings,
        "length": len(draft),
        "limit": limit,
        "note": "Keyword checks miss paraphrase. A clean result is a floor, not an approval. A person approves the reply.",
    }


@mcp.resource("vpp://about", mime_type="text/plain")
def about_resource() -> str:
    """Who VPP Texas is and how the offer works."""
    return k.ABOUT


@mcp.resource("vpp://facts", mime_type="text/markdown")
def facts_resource() -> str:
    """Every approved fact about the offer, grouped by topic."""
    return _facts_markdown()


@mcp.resource("vpp://never-say", mime_type="text/markdown")
def never_say_resource() -> str:
    """Claims that are never made about the offer, with the approved wording."""
    return "\n".join(f"- Never: {n['never']}\n  Instead: {n['instead']}" for n in k.NEVER_SAY)


@mcp.resource("vpp://reply-guide", mime_type="text/markdown")
def reply_guide_resource() -> str:
    """The voice and conduct rules for replying to comments, DMs and SMS."""
    lines = ["# Replying for VPP Texas", "", k.VOICE["job"], "", f"Register: {k.VOICE['register']}",
             f"Avoid: {k.VOICE['avoid']}", "", "## Moves"]
    lines += [f"- {m}" for m in k.VOICE["moves"]]
    lines += ["", "## Conduct"] + [f"- {c}" for c in k.VOICE["conduct"]]
    for name, channel in k.CHANNELS.items():
        lines += ["", f"## {name}", f"Length: {channel['length']}"] + [f"- {r}" for r in channel["rules"]]
    lines += ["", "## Always hand to a person"] + [f"- {e}" for e in k.ALWAYS_ESCALATE]
    return "\n".join(lines)


@mcp.prompt
def reply_to_comment(comment: str, channel: Channel = "public_comment") -> str:
    """Draft a reply to a comment, DM or text the way VPP Texas would."""
    return (
        f"Draft a reply for VPP Texas to this {channel.replace('_', ' ')}:\n\n{comment}\n\n"
        "Steps: 1) Call list_comment_intents and classify it. If you can't classify it with "
        "confidence, the intent is `unclear`. 2) Call get_reply_guidance for that intent and "
        f"channel '{channel}'. If the action is escalate, hide or no reply, stop and say so. "
        "3) Draft using only the approved facts returned. Answer the actual question first, "
        "match their length, no hype, no absolutes. 4) Call check_reply on the draft and fix "
        "every block. 5) Return the intent, the action, the draft, the fact ids used, and a "
        "note that a person approves it before it posts."
    )


def _facts_markdown():
    lines = ["# VPP Texas: approved facts", f"Last verified {k.CLAIMS_VERIFIED}.", ""]
    facts = [f for f in k.FACTS if not f.get("only_if_asked")]
    for topic in dict.fromkeys(f["topic"] for f in facts):
        lines.append(f"## {topic.replace('_', ' ').capitalize()}")
        lines += [f"- {f['text']}" for f in facts if f["topic"] == topic]
        lines.append("")
    return "\n".join(lines)


@mcp.custom_route("/llms.txt", methods=["GET"])
async def llms_txt(request):
    """Plain-text version of the guide for crawlers and models that don't speak MCP."""
    body = "\n".join([
        "# VPP Texas", "", k.ABOUT, f"Website: {k.WEBSITE}", "",
        _facts_markdown(),
        "## What we don't state",
        "Savings figures, blended rates for a home, competitor pricing, buyout or exit costs, "
        "system sizing for a specific home, and legal, tax or credit advice. Those are worked "
        "out with an engineer from the home's actual electric bill.", "",
        "## Next step", _booking()["next_step"], k.BOOKING_URL, "",
    ])
    return PlainTextResponse(body)


if __name__ == "__main__":
    mcp.run()
