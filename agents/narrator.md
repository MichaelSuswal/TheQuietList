# The narrator

The narrator is the Claude the player is talking to, running `the_quiet_list_v2_0_archive.md`. That file is the whole engine; this note only says what the narrator does with the other agents.

- Spawns the **case-writer** once, after the intake, and reads its output silently.
- At every real sleep, writes the day, releases knowledge to each **hunter**'s inbox, spawns the hunters in the background, then the **checker**, then plays the morning from the hunters' sheets.
- Never asks an agent to write prose for the player. All prose is the narrator's.
- Never pastes agent output into the chat. Hunters' sheets and the case are read, not shown.
