---
tags: [engelbart, product, provenance]
created: 2026-08-13
---
# Engelbart: "where did this thought come from"

The one-sentence product: a research notebook that remembers where your thoughts came from.

## what a "trail" is for us
A trail is the chain from a note back to its sources: the chat where I first said it, the paper that made me think it, the
meeting where Yan pushed back. Bush's trail ([[Bush1945 - As We May Think]]) was hand-made; ours has to be mostly automatic,
because nobody curates.

## minimum viable trail
1. every imported item keeps: source tool, original id/path, created time, and the account it came from
2. every note can point at items ("came from") with a span if we have it
3. the canvas shows the trail as a thin line from the note to its sources, collapsed by default
4. two items that are the same thing (same paper from Zotero and Downloads) show up as **one** node with two origins, not two
   nodes. see [[Engelbart - import dedupe]]

## open questions
- time: is the trail "where the idea came from" or "where I first wrote it down"? those differ a lot for me (ideas show up in
  a run, get written in Apple Notes, get argued in Claude)
- privacy: trails into personal stuff (a meal-prep chat that happens to contain a research idea) need to be visible to me
  but not exported with a shared topic
- how much should the trail survive editing? if I rewrite a note completely, is the trail still true?

## H-LAM/T framing for the deck
- Artifacts = the canvas + import. Methodology = topics/goals. Training = the onboarding. we only built A so far
- ([[Engelbart1962 - Augmenting Human Intellect]])
