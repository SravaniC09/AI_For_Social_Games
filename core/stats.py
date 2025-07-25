import random

def generate_sample_policy_deltas():
    """Generates a sample set of random stat deltas for a single policy option."""
    return {
        "treasury": random.randint(-10, 5),
        "stability": random.randint(-5, 5),
        "popularity": random.randint(-5, 5),
        "army": random.randint(-5, 5),
    }

def apple_policy(allocations, state, policy_base_effects_list):
    # allocations: a list of floats representing the proportion of resources for each policy
    # policy_base_effects_list: a list of dicts, where each dict is the base effects for a policy option

    num_policy_options = len(allocations)

    cumulative_deltas_float = {
        "treasury": 0.0,
        "stability": 0.0,
        "popularity": 0.0,
        "army": 0.0,
    }

    for i in range(num_policy_options):
        if allocations[i] > 0 and i < len(policy_base_effects_list):
            base_policy_option_deltas = policy_base_effects_list[i] # use pre-generated effects

            for stat, base_delta in base_policy_option_deltas.items():
                cumulative_deltas_float[stat] += allocations[i] * base_delta

        # Convert cumulative deltas to integers for application
        final_deltas = {stat: int(round(delta)) for stat, delta in cumulative_deltas_float()}

        for stat, delta in final_deltas.items():
            old = getattr(state, stat)
            new = max(0, min(100, old + delta)) # Clamp between 0 and 100
            setattr(state, stat, new)

        return final_deltas
    
def print_stats(state, deltas=None):
    from rich import print as rprint
    from rich.panel import Panel

    def fmt(stat, value, delta=None):
        if delta is None:
            return f"[bold]{stat.title()}[/]: {value}"
        color = "green" if delta > 0 else "red" if delta < 0 else "white"
        return f"[bold]{stat.title()}[/]: {value} ([{color}]{delta:+}[/])"
    
    rprint(Panel.fit(
        "\n".join([
            fmt("treasury", state.treasury, deltas.get("treasury") if deltas else None),
            fmt("stability", state.stability, deltas.get("stability") if deltas else None),
            fmt("popularity", state.popularity, deltas.get("popularity") if deltas else None),
            fmt("army", state.army, deltas.get("army") if deltas else None),
        ]),
        title="Current Kingdom Stats",
        border_style="blue"
    ))
