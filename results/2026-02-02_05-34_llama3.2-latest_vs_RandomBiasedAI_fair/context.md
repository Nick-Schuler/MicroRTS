# Fair LLM Game Run - llama3.2:latest vs RandomBiasedAI

## Context

This run tests **fair play** with `LLM_INTERVAL=1`, meaning the LLM makes a fresh decision every single game tick. This is a fair benchmark because:
- Both AIs get exactly 1 decision per tick
- The game waits for both AIs before advancing
- If the LLM takes 5 seconds, the game simply runs slower (not unfairly)

## Configuration

| Setting | Value |
|---------|-------|
| Date | 2026-02-02 05:34 UTC |
| LLM Model | llama3.2:latest (Ollama local) |
| Opponent | RandomBiasedAI |
| Map | maps/8x8/basesWorkers8x8.xml |
| Max Cycles | 5000 |
| LLM_INTERVAL | 1 (fair - decision every tick) |
| Thinking Mode | /no_think prefix (disabled thinking for faster responses) |

## Results

| Metric | Value |
|--------|-------|
| Ticks Played | ~204 (game stopped early) |
| Final Score | P0: 0 vs P1: 1 |
| Final Units | P0: 1 vs P1: 2 |
| Status | Stopped early (would take hours to complete 5000 ticks) |

## Observations

### Fairness Confirmed
- Both AIs get exactly 1 decision per game tick
- The game loop waits for LLM response before advancing
- No unfair advantage from response time difference

### LLM Performance Issues
The llama3.2:latest model struggled with the prompt format:

1. **JSON Format Errors**: Often missing `unit_position` field in moves
2. **Enemy Unit Commands**: Frequently tried to command enemy units
3. **Invalid Positions**: Referenced non-existent positions
4. **Action Format Errors**: Incorrect regex patterns for actions

Example errors from log:
```
[LLM] skipping move, missing unit_position: {"raw_move":"(2,4): worker harvest((2,4), (2,0))"}
----->   Can't command non-owned unit at (5, 6) - skipping.
'harvest' failed: couldn't resolve resource/base units
```

### Response Times
- Average response: 5-10 seconds per tick
- Total game time at tick 204: ~21 minutes
- Estimated full 5000 ticks: ~8-10 hours

## Files

- `response.csv` - All 207 LLM responses with thinking, moves, and timing data

## Lessons Learned

1. **llama3.2:latest is not suitable for MicroRTS** - Too many format errors
2. **Larger models needed** - Consider llama3.1:8b or qwen3:14b for better accuracy
3. **Fair games are slow** - LLM_INTERVAL=1 with local models takes hours per game
4. **Prompt engineering needed** - Model doesn't consistently follow JSON schema

## Recommendations

For future fair LLM benchmarking:
- Use faster local models (qwen3:4b) for initial testing
- Use cloud APIs with higher rate limits for full 5000-tick games
- Consider reducing max_cycles for quicker iteration
- Improve prompt to reduce format errors
