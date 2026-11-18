# SPOILERS. Do not open.

This folder holds the truth of the game: the sealed case, the hunters' private sheets, the roll log, the meters' event history. Opening it ends the mystery.

The honor system is the only lock. After credits, the narrator opens it for you (the director's cut).

- `case/case.md`: the sealed case, written by the case-writer agent at the start of the campaign. Never summarized in chat.
- `agents/<name>/`: one folder per hunter. `role.md` (who they are), `inbox/day-N.md` (what reached them that day), `sheet.md` (knows, believes, intends), `log.md` (their private diary).
- `rolls.log`: every roll, with its target and purpose.
- `events` live in `state/events.jsonl`; the computed stage and band in `state/meters.json`.
