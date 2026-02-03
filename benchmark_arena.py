#!/usr/bin/env python3
"""
MicroRTS LLM Benchmark Arena v1.0

Runs benchmarks against fixed reference AIs to produce comparable scores.
New LLMs can be measured at any time and compared to historical results.

Scoring: Based purely on performance against reference AIs (anchors).
- RandomBiasedAI (easy): 40 points max
- WorkerRush (hard): 60 points max
- Total: 0-100 scale

Usage:
    python3 benchmark_arena.py [--games N]

Environment Variables:
    GEMINI_API_KEY - Required for Gemini models
    OLLAMA_MODEL - Model for ai.abstraction.ollama (default: llama3.1:8b)
    OLLAMA_MODEL_P2 - Model for ai.abstraction.ollama2 (default: qwen3:4b)
"""

import subprocess
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuration
CONFIG_FILE = "resources/config.properties"
RESULTS_DIR = "benchmark_results"
MAX_CYCLES = 3000  # Reduced for faster games
MAP = "maps/8x8/basesWorkers8x8.xml"
GAME_TIMEOUT = 900  # 15 minutes per game

# Reference AI anchors with scoring weights
# These are FIXED - they provide the stable baseline for all comparisons
ANCHORS = {
    "ai.RandomBiasedAI": {
        "name": "RandomBiasedAI",
        "weight": 40,  # Easy anchor - 40 points max
        "difficulty": "easy"
    },
    "ai.abstraction.WorkerRush": {
        "name": "WorkerRush",
        "weight": 60,  # Hard anchor - 60 points max
        "difficulty": "hard"
    },
}

# LLM contestants
LLMS = {
    "ai.abstraction.ollama": {
        "name": "ollama",
        "display": None,
        "env": {"OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama3.1:8b")}
    },
    "ai.abstraction.ollama2": {
        "name": "ollama2",
        "display": None,
        "env": {"OLLAMA_MODEL_P2": os.environ.get("OLLAMA_MODEL_P2", "qwen3:4b")}
    },
    "ai.abstraction.LLM_Gemini": {
        "name": "gemini",
        "display": "gemini-2.5-flash",
        "env": {"GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", "")}
    },
}

# Set display names from env
LLMS["ai.abstraction.ollama"]["display"] = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
LLMS["ai.abstraction.ollama2"]["display"] = os.environ.get("OLLAMA_MODEL_P2", "qwen3:4b")


def update_config(ai1, ai2):
    """Update config.properties with AI settings."""
    with open(CONFIG_FILE, 'r') as f:
        content = f.read()

    content = re.sub(r'^AI1=.*$', f'AI1={ai1}', content, flags=re.MULTILINE)
    content = re.sub(r'^AI2=.*$', f'AI2={ai2}', content, flags=re.MULTILINE)
    content = re.sub(r'^max_cycles=.*$', f'max_cycles={MAX_CYCLES}', content, flags=re.MULTILINE)
    content = re.sub(r'^headless=.*$', 'headless=true', content, flags=re.MULTILINE)

    with open(CONFIG_FILE, 'w') as f:
        f.write(content)


