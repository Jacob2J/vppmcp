"""The approved public knowledge for VPP Texas.

Everything a client can read through this server lives in this file. It is a
copy of the company's internal approved-claims list, narrowed to what may be
said in public. Nothing here is improvised: if a claim is not in FACTS it is
not approved, and the right answer is to route the question to an engineer.

When the offer changes, update this file in the same pass as the internal
approved-claims list and bump CLAIMS_VERIFIED.
"""

import os
import re

# Date the facts below were last verified against the signed paperwork.
CLAIMS_VERIFIED = "2026-09-08"

WEBSITE = os.environ.get("VPP_WEBSITE", "https://vpptexas.com")
BOOKING_URL = os.environ.get("VPP_BOOKING_URL", WEBSITE)

ABOUT = """\
VPP Texas is a Texas virtual power plant operator. We install a home battery
system paired with roof-mounted solar in Texas homes at no cost to the
homeowner, and the homeowner pays for the energy they use.

How it's paid for: we make our money from the grid, not from the homeowner.
The batteries charge when power is cheap, and at peak we sell that stored
energy back to the grid at a much higher price. That revenue pays for the
equipment. It's a real business, not a government program.

The parts people like least, said first: solar panels go on the roof, it's a
25 year agreement, and you switch retail electricity providers.

Not every home qualifies, which is why we check first. The next step is a
video call of about 40 minutes with an engineer who works from the home's
actual electric bill. There's no commitment on the call.
"""

