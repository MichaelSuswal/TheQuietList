# 조용한 명단 · The Quiet List

A text adventure that runs inside Claude. Seoul, winter 1997, the IMF crisis. Your husband is murdered and the police close the case in three days. You find the thread they would not follow, and you decide to pull it yourself, name by name, up a chain of killers toward the man who ordered it. You have 49 days of mourning to finish it, a sister who will help, a detective circling closer, and one question you cannot answer until the end: justice, or becoming a killer.

The character is a version of you. Play in any language; Korean is native to the world.

## Two editions

**Standard Edition.** One file. Download `the_quiet_list_v2_1_standard.md`, start a new chat in Claude (a regular chat, not inside a Project), attach the file, and say hello. Nothing else to set up. Saves are text blocks you paste into a new chat to continue.

**Archive Edition.** The same game, kept in a private GitHub repository of your own that Claude manages for you. You get a case written fresh for your campaign that no one has read, hunters who think and move while you sleep, a continuity checker that catches the narrator's mistakes, a drawn evidence board and map of the city as you know it, and an optional sketchbook. Setup takes about fifteen minutes and Claude walks you through it. Download `the_quiet_list_v2_1_archive.md`, start a new chat (a regular chat, not inside a Project), attach it, and follow the setup. You will need a GitHub account (free) connected to Claude, and you will click **Use this template** on this page to make your own copy of the game.

Both editions run on current Claude models. The game is free.

## For the curious

- `engine/`: the parts of the engine that differ between editions, and the case brief that binds every campaign's sealed case.
- `agents/`: the roles Claude spawns in the Archive Edition (case-writer, hunter, checker).
- `checks/`: the failures checklist.
- `tools/`: small scripts for the things that must be exact (dice, the clock, travel times, the meters, the board, the sketchbook).
- `player/`, `state/`, `SPOILERS_do_not_open/`: the shape of a campaign's record. Empty in the template; filled during play. Never open the spoilers folder of a campaign you are playing.

Created by Creon Ghan Buri. First played by Seah.
