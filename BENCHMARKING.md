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

In `resources/config.properties`:

```properties
AI2=ai.RandomBiasedAI    # Standard benchmark opponent
```

Available baseline opponents:
| Opponent | Difficulty | Description |
|----------|------------|-------------|
| `ai.PassiveAI` | Trivial | Does nothing |
| `ai.RandomAI` | Very Easy | Random valid actions |
| `ai.RandomBiasedAI` | Easy | Prefers useful actions |
| `ai.abstraction.LightRush` | Medium | Aggressive light units |
| `ai.abstraction.HeavyRush` | Medium | Aggressive heavy units |

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

### Win Rate by Opponent

| Opponent | Expected LLM Win Rate (Good Agent) |
|----------|-----------------------------------|
| PassiveAI | 100% |
| RandomAI | 90%+ |
| RandomBiasedAI | 70%+ |
| LightRush | 50%+ |
| HeavyRush | 50%+ |

### Common Failure Modes

1. **Timeout** - LLM inference too slow (use GPU)
2. **Invalid JSON** - LLM doesn't follow response format
3. **Invalid Actions** - Actions reference wrong positions or unit types
4. **Poor Strategy** - Valid actions but loses to opponent

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