# Each fact: id, topic, the approved wording, and the phrases that route a
# question to it. `only_if_asked` facts are answered honestly when someone
# asks and are never volunteered.
FACTS = [
    {
        "id": "equipment_cost",
        "topic": "price",
        "text": "The equipment is $0. No down payment, no installation charge, and no monthly equipment or membership fee.",
        "keywords": ["how much", "cost", "price", "free", "upfront", "down payment", "install charge", "monthly fee", "membership"],
    },
    {
        "id": "really_free",
        "topic": "price",
        "text": "The equipment is free. You pay for the energy you use.",
        "keywords": ["really free", "actually free", "is it free", "free"],
    },
    {
        "id": "production_rate",
        "topic": "price",
        "text": "The power your system produces is 12.9 cents per kWh, and that rate can't go up more than 2.9% a year for 25 years.",
        "keywords": ["how much", "rate", "cents", "kwh", "price", "cost", "per kilowatt", "electricity"],
    },
    {
        "id": "grid_top_up",
        "topic": "price",
        "text": "Almost no home produces 100% of what it uses. Power you pull from the grid on top of what your system makes is billed separately by our approved retail electricity provider under its own Electricity Facts Label. So the 12.9 cent rate covers what the system produces. Your engineer runs the exact numbers off your bill.",
        "keywords": ["how much", "rate", "grid", "bill", "two bills", "delivery", "fees", "taxes", "all in", "all-in", "total", "efl", "everything"],
    },
    {
        "id": "rate_cap_scope",
        "topic": "price",
        "text": "The 2.9% cap covers the power your system makes. The grid portion sits on a 12-month fixed plan that gets renewed.",
        "keywords": ["go up", "increase", "escalator", "cap", "2.9", "rate lock", "locked", "raise", "rate protection"],
    },
    {
        "id": "no_net_metering",
        "topic": "price",
        "text": "Excess production is what funds the program. That's how the equipment is free. There's no separate net-metering credit on this plan.",
        "keywords": ["excess", "sell back", "net metering", "net-metering", "credit for", "buyback", "extra power", "overproduce"],
    },
    {
        "id": "term",
        "topic": "agreement",
        "text": "It's a 25 year agreement.",
        "keywords": ["contract", "how long is", "term", "years", "agreement", "commitment", "locked in"],
    },
    {
        "id": "provider_switch",
        "topic": "agreement",
        "text": "You do switch retail electricity providers. That's how the rate works. We partner with an approved retail provider, and your engineer confirms which one for your area.",
        "keywords": ["switch", "provider", "retail", "electric company", "who is the provider", "rep"],
    },
    {
        "id": "exit_fee_covered",
        "topic": "agreement",
        "text": "If you're in a contract with your current provider, we cover their cancellation fee when you switch. No cap.",
        "keywords": ["in a contract", "current provider", "cancellation fee", "early termination", "locked into", "exit fee", "etf"],
    },
    {
        "id": "sale_of_home",
        "topic": "agreement",
        "text": "If you sell the house, the agreement transfers with the home. There's more to it than fits in a short answer, so an engineer walks you through it.",
        "keywords": ["sell the house", "sell my house", "sell my home", "move", "moving", "transfer", "new owner"],
    },
    {
        "id": "equipment",
        "topic": "equipment",
        "text": "A Duracell battery system, typically 45 to 60 kWh, plus roof-mounted solar. Sizing for a specific home is the engineer's job.",
        "keywords": ["battery", "batteries", "how big", "how large", "size", "kwh", "duracell", "brand", "what equipment", "what do i get"],
    },
    {
        "id": "ownership",
        "topic": "equipment",
        "text": "We own, insure, maintain and replace the equipment. You don't own the batteries. You get the use of the system and the rate.",
        "keywords": ["own", "ownership", "insure", "insurance", "maintain", "maintenance", "breaks", "replace", "warranty", "repair"],
    },
    {
        "id": "placement",
        "topic": "equipment",
        "text": "The batteries go indoors, usually in a garage. They can't sit outside. They aren't noisy.",
        "keywords": ["where do", "garage", "outside", "indoors", "noisy", "noise", "loud", "space"],
    },
    {
        "id": "solar_required",
        "topic": "equipment",
        "text": "Yes, solar goes on the roof, and it isn't optional. It's why the equipment is free: the solar generates the energy we sell back to the grid.",
        "keywords": ["solar", "panel", "panels", "roof", "battery only", "without solar", "no solar"],
    },
    {
        "id": "backup_runtime",
        "topic": "backup",
        "text": "The battery runs about 24 to 36 hours on its own, depending on your usage. The solar keeps recharging it.",
        "keywords": ["how long does", "outage", "backup", "last", "blackout", "power goes out", "storm", "hurricane", "freeze", "runtime"],
    },
    {
        "id": "how_we_make_money",
        "topic": "how_it_works",
        "text": "We make our money from the grid, not from you. The batteries charge when power is cheap, and at peak we sell that energy back to the grid at a much higher price. That's what pays for your equipment.",
        "keywords": ["how do you make money", "why is it free", "how is it free", "how does it work", "virtual power plant", "vpp", "business model", "who pays"],
    },
    {
        "id": "the_catch",
        "topic": "how_it_works",
        "text": "It's a real business. We make our money selling stored energy to the grid at peak, not from you. And honestly, not every home qualifies, which is why we check first.",
        "keywords": ["catch", "scam", "too good", "legit", "real", "nothing is free", "trust", "fine print"],
    },
    {
        "id": "not_government",
        "topic": "how_it_works",
        "text": "It isn't a government program. It's a business, and the revenue comes from selling stored energy back to the grid.",
        "keywords": ["government", "state program", "subsidy", "funded", "ercot program"],
    },
    {
        "id": "company_age",
        "topic": "company",
        "text": "Two years doing this in Texas. The virtual power plant model is about ten years old.",
        "keywords": ["how long have you", "in business", "how old", "established", "new company", "years in business"],
    },
    {
        "id": "contracting_entity",
        "topic": "company",
        "text": "The agreement is with a separate finance and contracting entity. VPP Texas is the customer-facing side.",
        "keywords": ["who is the contract with", "finance company", "contracting", "solrite", "solwright", "solarite"],
    },
    {
        "id": "service_area",
        "topic": "eligibility",
        "text": "Texas only, in the areas where you can choose your electricity provider. If you're served by an electric co-op or a regulated utility, we can't help.",
        "keywords": ["where", "area", "city", "service", "co-op", "coop", "cooperative", "utility", "texas", "available in", "do you serve"],
    },
    {
        "id": "who_qualifies",
        "topic": "eligibility",
        "text": "In general it fits a homeowner who can choose their electricity provider, has indoor space for the batteries (usually a garage), and is open to solar on the roof. Not every home qualifies, which is why we check first.",
        "keywords": ["qualify", "qualifies", "eligible", "eligibility", "requirements", "rent", "renter", "homeowner", "would my house"],
    },
    {
        "id": "site_survey",
        "topic": "process",
        "text": "The site survey is free. If the survey comes back as a red light, it costs you nothing.",
        "keywords": ["site survey", "survey", "doesn't qualify", "not qualify", "red light", "inspection"],
    },
    {
        "id": "engineer_call",
        "topic": "process",
        "text": "The first step is a Google Meet with an engineer, about 40 minutes. Nobody comes to your house for that call, and there's no commitment on the call.",
        "keywords": ["call", "meeting", "appointment", "come to my house", "visit", "sign up", "next step", "get started", "how do i", "obligation"],
    },
    {
        "id": "process",
        "topic": "process",
        "text": "The steps are: engineer call, site survey, design and permits, install, utility approval.",
        "keywords": ["process", "steps", "what happens", "permits", "permit"],
    },
    {
        "id": "install_timeline",
        "topic": "process",
        "text": "About 45 days once everything's approved. Your engineer gives you the real timeline for your home.",
        "keywords": ["how long until", "install", "installation", "timeline", "how soon", "when would", "how fast"],
    },
    {
        "id": "hoa",
        "topic": "process",
        "text": "We deal with HOAs constantly and handle that process for you.",
        "keywords": ["hoa", "homeowners association", "homeowner association"],
    },
    {
        "id": "credit",
        "topic": "credit",
        "text": "No hard credit check. What matters is a history of paying bills on time.",
        "keywords": ["credit"],
        "only_if_asked": True,
    },
]

