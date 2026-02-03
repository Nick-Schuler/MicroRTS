# MicroRTS LLM Benchmark Results

## Latest Benchmark: 2026-02-03

### Configuration

| Setting | Value |
|---------|-------|
| Map | `maps/8x8/basesWorkers8x8.xml` |
| Max Cycles | 1500 |
| Games per Matchup | 1 |

### Scoring System

Scores are based on performance against fixed reference AIs (0-100 scale):

| Reference AI | Difficulty | Max Points |
|--------------|------------|------------|
| RandomBiasedAI | Easy | 40 |
| WorkerRush | Hard | 60 |

**Per-game scoring:**
- Win: 1.0 points (+ 0.2 bonus for fast wins)
- Draw: 0.5 points
- Loss/Timeout: 0.0 points

---

## Leaderboard

| Rank | Model | Score | Grade |
|------|-------|-------|-------|
| 1 | gemini-2.5-flash | **50.0** | D |
| 2 | llama3.1:8b | 0.0 | F |
| 3 | qwen3:4b | 0.0 | F |

---

## Detailed Results

### gemini-2.5-flash (Score: 50.0)

| Opponent | Result | Ticks | Game Score | Weight | Points |
|----------|--------|-------|------------|--------|--------|
| RandomBiasedAI | DRAW | 1500 | 0.50 | 40 | 20.0 |
| WorkerRush | DRAW | 1500 | 0.50 | 60 | 30.0 |

### llama3.1:8b (Score: 0.0)

| Opponent | Result | Ticks | Game Score | Weight | Points |
|----------|--------|-------|------------|--------|--------|
| RandomBiasedAI | TIMEOUT | 1500 | 0.00 | 40 | 0.0 |
| WorkerRush | TIMEOUT | 1500 | 0.00 | 60 | 0.0 |

### qwen3:4b (Score: 0.0)

| Opponent | Result | Ticks | Game Score | Weight | Points |
|----------|--------|-------|------------|--------|--------|
| RandomBiasedAI | TIMEOUT | 1500 | 0.00 | 40 | 0.0 |
| WorkerRush | TIMEOUT | 1500 | 0.00 | 60 | 0.0 |

---

## Head-to-Head Results (Supplementary)

These games do not affect benchmark scores but show relative performance between LLMs.

| Player 1 | Player 2 | Result | Ticks |
|----------|----------|--------|-------|
| llama3.1:8b | qwen3:4b | TIMEOUT | 1500 |
| llama3.1:8b | gemini-2.5-flash | DRAW | 1500 |
| qwen3:4b | gemini-2.5-flash | DRAW | 1500 |

---

## Analysis

### Key Findings

1. **Gemini performed best** - Cloud API response times allowed games to complete within timeout, achieving draws against both reference AIs.

2. **Local Ollama models timed out** - LLM inference bottleneck (~10+ seconds per move) caused subprocess timeouts before games could conclude.

3. **No wins recorded** - All LLMs played defensively, resulting in draws or timeouts rather than decisive victories.

### Recommendations for Future Benchmarks

- Use GPU-accelerated Ollama for faster local inference
- Increase `GAME_TIMEOUT` for slower models
- Consider running overnight batch jobs for comprehensive testing
- Test with smaller/faster local models

---

## Grade Scale

| Grade | Score Range | Description |
|-------|-------------|-------------|
| A+ | 90-100 | Excellent - beats hard AI consistently |
| A | 80-89 | Very Good - beats hard AI sometimes |
| B | 70-79 | Good - solid performance |
| C | 60-69 | Average - beats easy AI |
| D | 40-59 | Below Average - draws common |
| F | 0-39 | Failing - losses/timeouts |

---

*Generated from benchmark_2026-02-03_05-48.json*
