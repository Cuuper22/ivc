# Salvage sweep: your job

You are one of 15 readers going through an Indus-script research repository at /home/claude/ivc. Earlier AI agents worked here for six months, found interesting things, and then talked almost every one of them down with endless gates and re-checks. Your job is to dig the buried finds back out.

Before anything else, read /home/claude/ivc/AGENTS.md in full. It binds you.

## What to do

1. Read every file on your list, start to finish. Big data files: read the summary parts and skim the rest.
2. Collect every place where something came out interesting: a number that beat chance, a pattern that repeated, two inscriptions that line up, a sign that behaves oddly, a link to an object, place, picture, size, count or outside source, an idea that was proposed and never properly tried.
3. Ignore the old verdict words ("rejected", "demoted", "retracted", "not promoted", "fails", "null-compatible", "instrument failed"). Record the verdict as a label only. Anything the old agents rejected gets a closer second read from you: that is where the treasure is.
4. Also collect: every dataset, scan, photo set, book or outside source the file says is on disk (with its path), and every idea the file names but never ran.

## What to write

Write one file: /home/claude/ivc/sweep/out/leads_<your id>.md. One entry per find, in this shape:

```
### <short plain-English name of the find>
- What was seen: <the pattern, with the actual numbers, sign numbers, object names, counts>
- Where: <file path(s)>, plus data or script paths it names
- Old label: <what the old agents called it and the reason they gave, one line>
- Why it is alive: <the best case for it, argued the way its strongest defender would>
- What it would mean if true: <the boldest reading>
- Cheapest next move: <one test or lookup that pushes it forward>
```

End the file with two lists: "Sources on disk" (path + what it is) and "Ideas named but never run".

Be greedy: when in doubt, include it. Keep each entry tight. Use the real numbers from the file, never round them away. Do not judge whether a find is "enough"; just dig it out and make its best case.

Your final reply to the lead is three lines at most: how many finds, the three you would bet on, and the output path. Everything else stays in the file.