# Questions that are never answered from this server. Each has the approved
# line to use instead and where the question goes.
ROUTES = [
    {
        "id": "savings",
        "say": "That's exactly what the engineer works out from your actual bill.",
        "to": "engineer",
        "why": "A savings figure can't be known without the bill and the engineer's design.",
        "keywords": ["save", "saves", "saving", "savings", "lower my bill", "cut my bill", "cheaper than", "how much less", "blended", "what would my bill"],
    },
    {
        "id": "system_design",
        "say": "Honestly that's an engineer question. Yours would work it out from your actual bill and your home.",
        "to": "engineer",
        "why": "Panel count, battery sizing, AC load and anything about a specific roof are design questions.",
        "keywords": ["how many panels", "panel count", "how many batteries", "run my ac", "run the ac", "air condition", "whole house", "pool", "ev charger", "roof damage", "leak", "leaks", "old roof", "new roof", "replace my roof", "tree", "trees", "shade"],
    },
    {
        "id": "contract_mechanics",
        "say": "Let me get somebody on this who can actually answer it properly.",
        "to": "human",
        "why": "Buyout, exit, removal and transfer details are per-home contract terms and are never estimated.",
        "keywords": ["buyout", "buy out", "buy it out", "cancel", "get out of", "remove the system", "removal", "exit", "terminate", "buyer doesn't want", "end of the term", "after 25 years", "lien"],
    },
    {
        "id": "legal_tax_finance",
        "say": "Let me get somebody on this who can actually answer it properly.",
        "to": "human",
        "why": "We don't give legal, tax or credit advice, and we don't describe the finance partner's structure.",
        "keywords": ["tax", "tax credit", "itc", "grant", "rebate", "legal", "legally", "law", "lawsuit", "attorney", "credit score", "finance partner", "investor"],
    },
    {
        "id": "competitors",
        "say": "I can't speak to their numbers. Here's ours.",
        "to": "answer_with_our_facts_only",
        "why": "We never state another company's rate, fee or terms.",
        "keywords": ["base power", "base", "tesla", "powerwall", "generac", "sunrun", "competitor", "other company", "compare", "versus", " vs "],
    },
    {
        "id": "existing_customer",
        "say": "That's not okay and I'm sorry. Let me get a person on this.",
        "to": "human_priority",
        "why": "Anything from an existing customer about an install, a delay or not hearing back goes to a person. Acknowledge only.",
        "keywords": ["i signed", "signed up", "still waiting", "nobody called", "no one called", "call me back", "my install", "my system", "my appointment", "customer service", "complaint"],
    },
]

