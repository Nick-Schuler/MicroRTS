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

---

## Benchmark Results (2026-02-01)

**Status:** All games timed out - GPU required for playable inference speed

| Model | Game | Winner | Ticks | Status |
|-------|------|--------|-------|--------|
| llama3.1:8b | 1 | unknown | unknown | timeout |
| llama3.1:8b | 2 | unknown | unknown | timeout |
| qwen3:14b | 1 | unknown | unknown | timeout |
| qwen3:14b | 2 | unknown | unknown | timeout |

**Configuration:**
- Map: maps/8x8/basesWorkers8x8.xml
- Max Cycles: 5000
- Timeout per game: 300 seconds
- Ollama running on CPU

**Finding:** CPU-only inference is too slow for real-time gameplay. All games timed out because the LLM couldn't generate responses fast enough. Games hung at the first `[ollama.getAction]` call.

**Recommendation:** Run benchmarks on a GPU node with:
```bash
srun --gres=gpu:1 --pty bash
ollama serve &
./benchmark.sh
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `benchmark.sh` | Main benchmark script |
| `benchmark_gpu.sh` | GPU-aware benchmark with SLURM |
| `benchmark_results_*.txt` | Output results |
| `logs/` | Game logs per run |
| `GPU_SETUP.md` | GPU setup instructions |
| `PROJECT_STRUCTURE.md` | Codebase structure reference |