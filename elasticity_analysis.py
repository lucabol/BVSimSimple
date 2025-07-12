# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Elasticity analysis for beach volleyball state machine statistics."""

from typing import Dict, List, Tuple, Any
from decimal import Decimal
import copy
from state_definitions import create_beach_volleyball_state_machine
from match_simulator import simulate_match_points
from state_machine_builder import create_state_machine_from_teams


def extract_baseline_probabilities() -> Dict[str, float]:
    """Extract baseline probabilities from the standard state machine."""
    sm = create_beach_volleyball_state_machine()
    baseline = {}
    
    # Extract key probabilities that trainers can influence
    for state, transitions in sm.transitions.items():
        for next_state, probability, action_type in transitions:
            # Create meaningful stat names
            if state == "s_serve_ready":
                if "ace" in next_state:
                    baseline["serve_ace_rate"] = float(probability)
                elif "error" in next_state:
                    baseline["serve_error_rate"] = float(probability)
                elif "in_play" in next_state:
                    baseline["serve_in_play_rate"] = float(probability)
            
            elif state == "s_serve_in_play":
                if "perfect" in next_state:
                    baseline["reception_perfect_rate"] = float(probability)
                elif "good" in next_state:
                    baseline["reception_good_rate"] = float(probability)
                elif "error" in next_state:
                    baseline["reception_error_rate"] = float(probability)
            
            elif state == "r_set_perfect" and "attack" in next_state:
                if "kill" in next_state:
                    baseline["attack_kill_from_perfect_set"] = float(probability)
                elif "error" in next_state:
                    baseline["attack_error_from_perfect_set"] = float(probability)
                elif "defended" in next_state:
                    baseline["attack_defended_from_perfect_set"] = float(probability)
            
            elif state == "r_set_good" and "attack" in next_state:
                if "kill" in next_state:
                    baseline["attack_kill_from_good_set"] = float(probability)
                elif "error" in next_state:
                    baseline["attack_error_from_good_set"] = float(probability)
            
            elif state == "r_attack_defended":
                if "perfect" in next_state:
                    baseline["dig_perfect_rate"] = float(probability)
                elif "good" in next_state:
                    baseline["dig_good_rate"] = float(probability)
                elif "error" in next_state:
                    baseline["dig_error_rate"] = float(probability)
            
            elif state == "r_attack_blocked":
                if "s_block_kill" in next_state:
                    baseline["block_kill_rate"] = float(probability)
                elif "s_block_error" in next_state:
                    baseline["block_error_rate"] = float(probability)
    
    return baseline


def create_modified_state_machine(baseline_probs: Dict[str, float], stat_name: str, improvement_factor: float):
    """Create a state machine with one stat improved."""
    sm = create_beach_volleyball_state_machine()
    
    # Create a copy of transitions
    modified_transitions = copy.deepcopy(sm.transitions)
    
    # Apply the improvement to the specific stat
    improvement_applied = False
    
    for state, transitions in modified_transitions.items():
        for i, (next_state, probability, action_type) in enumerate(transitions):
            should_modify = False
            
            # Map stat names to state transitions
            if stat_name == "serve_ace_rate" and state == "s_serve_ready" and "ace" in next_state:
                should_modify = True
            elif stat_name == "serve_error_rate" and state == "s_serve_ready" and "error" in next_state:
                should_modify = True
            elif stat_name == "reception_perfect_rate" and state == "s_serve_in_play" and "perfect" in next_state:
                should_modify = True
            elif stat_name == "reception_good_rate" and state == "s_serve_in_play" and "good" in next_state:
                should_modify = True
            elif stat_name == "attack_kill_from_perfect_set" and state == "r_set_perfect" and "kill" in next_state:
                should_modify = True
            elif stat_name == "attack_kill_from_good_set" and state == "r_set_good" and "kill" in next_state:
                should_modify = True
            elif stat_name == "dig_perfect_rate" and state == "r_attack_defended" and "perfect" in next_state:
                should_modify = True
            elif stat_name == "block_kill_rate" and state == "r_attack_blocked" and "s_block_kill" in next_state:
                should_modify = True
            
            if should_modify:
                # Calculate the improvement
                old_prob = float(probability)
                improvement_amount = old_prob * (improvement_factor - 1.0)  # Absolute improvement
                new_prob = old_prob + improvement_amount
                
                # Ensure new probability doesn't exceed 1.0
                if new_prob > 1.0:
                    new_prob = 1.0
                    improvement_amount = new_prob - old_prob
                
                # Calculate how much to reduce from other probabilities
                other_transitions = [(j, ns, p, at) for j, (ns, p, at) in enumerate(transitions) if j != i]
                total_other_prob = sum(float(p) for _, _, p, _ in other_transitions)
                
                if total_other_prob > 0 and improvement_amount > 0:
                    # Reduce other probabilities proportionally
                    reduction_factor = improvement_amount / total_other_prob
                    
                    # Update all transitions for this state
                    new_transitions = []
                    for j, (ns, p, at) in enumerate(transitions):
                        if j == i:
                            new_transitions.append((ns, Decimal(str(new_prob)), at))
                        else:
                            reduced_prob = float(p) * (1.0 - reduction_factor)
                            new_transitions.append((ns, Decimal(str(reduced_prob)), at))
                    
                    # Verify probabilities sum to 1.0
                    total_check = sum(float(p) for _, p, _ in new_transitions)
                    if abs(total_check - 1.0) > 0.001:
                        # Renormalize if needed
                        new_transitions = [(ns, Decimal(str(float(p) / total_check)), at) 
                                         for ns, p, at in new_transitions]
                    
                    modified_transitions[state] = new_transitions
                    improvement_applied = True
                break
    
    if not improvement_applied:
        raise ValueError(f"Could not find transition for stat: {stat_name}")
    
    # Create new state machine with modified transitions
    from state_machine import RallyStateMachine
    return RallyStateMachine(
        transitions=modified_transitions,
        terminal_states=sm.terminal_states,
        initial_state=sm.initial_state
    )


