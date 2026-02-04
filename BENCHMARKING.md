# LLM Benchmarking Guide

This guide explains how to use MicroRTS as a benchmark suite for evaluating LLM game-playing capabilities.

---

## Purpose

MicroRTS provides a controlled environment to measure:
- **Strategic reasoning** - Can the LLM develop and execute winning strategies?
- **State understanding** - Can it correctly parse game state descriptions?
- **Action generation** - Can it produce valid, well-formed action commands?
- **Real-time performance** - Can it respond quickly enough for gameplay?

---

## Quick Start

```bash
# 1. Start Ollama (GPU recommended)
srun --gres=gpu:1 --pty bash  # If on HPC
ollama serve &

# 2. Run the benchmark
./benchmark.sh
```

---

## Benchmark Configuration

### Models to Test

Edit `benchmark.sh` or set environment variables:

```bash
export OLLAMA_MODEL="llama3.1:8b"   # Model under test
```

Supported models (via Ollama):
- `llama3.1:8b` - Meta Llama 3.1 8B
- `qwen3:14b` - Alibaba Qwen 3 14B
- `mistral` - Mistral 7B
- `llama3.3:70b` - Meta Llama 3.3 70B (requires ~42GB VRAM)

### Opponents

The benchmark arena (v2.0) uses **single-elimination** against 6 reference AIs. LLMs must **win** to advance to the next opponent. A draw, loss, or timeout eliminates.

| # | Opponent | Class | Tier | Weight | Description |
|---|----------|-------|------|--------|-------------|
| 1 | RandomBiasedAI | `ai.RandomBiasedAI` | Easy | 10 pts | Prefers useful actions |
| 2 | HeavyRush | `ai.abstraction.HeavyRush` | Medium-Hard | 20 pts | Heavy unit pressure |
| 3 | LightRush | `ai.abstraction.LightRush` | Medium | 15 pts | Aggressive light units |
| 4 | WorkerRush | `ai.abstraction.WorkerRush` | Medium | 15 pts | Aggressive workers |
| 5 | Tiamat | `ai.competition.tiamat.Tiamat` | Hard | 20 pts | Competition-winning bot |
| 6 | CoacAI | `ai.coac.CoacAI` | Hard | 20 pts | Competition-winning bot |

Total: **100 points**. If an LLM can't beat an easier opponent, there's no point playing harder ones.

**Note:** CoacAI and Tiamat require the bot JARs in `lib/bots/`. The arena uses classpath `lib/*:lib/bots/*:bin`.

Additional opponents (not in benchmark, for manual testing):

| Opponent | Difficulty | Description |
|----------|------------|-------------|
| `ai.PassiveAI` | Trivial | Does nothing |
| `ai.RandomAI` | Very Easy | Random valid actions |

### Game Settings

In `resources/config.properties`:

```properties
map_location=maps/8x8/basesWorkers8x8.xml  # Map
max_cycles=5000                             # Max game length
headless=true                               # No GUI
```

---

## Running Benchmarks

### Single Model Test

```bash
# Set model and run
export OLLAMA_MODEL="llama3.1:8b"
./benchmark.sh
```

### Multi-Model Comparison

```bash
for model in "llama3.1:8b" "qwen3:14b" "mistral"; do
    export OLLAMA_MODEL="$model"
    ./benchmark.sh
done
```

### Benchmark Arena (Recommended)

```bash
# Run full benchmark (all LLMs vs all 6 reference AIs)
python3 benchmark_arena.py

# Run with multiple games per matchup
python3 benchmark_arena.py --games 3
```

This produces:
- `benchmark_results/benchmark_YYYY-MM-DD_HH-MM.json` (detailed results)
- `benchmark_results/RESULTS.md` (formatted report)
- `benchmark_results/leaderboard.json` (appended entries)

### Generating the Consolidated Leaderboard

After running one or more benchmarks:

```bash
python3 generate_leaderboard.py
```

This reads all `benchmark_results/benchmark_*.json` files, finds the best score per model, and generates:
- `benchmark_results/leaderboard.json` (consolidated best-score-per-model)
- `benchmark_results/LEADERBOARD.md` (rich per-opponent breakdown table)

Both v1.0 (2 opponents) and v2.0 (6 opponents) result files are handled. Scores from different versions are not directly comparable.

### Using RunLoop for Multiple Games

```bash
# Edit RunLoop.sh settings
TOTAL_RUNS=10            # Games per session
RUN_TIME_PER_GAME_SEC=300  # Timeout per game

./RunLoop.sh
```

---

## Output Format

### Benchmark Results

Output files: `benchmark_results_YYYY-MM-DD_HH-MM-SS.txt`

```
model=llama3.1:8b opponent=RandomBiasedAI map=8x8/basesWorkers8x8 game=1 winner=LLM ticks=4321 crashed=no
model=llama3.1:8b opponent=RandomBiasedAI map=8x8/basesWorkers8x8 game=2 winner=Opponent ticks=3892 crashed=no
```

### CSV Game Logs

Output files: `Response<TIMESTAMP>_<AI1>_<AI2>_<MODEL>.csv`

Contains per-game statistics including scores and actions.

### Detailed Logs

The `logs/` directory contains detailed game traces including LLM responses.

---

## Metrics

### Primary Metrics