def run_game(ai1, ai2):
    """Run a single game and return result."""
    update_config(ai1, ai2)

    env = os.environ.copy()
    if ai1 in LLMS:
        env.update(LLMS[ai1]["env"])
    if ai2 in LLMS:
        env.update(LLMS[ai2]["env"])

    ai1_name = LLMS.get(ai1, {}).get("display", ai1.split(".")[-1])
    ai2_name = LLMS.get(ai2, {}).get("display", ai2.split(".")[-1])

    print(f"  {ai1_name} vs {ai2_name}...", end=" ", flush=True)

    try:
        result = subprocess.run(
            ["java", "-cp", "lib/*:bin", "rts.MicroRTS", "-f", CONFIG_FILE],
            capture_output=True,
            text=True,
            timeout=GAME_TIMEOUT,
            env=env
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return {"result": "timeout", "ticks": MAX_CYCLES}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"result": "error", "ticks": 0, "error": str(e)}

    # Parse result
    winner = None
    ticks = MAX_CYCLES

    winner_match = re.search(r'WINNER:\s*(-?\d+)', output)
    if winner_match:
        winner = int(winner_match.group(1))

    tick_match = re.search(r'FINAL_TICK:\s*(\d+)', output)
    if tick_match:
        ticks = int(tick_match.group(1))

    if winner is None:
        if "Player 0 wins" in output:
            winner = 0
        elif "Player 1 wins" in output:
            winner = 1

    if winner == 0:
        print(f"WIN ({ticks} ticks)")
        return {"result": "win", "ticks": ticks}
    elif winner == 1:
        print(f"LOSS ({ticks} ticks)")
        return {"result": "loss", "ticks": ticks}
    else:
        print(f"DRAW ({ticks} ticks)")
        return {"result": "draw", "ticks": ticks}


def calculate_game_score(result, ticks):
    """
    Calculate score for a single game against a reference AI.

    Returns a value 0.0 - 1.0:
      Win:  1.0 + efficiency bonus (max 1.2)
      Draw: 0.5
      Loss: 0.0
      Timeout: 0.0
    """
    if result == "win":
        base = 1.0
        # Efficiency bonus for fast wins
        if ticks < MAX_CYCLES * 0.5:
            bonus = 0.2
        elif ticks < MAX_CYCLES * 0.75:
            bonus = 0.1
        else:
            bonus = 0.0
        return min(1.2, base + bonus)
    elif result == "draw":
        return 0.5
    else:  # loss, timeout, error
        return 0.0


def calculate_benchmark_score(llm_results):
    """
    Calculate the final benchmark score (0-100) for an LLM.

    Score = Sum of (game_score × anchor_weight) for each anchor

    This score is COMPARABLE across tournaments because it's based
    only on performance against fixed reference AIs.
    """
    total_score = 0.0

    for anchor_class, anchor_info in ANCHORS.items():
        if anchor_class in llm_results:
            games = llm_results[anchor_class]
            if games:
                # Average score across games against this anchor
                avg_score = sum(
                    calculate_game_score(g["result"], g["ticks"])
                    for g in games
                ) / len(games)

                # Weight by anchor difficulty
                weighted = avg_score * anchor_info["weight"]
                total_score += weighted

    return round(total_score, 1)


