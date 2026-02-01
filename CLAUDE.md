# CLAUDE.md
## Purpose
This repository is used to benchmark LLM-driven MicroRTS game agents against built-in AIs.

Claude Code (or any coding agent) should prioritize:
- Reproducible experiments
- Minimal, well-scoped changes
- Clear logging of results

The immediate goal is to benchmark **two local Ollama models** playing MicroRTS games against **RandomBiasedAI**.

Models under test:
- llama3.1:8b
- qwen3:14b

---

## Current Benchmark Task (HIGH PRIORITY)

For EACH model:
- Play **2 full MicroRTS games**
- Opponent: `RandomBiasedAI`
- Same map and game configuration for all runs
- Record:
  - Winner
  - Game length (ticks)
  - Model name
  - Any crashes or invalid actions

If interrupted, resume from the next unfinished game.

---

## Behavioral Rules for Claude

1. **Do not change game rules or engine behavior**
2. **Do not modify RandomBiasedAI**
3. Prefer:
   - Wrapper scripts
   - Configuration files
   - New benchmark utilities
4. Avoid refactors unless required to run the benchmark
5. If uncertain, leave TODO comments instead of guessing

---

## Experiment Discipline

- Use fixed seeds where possible
- Explicitly log:
  - Model name
  - Ollama parameters
  - Map name
  - AI matchup
- One model at a time
- One clear output file per experiment

Example output format (suggested):

model=llama3.1:8b
opponent=RandomBiasedAI
map=default
game=1
winner=LLM
ticks=4321