| Metric | Description |
|--------|-------------|
| **Win Rate** | Percentage of games won against opponent |
| **Average Game Length** | Mean ticks to game completion |
| **Crash Rate** | Percentage of games with invalid actions |

### Secondary Metrics

| Metric | Description |
|--------|-------------|
| **Response Time** | Average LLM inference time |
| **Valid Action Rate** | Percentage of LLM actions that were valid |
| **Resource Efficiency** | Resources gathered vs spent |

---

## Hardware Requirements

### Minimum (CPU)
- Any modern CPU
- 16GB RAM
- **Warning:** CPU inference is too slow for real-time play; games will timeout

### Recommended (GPU)
- NVIDIA GPU with 8GB+ VRAM
- 16GB+ system RAM
- GPU provides ~10-50x faster inference

### Model VRAM Requirements

| Model | VRAM Required |
|-------|---------------|
| llama3.1:8b | ~5GB |
| qwen3:14b | ~9GB |
| mistral | ~5GB |
| llama3.3:70b | ~42GB |

---

## HPC Cluster Usage

### Request GPU Resources

```bash
# Interactive
srun --gres=gpu:1 --pty bash

# Batch job
sbatch benchmark_gpu.sh
```

### Verify GPU Access

```bash
nvidia-smi                    # Should show GPU info
ollama ps                     # Should show "100% GPU" not "100% CPU"
```

See [GPU_SETUP.md](GPU_SETUP.md) for detailed HPC instructions.

---

## Interpreting Results

### Expected Win Rates (Elimination Order)

| # | Opponent | Tier | Expected Win Rate (Good LLM) |
|---|----------|------|------------------------------|
| 1 | RandomBiasedAI | Easy | 80%+ |
| 2 | HeavyRush | Medium-Hard | 30-50% |
| 3 | LightRush | Medium | 50-70% |
| 4 | WorkerRush | Medium | 50-70% |
| 5 | Tiamat | Hard | 10-30% |
| 6 | CoacAI | Hard | 10-30% |

**Score interpretation:** An LLM eliminated at RandomBiasedAI scores 0-12 (F). Clearing easy+medium opponents: ~40-60 (D-C). Competing with hard AIs: 70-100 (B to A+).

### Common Failure Modes

1. **Timeout** - LLM inference too slow (use GPU)
2. **Invalid JSON** - LLM doesn't follow response format
3. **Invalid Actions** - Actions reference wrong positions or unit types
4. **Poor Strategy** - Valid actions but loses to opponent

---

## LLM vs LLM Games

You can run two LLMs against each other to compare their strategic capabilities.

### Using Different Ollama Models

```bash
# Set different models for each player
export OLLAMA_MODEL="llama3.1:8b"      # Player 0
export OLLAMA_MODEL_P2="qwen3:4b"      # Player 1

# Update config.properties
# AI1=ai.abstraction.ollama
# AI2=ai.abstraction.ollama2
```

### Using Ollama vs Gemini

```bash
# Set Ollama model for Player 0
export OLLAMA_MODEL="llama3.1:8b"

# Set Gemini API key for Player 1
export GEMINI_API_KEY="your-api-key"

# Update config.properties
# AI1=ai.abstraction.ollama
# AI2=ai.abstraction.LLM_Gemini
```

### Available LLM AI Classes

| Class | Environment Variables | Description |
|-------|----------------------|-------------|
| `ai.abstraction.ollama` | `OLLAMA_MODEL`, `OLLAMA_HOST` | Primary Ollama agent |
| `ai.abstraction.ollama2` | `OLLAMA_MODEL_P2`, `OLLAMA_HOST` | Second Ollama agent (different model) |
| `ai.abstraction.LLM_Gemini` | `GEMINI_API_KEY` | Google Gemini API |

### Example: LLM Tournament

```bash
#!/bin/bash
models=("llama3.1:8b" "qwen3:4b" "mistral:7b")
for m1 in "${models[@]}"; do
    for m2 in "${models[@]}"; do
        if [ "$m1" != "$m2" ]; then
            export OLLAMA_MODEL="$m1"
            export OLLAMA_MODEL_P2="$m2"
            echo "Running: $m1 vs $m2"
            java -cp "lib/*:bin" rts.MicroRTS -f resources/config.properties
        fi
    done
done
```

---

## Adding New LLM Backends

To benchmark a new LLM provider:

1. Create `src/ai/abstraction/NewLLM.java` extending `AbstractionLayerAI`
2. Implement `getAction(int player, GameState gs)`
3. Handle API calls and JSON parsing
4. Reference in config: `AI1=ai.abstraction.NewLLM`

See existing implementations for examples:
- `ollama.java` - Local Ollama API
- `LLM_Gemini.java` - Google Gemini API
- `mistral.java` - Mistral API

---

## Reproducibility

For reproducible benchmarks:

1. **Fixed seeds** - Use deterministic game settings
2. **Document configuration** - Record model, map, opponent, max_cycles
3. **Multiple runs** - Run each configuration multiple times
4. **Hardware notes** - Document GPU model and driver version

Example benchmark metadata:
```
Date: 2026-02-01
Model: llama3.1:8b via Ollama 0.1.x
GPU: NVIDIA RTX A6000
Map: maps/8x8/basesWorkers8x8.xml
Opponent: RandomBiasedAI
Games: 10
Max Cycles: 5000
```