# What never gets said, with the approved replacement.
NEVER_SAY = [
    {"never": "Any promise of unlimited backup, or any absolute about power during an outage.",
     "instead": "About 24 to 36 hours on its own, and the solar keeps recharging it."},
    {"never": "\"The battery lasts two days.\"",
     "instead": "About 24 to 36 hours on its own, depending on your usage."},
    {"never": "\"12.9 cents all in\" or \"nothing else\" or \"includes delivery, fees and taxes.\"",
     "instead": "12.9 cents for what your system produces. Grid top-up is billed by our retail partner."},
    {"never": "A blended or all-in rate figure for a home.",
     "instead": "That depends on the home. Your engineer runs the exact number off your bill."},
    {"never": "\"The 2.9% cap protects you from rate increases,\" unqualified.",
     "instead": "The cap covers the power your system makes. The grid portion sits on a 12-month fixed plan that gets renewed."},
    {"never": "\"You get credit for excess power you send back.\"",
     "instead": "Excess production is what funds the program. There's no separate net-metering credit on this plan."},
    {"never": "Any competitor's rate, fee or terms.",
     "instead": "I can't speak to their numbers. Here's ours."},
    {"never": "Any dollar or percent savings figure.",
     "instead": "That's what the engineer works out from your actual bill."},
    {"never": "Any buyout, exit or removal cost, or any buyout year.",
     "instead": "Route it to a person."},
    {"never": "\"You'll own the batteries.\"",
     "instead": "We own, insure, maintain and replace them. You get the use and the rate."},
    {"never": "The retail provider's name.",
     "instead": "We partner with an approved retail provider. Your engineer confirms which one for your area."},
    {"never": "Anything about HOA law.",
     "instead": "We deal with HOAs constantly and handle that process for you."},
    {"never": "Anything about tax credits, grants, or the finance partner's structure.",
     "instead": "Route it to a person."},
    {"never": "\"It's a government program,\" or anything implying government funding.",
     "instead": "It's a real business. We make our money selling stored energy back to the grid."},
    {"never": "An install date tighter than about 45 days from approval.",
     "instead": "About 45 days once everything's approved."},
    {"never": "Any promise about how often someone will hear from us after signing.",
     "instead": "Say nothing about it. Route it."},
    {"never": "Credit, unless the person asked first.",
     "instead": "If asked: no hard credit check. What matters is a history of paying bills on time."},
    {"never": "\"You won't find anything cheaper,\" or any absolute: always, never, guaranteed.",
     "instead": "State our number and let them compare it to their bill."},
    {"never": "Panel count, battery sizing, whether it runs their AC, or anything about their specific roof.",
     "instead": "That's an engineer question."},
    {"never": "Any customer count, statistic or fact about a specific person.",
     "instead": "Say you can't see that from here and route it."},
]

VOICE = {
    "job": "The reply agent does not sell and does not close. It makes the company sound like one worth taking a call from, then gets out of the way. On a public post the real audience is the people reading silently, not the person who commented.",
    "register": "Plain, calm, a little understated. A Texan explaining something over a fence. Contractions, short common words, real numbers.",
    "avoid": "Superlatives, hype, urgency, stacked exclamation points, corporate warmth, \"we're so excited\", \"amazing\", \"reach out\". Essentially no emoji. No em dashes.",
    "moves": [
        "Answer the actual question first. Give the number, then explain if there's room.",
        "Qualify instead of defending: \"Not every home qualifies, which is why we check first.\"",
        "Say \"I don't know\" plainly: \"That's a question for the engineer, not for me in a comment box.\"",
        "Volunteer the awkward part: panels go on the roof, it's a 25 year agreement, you switch providers.",
        "Never use an absolute: always, never, guaranteed, you won't find cheaper.",
        "When someone is suspicious, explain how we make money. Don't add more benefits.",
        "Match their length, then stop.",
    ],
    "conduct": [
        "Never put anyone's private information in a public reply, and never confirm publicly that a named person is a customer.",
        "One calm, factual reply to a hostile or accusatory public comment. Then stop on that thread for good. No last word.",
        "Never delete or hide criticism. Hide only spam, bots and hate speech.",
        "Never argue or correct someone in public.",
        "Never invent a number, a customer count, a statistic, or a fact about a person's situation.",
        "Existing customer complaints always go to a person. Acknowledge, apologise, promise nothing, move it to DM.",
        "Ask one question per message.",
    ],
    "lines_that_work": [
        "Not every home qualifies, which is why we check first.",
        "There's no commitment on the call.",
    ],
}

