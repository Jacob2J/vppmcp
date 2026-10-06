# VPP Texas MCP

The official guide to VPP Texas for people, crawlers and LLMs: who we are, what the offer is, and how to reply to comments about it.

It's a read-only [FastMCP](https://gofastmcp.com) server. Nothing it returns is improvised. If a claim about the offer isn't in the approved facts, the server says so and points at an engineer call.

## What's in it

| Tool | What it does |
|---|---|
| `about_vpp_texas` | Who we are and how the offer is paid for |
| `list_approved_facts` | Every fact that may be stated about the offer, by topic |
| `find_approved_answer` | The approved answer to a question, or where to route it |
| `check_general_fit` | A first read on whether the program could fit a home. Never says a home qualifies |
| `how_to_book` | The next step: a 40 minute video call with an engineer |
| `get_reply_guide` | Voice, conduct rules and limits for public comments, DMs and SMS |
| `list_comment_intents` | The triage list for incoming comments and what to do with each |
| `get_reply_guidance` | The action, approved facts and an example reply for one intent |
| `check_reply` | Checks a drafted reply against claims that may never be made |

Resources: `vpp://about`, `vpp://facts`, `vpp://never-say`, `vpp://reply-guide`.
Prompt: `reply_to_comment`.
Over HTTP the same guide is also served as plain text at `/llms.txt`.

## What it won't tell you

Savings figures, a blended rate for a home, competitor pricing, buyout or exit costs, system sizing for a specific home, and anything legal, tax or credit related. Those get worked out with an engineer from the home's actual electric bill.

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Local, over stdio:

```bash
.venv/bin/fastmcp run server.py:mcp
```

Over HTTP (MCP at `/mcp`, plain text at `/llms.txt`):

```bash
.venv/bin/fastmcp run server.py:mcp --transport http --port 8000
```

To host it, point any FastMCP-compatible host at this repo with the entrypoint `server.py:mcp`.

Optional environment variables: `VPP_WEBSITE` and `VPP_BOOKING_URL`. Both default to `https://vpptexas.com`.

## Replying to comments with it

1. `list_comment_intents`, then classify the comment. If it can't be classified with confidence, it goes to a person.
2. `get_reply_guidance` for that intent and channel.
3. Draft using only the approved facts returned.
4. `check_reply` on the draft, and fix every block.
5. A person approves the reply before it posts.

`check_reply` is keyword matching, so it misses paraphrase. A clean result is a floor, not an approval.

## Changing a fact

Every fact lives in `knowledge.py`, which mirrors the company's internal approved-claims list. When the offer changes, update both in the same pass, bump `CLAIMS_VERIFIED`, and run the tests:

```bash
.venv/bin/pip install pytest && .venv/bin/python -m pytest -q
```

The tests are the gate. They fail if a known unapproved claim stops being blocked, or if anything internal leaks into a public response.
