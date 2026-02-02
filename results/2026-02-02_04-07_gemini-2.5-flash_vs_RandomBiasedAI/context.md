# Game Run: Gemini 2.5 Flash vs RandomBiasedAI

## Date
2026-02-02 04:07 UTC

## Configuration
- **LLM Model**: gemini-2.5-flash (Google Gemini API)
- **Opponent**: RandomBiasedAI
- **Map**: maps/8x8/basesWorkers8x8.xml
- **Max Cycles**: 5000
- **LLM_INTERVAL**: 1 (API called every game tick)
- **API Tier**: Free tier (5 requests/minute limit)

## Result: FAILED - Rate Limited

The game ran for only **6 turns** before hitting the Gemini API rate limit.

### Error Message
```
Error response: {"error": {"code": 429, "message": "You exceeded your current quota...
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests,
limit: 5, model: gemini-2.5-flash"}}
```

## LLM Performance (Before Failure)

### Strategy Observed
Gemini showed consistent, sound strategic reasoning:
1. Train workers from base to build economy
2. Harvest resources from nearest node (0,0)
3. Plan all-in attack on enemy base (5,6) once scaled up

### Moves Generated (all 6 turns)
```
(2, 1): base train(worker)
(1, 1): worker harvest((0, 0), (2, 1))
```

### Metrics

| Turn | Prompt Tokens | Response Tokens | Latency (ms) |
|------|---------------|-----------------|--------------|
| 0    | 1544          | 399             | 4362         |
| 1    | 1558          | 284             | 3676         |
| 2    | 1558          | 380             | 5107         |
| 3    | 1558          | 400             | 5683         |
| 4    | 1558          | 405             | 4860         |
| 5    | 1558          | 371             | 8624         |

**Average Latency**: ~5.4 seconds per API call

## Key Findings

1. **LLM_INTERVAL=1 is incompatible with free tier** - Calling the API every tick exhausts 5 req/min quota almost instantly

2. **JSON output quality is excellent** - All responses were valid, properly formatted JSON matching the required schema

3. **Strategic reasoning is good** - The LLM correctly prioritized economy before military

## Recommendations

- Increase `LLM_INTERVAL` to at least 100 (call LLM every 100 ticks instead of every tick)
- For serious benchmarking, use paid API tier or local Ollama
- The LLM_Gemini.java code should handle API errors gracefully instead of crashing

## Files
- `response.csv` - Move-by-move data with tokens and latency
- `llm_responses.json` - Raw LLM JSON responses
