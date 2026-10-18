# Juno graveyard

Created: February 7, 2026 12:20 AM
Tags: archive, juno

Everything I built for Juno (2023–2025) and why each piece died. Writing it down so I stop reopening the repos at 1am.

<aside>
🪦 Juno = customizable AI voice agents ("conversational entities") you could give a persona, a voice and a memory. CLI first, then a lab web app, then a browser extension.

</aside>

## The graves

- **juno CLI** (spring 2023 → fall 2023)
    - What it was: `juno new --persona tutor --voice warm` spun up a voice agent in the terminal; push-to-talk with the space bar.
    - Cause of death: latency. 2.5–4 s round trip (STT → LLM → TTS) made every conversation feel like a bad phone line. Streaming TTS helped but never got under 1.5 s.
    - Salvage: the persona YAML format was actually nice.
- **Juno lab web app** (2024)
    - What it was: a web page where PRIME Lab people could build agents and share a link with study participants.
    - Cause of death: nobody wanted a generic agent builder; every study needed something custom, and I became the custom-builder.
    - Salvage: the transcript viewer with per-turn timing.
- **browser extension** (early 2025)
    - What it was: talk to any webpage; agent reads the DOM and answers questions about it.
    - Cause of death: Chrome Web Store review rejected it twice for broad host permissions; by the time I narrowed them every big lab shipped the same thing.
    - Salvage: nothing really. maybe the "explain this paragraph" shortcut.
- **memory layer** (never shipped)
    - Agents were supposed to remember past chats with a user. Ended up as a JSON file per user that grew forever.
    - Cause of death: I never figured out what was worth remembering. This is the part I keep thinking about.

## What I learned

1. Voice is a delivery format, not the product. People came for the persona and left because of latency.
2. Building a platform before having one user with one real job to do = graveyard.
3. The memory question (what should a tool remember about how you think) is still the interesting one. → maybe the notebook idea is the real version of it.

## Don't

- [ ] don't revive the CLI
- [ ] don't port the extension to MV3 "just to see"
