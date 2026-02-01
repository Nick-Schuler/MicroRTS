# CLAUDE.md

Instructions for Claude Code (or any AI coding assistant) working on this repository.

---

## Repository Purpose

This repository serves three purposes:
1. **MicroRTS Game Engine** - Fork of original MicroRTS Java codebase
2. **LLM Competition Platform** - Template for 2026 IEEE WCCI competition
3. **LLM Benchmark Suite** - Tools to measure LLM game-playing performance

---

## Key Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main entry point, overview of all three purposes |
| `COMPETITION.md` | Competition setup and rules |
| `BENCHMARKING.md` | How to benchmark LLMs |
| `MICRORTS_ORIGINAL.md` | Original MicroRTS documentation |
| `PROJECT_STRUCTURE.md` | Codebase navigation reference |
| `LLM_PROMPTS.md` | LLM prompt format specification |
| `GPU_SETUP.md` | HPC/GPU setup instructions |

---

## Behavioral Rules

1. **Do not change game rules or engine behavior** - The `rts/` package should remain unchanged
2. **Do not modify baseline AIs** - `RandomBiasedAI`, `RandomAI`, etc. are reference implementations
3. **Prefer non-invasive changes:**
   - Wrapper scripts
   - Configuration files
   - New benchmark utilities
4. **Avoid refactors** unless required for a specific task
5. **Leave TODO comments** rather than guessing at unclear requirements

---

## Common Tasks

### Run a benchmark
```bash
srun --gres=gpu:1 --pty bash  # If on HPC
ollama serve &
./benchmark.sh
```

### Compile the project
```bash
find src -name '*.java' > sources.list
javac -cp "lib/*:bin" -d bin @sources.list
```

### Run with GUI
```bash
java -cp "lib/*:bin" gui.frontend.FrontEnd
```

### Run headless
```bash
java -cp "lib/*:bin" rts.MicroRTS -f resources/config.properties
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/ai/abstraction/ollama.java` | Main LLM agent implementation |
| `resources/config.properties` | Game configuration |
| `benchmark.sh` | Benchmark runner script |
| `RunLoop.sh` | Multi-game execution script |

---

## Experiment Discipline

When running experiments:
- Use fixed seeds where possible
- Log: model name, map, opponent, max_cycles
- One model at a time
- One clear output file per experiment

Example output format:
```
model=llama3.1:8b opponent=RandomBiasedAI map=8x8/basesWorkers8x8 game=1 winner=LLM ticks=4321
```