def convert_state_machine_to_template(sm):
    """Convert state machine to template format for simulate_match_points."""
    template = {}
    for state, transitions in sm.transitions.items():
        if not sm.is_terminal_state(state):
            template[state] = [(next_state, probability) for next_state, probability, _ in transitions]
    return template


def calculate_elasticity(stat_name: str, baseline_probs: Dict[str, float], 
                        improvement_pct: float = 0.05, num_points: int = 10000) -> float:
    """Calculate elasticity for a specific stat."""
    
    print(f"Analyzing {stat_name}...")
    
    # Create baseline state machine
    baseline_sm = create_beach_volleyball_state_machine()
    baseline_template = convert_state_machine_to_template(baseline_sm)
    
    # Simulate baseline win rate
    baseline_win_rate = simulate_match_points(baseline_template, baseline_template, num_points)
    
    # Create improved state machine
    improvement_factor = 1.0 + improvement_pct
    try:
        improved_sm = create_modified_state_machine(baseline_probs, stat_name, improvement_factor)
        improved_template = convert_state_machine_to_template(improved_sm)
        
        # Simulate improved win rate (team with improvement vs baseline team)
        improved_win_rate = simulate_match_points(improved_template, baseline_template, num_points)
        
        # Calculate elasticity
        win_rate_change = improved_win_rate - baseline_win_rate
        elasticity = win_rate_change / (baseline_win_rate * improvement_pct)
        
        return elasticity
        
    except Exception as e:
        print(f"Error calculating elasticity for {stat_name}: {e}")
        return 0.0