CHANNELS = {
    "public_comment": {
        "max_chars": 250,
        "length": "1 to 2 sentences, under 250 characters.",
        "can_book": False,
        "personal_details": False,
        "rules": [
            "No pitch. Short, calm, factual.",
            "If the answer needs personal detail, give one public sentence and invite a DM.",
            "Don't paste a booking link into every reply. Links go in DMs, or in public only when someone asked how to sign up.",
            "One reply per hostile thread, then stop.",
        ],
    },
    "dm": {
        "max_chars": None,
        "length": "2 to 4 sentences.",
        "can_book": True,
        "personal_details": True,
        "rules": [
            "Learn these one at a time, conversationally: are they the homeowner, who their electricity provider is, are they open to solar on the roof, roughly what they pay now.",
            "A co-op or regulated utility means we can't help. Say so kindly and end it.",
            "Once those look fine, hand off to booking. Don't run discovery and don't pitch.",
        ],
    },
    "sms": {
        "max_chars": 320,
        "length": "1 to 3 sentences, under 320 characters.",
        "can_book": True,
        "personal_details": True,
        "rules": [
            "Honor an opt-out at once: STOP, unsubscribe, \"quit texting me\", \"remove me\", or anything that plainly means the same. Confirm once in under ten words and stop. No retention attempt.",
            "Never text outside 8am to 9pm in the recipient's local time.",
            "Never send the first message to someone who hasn't consented. Reply and continue threads only.",
            "No emoji.",
        ],
    },
}

ESCALATION_ACK = "Let me get somebody on this who can actually answer it properly. Sending you a DM."

# The triage taxonomy. `action` is what the reply agent does; `example` is a
# public-comment reply built only from FACTS.
INTENTS = [
    {"id": "price", "looks_like": "how much / what's the cost / is it really free",
     "action": "reply", "claims": ["equipment_cost", "production_rate", "grid_top_up"],
     "guidance": "Answer the question first. Give both pieces of the price, then stop.",
     "example": "Equipment's free, no install charge. You pay 12.9 cents a kilowatt hour for what your system produces. Anything you pull from the grid on top of that is billed by our retail partner."},
    {"id": "skepticism", "looks_like": "what's the catch / nothing is free / scam",
     "action": "reply", "claims": ["how_we_make_money", "the_catch"],
     "guidance": "Mechanism, then the qualifier. No defensiveness, no benefit list. One reply only.",
     "example": "Fair. We make our money selling the stored power back to the grid at peak, not from you. That's the whole model. And not every home qualifies, which is why we check first."},
    {"id": "how_it_works", "looks_like": "what's a virtual power plant / how does this work",
     "action": "reply", "claims": ["how_we_make_money"],
     "guidance": "Short mechanism answer.",
     "example": "The batteries charge when power is cheap, and at peak we sell that stored energy back to the grid. That's what pays for the equipment. You pay for the power you use."},
    {"id": "backup_duration", "looks_like": "how long does it last in an outage",
     "action": "reply", "claims": ["backup_runtime"],
     "guidance": "The range, then the recharge. No absolutes.",
     "example": "About 24 to 36 hours on its own, depending on your usage. The solar keeps recharging it."},
    {"id": "solar_objection", "looks_like": "not putting panels on my roof",
     "action": "reply", "claims": ["solar_required"],
     "guidance": "Acknowledge, give the reason it exists, let them leave. Don't argue.",
     "example": "Understood, and that's the part most people like least. It's also the reason the equipment costs nothing, since the solar is what generates the power we sell back. Not for everybody."},
    {"id": "competitor", "looks_like": "how's this different from another company / they quoted me cheaper",
     "action": "reply", "claims": ["production_rate", "equipment_cost", "solar_required"],
     "guidance": "Claims about us only. Nothing about them, and never their numbers.",
     "example": "Can't speak to their numbers. Ours is 12.9 cents for what the system produces, nothing upfront, no monthly equipment fee, and it's paired with solar so the batteries recharge."},
    {"id": "eligibility_general", "looks_like": "does this work in my city / what about co-ops",
     "action": "reply", "claims": ["service_area", "who_qualifies"],
     "guidance": "Answer the general case, invite a DM for their specifics.",
     "example": "We work in the parts of Texas where you can choose your electricity provider. On a co-op or a regulated utility we can't help. Send us a DM and we'll take a look at your area."},
    {"id": "eligibility_personal", "looks_like": "would my house work / my roof is 20 years old",
     "action": "reply", "claims": [],
     "guidance": "You can't know from a comment. Say so and invite a DM or a call.",
     "example": "Depends on your roof and your bill, which I can't see from here. Send us a DM and we'll take a look."},
    {"id": "ready_to_book", "looks_like": "how do I sign up / who do I call",
     "action": "reply", "claims": ["engineer_call"],
     "guidance": "Give the booking path. A link is fine here because they asked.",
     "example": "It starts with a video call with an engineer, about 40 minutes. There's no commitment on the call. Send us a DM and we'll get you a time."},
    {"id": "technical", "looks_like": "panel count, AC load, roof damage, battery sizing",
     "action": "reply", "claims": [],
     "guidance": "Never answered. Say it's an engineer question and offer the call.",
     "example": "Honestly that depends on your system and your usage, and I'm not going to guess at it in a comment. The engineer works it out from your actual bill. Happy to get you on that call."},
    {"id": "contract_mechanics", "looks_like": "buyout, exit cost, selling the house, transfer",
     "action": "escalate", "claims": [],
     "guidance": "Never auto-answered past the headline terms. Acknowledge and hand to a person.",
     "example": ESCALATION_ACK},
    {"id": "customer_complaint", "looks_like": "install delay, no communication, something broke",
     "action": "escalate_priority", "claims": [],
     "guidance": "Acknowledge like a person. Don't explain, don't defend, promise nothing about timing. Move it out of public and get a person.",
     "example": "That's not okay and I'm sorry. Sending you a DM right now so I can get a person on this."},
    {"id": "legal_tax_credit", "looks_like": "HOA law, tax credits, grants, credit, the finance partner",
     "action": "escalate", "claims": [],
     "guidance": "Never auto-answered. Acknowledge and hand to a person.",
     "example": ESCALATION_ACK},
    {"id": "hostile", "looks_like": "insults, harassment, pile-on",
     "action": "reply_once_then_stop", "claims": [],
     "guidance": "One calm reply at most, then stop on that thread and flag it for a person.",
     "example": ""},
    {"id": "spam", "looks_like": "bots, spam, competitor links",
     "action": "hide", "claims": [],
     "guidance": "Hide it. No reply, no escalation.",
     "example": ""},
    {"id": "business_enquiry", "looks_like": "press, partnership, investor, vendor",
     "action": "escalate", "claims": [],
     "guidance": "No reply. Hand to a person.",
     "example": ""},
    {"id": "recruiting", "looks_like": "are you hiring",
     "action": "reply", "claims": [],
     "guidance": "Point them at the website. Don't describe roles or pay.",
     "example": "Appreciate you asking. Best place to start is our website."},
    {"id": "unclear", "looks_like": "can't classify with confidence",
     "action": "escalate", "claims": [],
     "guidance": "Never pick the closest bucket and hope. Hand to a person.",
     "example": ""},
]

