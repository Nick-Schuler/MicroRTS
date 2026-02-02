# Game Run: Gemini 2.5 Flash vs RandomBiasedAI (LLM_INTERVAL=100)

## Date
2026-02-02 04:14 UTC

## Configuration
- **LLM Model**: gemini-2.5-flash (Google Gemini API)
- **Opponent**: RandomBiasedAI
- **Map**: maps/8x8/basesWorkers8x8.xml
- **Max Cycles**: 5000
- **LLM_INTERVAL**: 100 (API called every 100 game ticks)
- **API Tier**: Free tier (5 requests/minute limit)

## Result: FAILED - Rate Limited at Turn 600

The game ran for **600 turns** (7 API calls at turns 0, 100, 200, 300, 400, 500, 600) before hitting rate limit.

### Game State at Failure (Turn 600)
- **LLM**: Only base remaining (9 HP, 8 resources) - no workers
- **RandomBiasedAI**: 8 workers scattered across map, no base
- **Likely outcome**: LLM LOSS (8 workers would destroy base)

## Strategic Analysis

### Turn-by-Turn Progression

| Turn | LLM Strategy | Enemy Base HP | Key Event |
|------|--------------|---------------|-----------|
| 0    | Economy: harvest + train workers | 10 | Initial setup |
| 100  | "All-in" attack started | 10 | Sent workers to attack |
| 200  | Continue attack | 6 | Good progress |
| 300  | Committed all workers | 3 | Almost destroyed |
| 400  | Continue assault | 3 | Stalemate |
| 500  | Victory achieved | 0 (destroyed) | Enemy base eliminated |
| 600  | Economy rebuild | N/A | Only base left, 8 enemy workers incoming |

### Key Insight: Pyrrhic Victory
The LLM successfully **destroyed the enemy base** at Turn 500, but lost all workers in the process. Meanwhile, RandomBiasedAI's workers (which were out harvesting/exploring) survived and turned around to attack the now-defenseless LLM base.

This demonstrates a strategic flaw: the LLM correctly identified and executed an "all-in" attack, but failed to:
1. Preserve any workers for defense
2. Account for enemy workers that weren't at the base
3. Rebuild economy after winning the engagement

## Performance Metrics

| Turn | Prompt Tokens | Response Tokens | Latency (ms) |
|------|---------------|-----------------|--------------|
| 0    | 1544          | 359             | 4294         |
| 100  | 1612          | 403             | 7047         |
| 200  | 1660          | 506             | 5946         |
| 300  | 1685          | 435             | 5567         |
| 400  | 1713          | 460             | 5310         |
| 500  | 1695          | 506             | 5429         |

**Average Latency**: ~5.6 seconds per API call
**Average Response Tokens**: ~445 (more complex decisions than first run)

## Comparison with First Run (LLM_INTERVAL=1)

| Metric | Run 1 (interval=1) | Run 2 (interval=100) |
|--------|-------------------|---------------------|
| Turns completed | 6 | 600 |
| API calls | 6 | 7 |
| Game progress | Minimal | Significant |
| Rate limit hit | Yes | Yes |

## Key Findings

1. **LLM_INTERVAL=100 allows 100x more game progression** before rate limit

2. **Strategic depth improved** - LLM showed adaptive behavior:
   - Recognized enemy base HP (3) and committed to "all-in"
   - Made context-aware decisions based on game state

3. **Still hit rate limit** - Free tier insufficient even with 100-tick intervals

4. **Revealed strategic weakness** - "All-in" attacks can backfire when enemy has distributed units

## Recommendations

- Increase `LLM_INTERVAL` further (200-500) for free tier
- OR use paid API tier for serious benchmarking
- OR use local Ollama (no rate limits)
- Consider adding logic to preserve some workers for defense

## Files
- `response.csv` - Move-by-move data with tokens and latency
- `llm_responses.json` - Raw LLM JSON responses
