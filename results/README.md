# Game Run Results

This folder stores results from LLM vs AI game runs for future reference and learning.

## Purpose
- Document experiment outcomes to avoid repeating failed configurations
- Track LLM performance across different settings
- Provide context for each run's success or failure

## Folder Structure
Each run is stored in a subfolder named: `YYYY-MM-DD_HH-MM-SS_<model>_vs_<opponent>/`

Contents:
- `context.md` - Description of the run, configuration, and key findings
- `*.csv` - Detailed move-by-move data (thinking, tokens, latency)
- `*.json` - Raw LLM responses

## Quick Reference

| Date | Model | Opponent | LLM_INTERVAL | Result | Key Finding |
|------|-------|----------|--------------|--------|-------------|
| 2026-02-02 04:07 | gemini-2.5-flash | RandomBiasedAI | 1 | Rate Limited (6 turns) | Interval=1 exhausts free tier instantly |
| 2026-02-02 04:14 | gemini-2.5-flash | RandomBiasedAI | 100 | Rate Limited (600 turns) | LLM destroyed enemy base but lost all workers; pyrrhic victory |
| 2026-02-02 05:34 | llama3.2:latest | RandomBiasedAI | 1 | Stopped (204 ticks) | **Fair game test**: Many JSON format errors, model struggles with prompt |