ALWAYS_ESCALATE = [
    "Any existing customer with a complaint.",
    "Anything legal, tax, credit, or about the finance partner.",
    "Contract mechanics past the headline terms: buyout, exit, removal, transfer disputes.",
    "Anyone threatening a lawsuit, a chargeback, a regulator or the news.",
    "Anything mentioning a minor, a medical emergency, or someone in crisis.",
    "Press, partnership, investor or vendor enquiries.",
    "Any message that can't be classified with confidence.",
    "Any thread where one reply has been posted and hostility continued.",
]

# Draft-reply lint. (pattern, message[, negatable]). A hit in BLOCKS means the
# draft can't ship as written. A negatable block is skipped when the sentence
# it sits in negates the claim ("it isn't a government program"). Keyword checks undercount paraphrase, so a clean result is
# a floor and never an approval.
_F = re.IGNORECASE
BLOCKS = [
    (re.compile(r"\ball[\s-]?in\b|\bnothing else\b|includ\w+ (delivery|fees|taxes)", _F),
     "\"All in\" / \"nothing else\": the 12.9 cent rate covers system production only. Grid top-up is a separate bill.", True),
    (re.compile(r"\b12(\.0)?\s?(¢|cents?)", _F),
     "Old rate. Production is 12.9 cents per kWh."),
    (re.compile(r"\b(always|never|guarantee\w*|no matter (how|what))\b", _F),
     "Absolute. Any sentence that can't survive one skeptical follow-up shouldn't be said."),
    (re.compile(r"unlimited|two days|2 days|48 hours|never lose power|whole[- ]home backup forever", _F),
     "Backup claim. Approved: about 24 to 36 hours on its own, and the solar keeps recharging it."),
    (re.compile(r"indefinite", _F),
     "\"Indefinitely\" is only approved as a design property (\"designed to keep recharging\"). Safer to leave it out in public."),
    (re.compile(r"\bsav(e|es|ing|ings)\b[^.]*(\$|\d|percent|%)|(\$|\d+\s?%)[^.]*\bsav(e|es|ing|ings)\b|cut your bill|lower bill guaranteed|half your bill", _F),
     "Savings figure. It can't be known without the bill."),
    (re.compile(r"cheapest|won'?t find (anything )?cheaper|lowest rate|best rate|beat any", _F),
     "Unqualified superiority claim."),
    (re.compile(r"(base power|tesla|powerwall|generac|sunrun|enphase)[^.]*(\d|\$|¢)|(\d|\$|¢)[^.]*(base power|tesla|powerwall|generac|sunrun|enphase)", _F),
     "A competitor named next to a number. We never state their rates, fees or terms."),
    (re.compile(r"tax (credit|deduct|break|incentive)|\bITC\b|\bgrants?\b|\brebates?\b", _F),
     "Tax credits, grants and rebates are never discussed. Route it."),
    (re.compile(r"legal(ly)?\b|by law|\bHOA\b[^.]*(can'?t|cannot|not allowed|illegal)|texas law", _F),
     "Legal opinion. Approved: we deal with HOAs constantly and handle that process for you."),
    (re.compile(r"government|state[- ]funded|federal(ly)? funded|ercot program", _F),
     "Implies a government program. It's a business.", True),
    (re.compile(r"\b(you|you'll|you will|you'd)\b[^.]*\bown\b[^.]*(batter|system|equipment)|yours to keep", _F),
     "Ownership claim. We own the equipment, and the batteries are never the homeowner's.", True),
    (re.compile(r"buy ?out|buy it out|removal (fee|cost)|cost to (cancel|remove)|cancel anytime", _F),
     "Buyout, exit and removal are never estimated or described. Route it."),
    (re.compile(r"net[- ]meter\w*|credit (for|on) (your )?(excess|extra)|paid for (your )?(excess|extra)|sell (your )?(excess|extra) (power|energy) back", _F),
     "No net-metering credit exists on this plan. Excess production funds the program.", True),
    (re.compile(r"light energy|abundance energy", _F),
     "Don't name the retail provider. The engineer confirms which one for the area."),
    (re.compile(r"next week|this week|right away|in no time", _F),
     "Install timing. Nothing tighter than about 45 days once approved."),
    (re.compile(r"(we'?ll|we will|someone will|somebody will)\s+(call|text|email|contact|be in touch)[^.]*(within|every|daily|weekly|by (tomorrow|monday|tuesday|wednesday|thursday|friday))", _F),
     "Promise about follow-up contact. Nobody replying here controls it."),
    (re.compile(r"\d[\d,]*\+?\s+(families|homeowners|customers|homes|installs)", _F),
     "Customer count or statistic. None are approved."),
    (re.compile(r"welcome (aboard|to the family)|(great|glad) to have you (on board|with us)|as (a|our) customer", _F),
     "Confirms someone is a customer. Never do that in public."),
    (re.compile(r"\$\s?40[,.]?000|\b40k\b|forty thousand", _F),
     "The $40,000 figure isn't approved for public replies."),
    (re.compile(r"actually,? (that'?s|you'?re|it'?s) (incorrect|wrong|not true|mistaken)|as (i|we) (said|explained)", _F),
     "Arguing or correcting in public."),
]
WARNINGS = [
    (re.compile(r"\bcredit\b", _F),
     "Mentions credit. Only allowed if the person asked about it first."),
    (re.compile(r"amazing|excited|thrilled|incredible|awesome|game[- ]chang\w+|reach out|love to", _F),
     "Hype or corporate warmth. Plain and understated reads as true."),
    (re.compile(r"!.*!|!!", re.DOTALL),
     "More than one exclamation point."),
    (re.compile(r"—"),
     "Em dash. Use commas and periods."),
    (re.compile("[\U0001F300-\U0001FAFF☀-➿]"),
     "Emoji. Essentially none, and none at all in SMS."),
    (re.compile(r"https?://|www\.", _F),
     "Link. In public, only when the person asked how to sign up."),
]