def run_tournament(games_per_pair=1):
    """Run benchmark tournament."""
    print("=" * 60)
    print("MicroRTS LLM Benchmark v1.0")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Map: {MAP}")
    print(f"Max Cycles: {MAX_CYCLES}")
    print(f"Games per matchup: {games_per_pair}")
    print()
    print("Scoring: Reference-based (comparable across tournaments)")
    print(f"  - RandomBiasedAI (easy): {ANCHORS['ai.RandomBiasedAI']['weight']} pts max")
    print(f"  - WorkerRush (hard): {ANCHORS['ai.abstraction.WorkerRush']['weight']} pts max")
    print()

    # Results storage
    all_results = {}
    benchmark_scores = {}

    # Phase 1: Each LLM vs each Reference AI
    print("BENCHMARK GAMES (vs Reference AIs)")
    print("-" * 40)

    for llm_class, llm_info in LLMS.items():
        llm_name = llm_info["display"]
        all_results[llm_name] = {"reference_games": {}, "llm_games": []}

        print(f"\n{llm_name}:")

        for anchor_class, anchor_info in ANCHORS.items():
            all_results[llm_name]["reference_games"][anchor_class] = []

            for game_num in range(games_per_pair):
                result = run_game(llm_class, anchor_class)
                result["game_num"] = game_num + 1
                result["opponent"] = anchor_info["name"]
                all_results[llm_name]["reference_games"][anchor_class].append(result)

        # Calculate benchmark score for this LLM
        benchmark_scores[llm_name] = calculate_benchmark_score(
            all_results[llm_name]["reference_games"]
        )

    print()

    # Phase 2: LLM vs LLM (supplementary, not part of benchmark score)
    print("LLM vs LLM GAMES (supplementary)")
    print("-" * 40)

    llm_list = list(LLMS.keys())
    h2h_results = []

    for i, llm1_class in enumerate(llm_list):
        for llm2_class in llm_list[i+1:]:
            llm1_name = LLMS[llm1_class]["display"]
            llm2_name = LLMS[llm2_class]["display"]

            for game_num in range(games_per_pair):
                result = run_game(llm1_class, llm2_class)
                result["player0"] = llm1_name
                result["player1"] = llm2_name
                h2h_results.append(result)

    print()

    # Display Results
    print("=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print()

    # Sort by score
    sorted_scores = sorted(benchmark_scores.items(), key=lambda x: x[1], reverse=True)

    print("BENCHMARK SCORES (0-100, comparable across tournaments)")
    print("-" * 50)
    print(f"{'Rank':<6}{'Model':<25}{'Score':<10}{'Grade'}")
    print("-" * 50)

    for rank, (llm_name, score) in enumerate(sorted_scores, 1):
        # Assign grade
        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 40:
            grade = "D"
        else:
            grade = "F"

        print(f"{rank:<6}{llm_name:<25}{score:<10}{grade}")

    print()

    # Detailed breakdown
    print("DETAILED BREAKDOWN")
    print("-" * 50)

    for llm_name, results in all_results.items():
        print(f"\n{llm_name}:")
        for anchor_class, games in results["reference_games"].items():
            anchor_name = ANCHORS[anchor_class]["name"]
            weight = ANCHORS[anchor_class]["weight"]

            for g in games:
                result_str = g["result"].upper()
                ticks = g["ticks"]
                game_score = calculate_game_score(g["result"], g["ticks"])
                weighted = game_score * weight
                print(f"  vs {anchor_name}: {result_str} ({ticks} ticks) → {game_score:.2f} × {weight} = {weighted:.1f} pts")

    print()

    # Head-to-head summary
    print("HEAD-TO-HEAD SUMMARY (not part of benchmark score)")
    print("-" * 50)

    wins = {LLMS[c]["display"]: 0 for c in LLMS}
    losses = {LLMS[c]["display"]: 0 for c in LLMS}

    for h in h2h_results:
        if h["result"] == "win":
            wins[h["player0"]] += 1
            losses[h["player1"]] += 1
        elif h["result"] == "loss":
            losses[h["player0"]] += 1
            wins[h["player1"]] += 1

    for llm_name in wins:
        print(f"  {llm_name}: {wins[llm_name]}W - {losses[llm_name]}L")

    print()

    # Save results
    Path(RESULTS_DIR).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')

    results_file = f"{RESULTS_DIR}/benchmark_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "version": "1.0",
            "date": datetime.now().isoformat(),
            "config": {
                "map": MAP,
                "max_cycles": MAX_CYCLES,
                "games_per_matchup": games_per_pair
            },
            "benchmark_scores": benchmark_scores,
            "detailed_results": all_results,
            "head_to_head": h2h_results
        }, f, indent=2)

    print(f"Results saved to {results_file}")

    # Also append to historical leaderboard
    leaderboard_file = f"{RESULTS_DIR}/leaderboard.json"
    if Path(leaderboard_file).exists():
        with open(leaderboard_file, 'r') as f:
            leaderboard = json.load(f)
    else:
        leaderboard = {"entries": []}

    for llm_name, score in benchmark_scores.items():
        leaderboard["entries"].append({
            "model": llm_name,
            "score": score,
            "date": datetime.now().isoformat(),
            "map": MAP,
            "games_per_matchup": games_per_pair
        })

    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f, indent=2)

    print(f"Leaderboard updated: {leaderboard_file}")

    return benchmark_scores


if __name__ == "__main__":
    games = 1
    if len(sys.argv) > 1 and sys.argv[1] == "--games":
        games = int(sys.argv[2])

    run_tournament(games_per_pair=games)