def run_elasticity_analysis(improvement_pct: float = 0.05, num_points: int = 10000) -> List[Tuple[str, float, float]]:
    """Run complete elasticity analysis for all key stats."""
    
    print("Beach Volleyball Elasticity Analysis")
    print("=" * 50)
    print(f"Improvement: {improvement_pct*100:.1f}% per stat")
    print(f"Simulation points: {num_points:,}")
    print()
    
    # Get baseline probabilities
    baseline_probs = extract_baseline_probabilities()
    
    # Stats to analyze (trainable skills)
    stats_to_analyze = [
        "serve_ace_rate",
        "reception_perfect_rate", 
        "reception_good_rate",
        "attack_kill_from_perfect_set",
        "attack_kill_from_good_set",
        "dig_perfect_rate",
        "block_kill_rate"
    ]
    
    results = []
    
    for stat_name in stats_to_analyze:
        if stat_name in baseline_probs:
            baseline_value = baseline_probs[stat_name]
            elasticity = calculate_elasticity(stat_name, baseline_probs, improvement_pct, num_points)
            
            results.append((stat_name, elasticity, baseline_value))
            
            print(f"{stat_name:30} | Baseline: {baseline_value:6.1%} | Elasticity: {elasticity:+6.3f}")
        else:
            print(f"Warning: {stat_name} not found in baseline probabilities")
    
    # Sort by elasticity (highest impact first)
    results.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print("\n" + "=" * 50)
    print("TRAINING PRIORITY RANKING")
    print("=" * 50)
    
    for i, (stat_name, elasticity, baseline) in enumerate(results, 1):
        impact_desc = "High Impact" if abs(elasticity) > 1.0 else "Medium Impact" if abs(elasticity) > 0.5 else "Low Impact"
        print(f"{i}. {stat_name:25} | {elasticity:+6.3f} | {impact_desc}")
    
    print(f"\nInterpretation: Elasticity shows how much win rate changes per 1% stat improvement")
    print(f"Example: Elasticity of +2.0 means 1% stat improvement → +2% win rate improvement")
    
    # Training insights
    print("\n" + "=" * 50)
    print("TRAINING INSIGHTS FOR COACHES")
    print("=" * 50)
    
    positive_impacts = [(name, elast, base) for name, elast, base in results if elast > 0]
    negative_impacts = [(name, elast, base) for name, elast, base in results if elast < 0]
    
    if positive_impacts:
        print("🟢 SKILLS TO IMPROVE (Positive Impact):")
        for name, elasticity, baseline in positive_impacts:
            readable_name = name.replace("_", " ").title()
            print(f"   {readable_name}: {elasticity:+.3f} elasticity")
            
            # Calculate practical examples
            example_improvement = baseline * 0.10  # 10% relative improvement
            win_rate_change = elasticity * 0.10 * 50  # Assuming 50% baseline win rate
            print(f"   → Improving from {baseline:.1%} to {baseline + example_improvement:.1%} = {win_rate_change:+.1f}% win rate change")
            print()
    
    if negative_impacts:
        print("🔴 UNEXPECTED NEGATIVE IMPACTS:")
        for name, elasticity, baseline in negative_impacts:
            readable_name = name.replace("_", " ").title()
            print(f"   {readable_name}: {elasticity:+.3f} elasticity")
            print(f"   → This suggests improving this stat alone may hurt win rate")
            print(f"   → Likely due to opportunity cost or system interactions")
            print()
    
    # Top recommendation
    if results:
        top_stat = results[0]
        print("🎯 TOP TRAINING PRIORITY:")
        readable_name = top_stat[0].replace("_", " ").title()
        print(f"   Focus on: {readable_name}")
        print(f"   Impact: {abs(top_stat[1]):.3f} elasticity")
        if top_stat[1] > 0:
            print(f"   Strategy: Increase this skill for direct win rate improvement")
        else:
            print(f"   Strategy: This has highest impact but negative - investigate why")
    
    return results


def test_consistency(num_trials=3, num_points=50000):
    """Test consistency of elasticity results across multiple trials."""
    print("TESTING RESULT CONSISTENCY")
    print("=" * 50)
    print(f"Running {num_trials} trials with {num_points:,} points each")
    print()
    
    all_results = []
    for trial in range(num_trials):
        print(f"Trial {trial + 1}:")
        results = run_elasticity_analysis(improvement_pct=0.05, num_points=num_points)
        all_results.append(results)
        print()
    
    # Analyze consistency
    print("CONSISTENCY ANALYSIS")
    print("=" * 30)
    
    if len(all_results) > 1:
        # Get all stat names
        stat_names = [stat for stat, _, _ in all_results[0]]
        
        for stat_name in stat_names:
            elasticities = []
            for trial_results in all_results:
                for name, elast, _ in trial_results:
                    if name == stat_name:
                        elasticities.append(elast)
                        break
            
            if elasticities:
                mean_elast = sum(elasticities) / len(elasticities)
                min_elast = min(elasticities)
                max_elast = max(elasticities)
                range_elast = max_elast - min_elast
                
                print(f"{stat_name:25} | Mean: {mean_elast:+.3f} | Range: {range_elast:.3f} | Values: {elasticities}")


if __name__ == "__main__":
    # Single run with high confidence
    print("SINGLE HIGH-CONFIDENCE RUN")
    print("=" * 50)
    results = run_elasticity_analysis(improvement_pct=0.05, num_points=100000)  # Very high for stable results
    
    print("\n\n")
    
    # Consistency test with multiple smaller runs
    test_consistency(num_trials=3, num_points=30000)