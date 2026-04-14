import random
import statistics

from system.decision_engine import risk_score


def run_simulation(
    economic, political, social,
    tech, env, legal,
    use_case,
    strategy,
    iterations=1000,
    variation=10
):
    """
    Monte Carlo Risk Simulation Engine
    """

    results = []

    for _ in range(iterations):

        # Random variation (bounded)
        e = max(0, min(100, economic + random.uniform(-variation, variation)))
        p = max(0, min(100, political + random.uniform(-variation, variation)))
        s = max(0, min(100, social + random.uniform(-variation, variation)))
        t = max(0, min(100, tech + random.uniform(-variation, variation)))
        en = max(0, min(100, env + random.uniform(-variation, variation)))
        l = max(0, min(100, legal + random.uniform(-variation, variation)))

        score, _, _ = risk_score(
            e, p, s, t, en, l,
            use_case,
            strategy
        )

        results.append(score)

    # ================= SUMMARY =================
    mean_score = round(statistics.mean(results), 2)
    min_score = round(min(results), 2)
    max_score = round(max(results), 2)
    std_dev = round(statistics.pstdev(results), 2)

    # ================= PROBABILITY =================
    high_risk_prob = round(
        sum(1 for r in results if r > 70) / iterations * 100, 2
    )

    return {
        "mean": mean_score,
        "min": min_score,
        "max": max_score,
        "std_dev": std_dev,
        "high_risk_probability": high_risk_prob,
        "distribution": results
    }
