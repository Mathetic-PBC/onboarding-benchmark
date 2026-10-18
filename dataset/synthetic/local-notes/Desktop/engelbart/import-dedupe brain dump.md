# import dedupe — brain dump (10/14, after Marcus call)

ok so the pilots broke import in two ways and they're the same problem: we don't know what we *should* have.

**missing**: we never compare expected vs got. claude export says 1,400 convos, we paginate to 1,000 and stop.
nobody notices unless the user counts. fix = every connector reports `expected` (from the source's own count / listing)
and we show the gap on the import summary. "1,262 of 1,400 Claude chats — 138 missing, retry?"

**dupes**: the same thing arrives from two tools. cases I've seen:
- paper PDF in Zotero storage + ~/Downloads + Drive (+ attached in gmail). key = DOI. no DOI -> title/first author/year
- a chat exported twice (two export zips, Aug and Oct). key = vendor convo id
- google doc + its downloaded .docx. key = ??? content hash after text extraction? title + modified?
- zip that contains files we also have unzipped. hash members

**not dupes** (do NOT merge):
- "Copy of X" vs "X" — versions, group them
- "deck" vs "deck v2"
- notes.md vs "notes copy.md" (lol I have this on my own desktop)

**wrong items**: stuff that isn't research at all getting dumped into projects (receipts, meal plans). project
assignment should be allowed to say "none". ask: is a training log "a project"? for me yes.

order: expected counts -> DOI dedupe -> version grouping -> "none" bucket. ship to Priya again before pilot 3.
