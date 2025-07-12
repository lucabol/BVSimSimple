# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Multi-threaded elasticity analysis for beach volleyball state machine statistics."""

from typing import Dict, List, Tuple, Any
from decimal import Decimal
import copy
import concurrent.futures
import threading
import time
from state_definitions import create_beach_volleyball_state_machine
from match_simulator import simulate_match_points
from state_machine_builder import create_state_machine_from_teams
from elasticity_analysis import (
    extract_baseline_probabilities, 
    create_modified_state_machine, 
    convert_state_machine_to_template
)

# Thread-safe print lock
print_lock = threading.Lock()

def thread_safe_print(*args, **kwargs):
    """Thread-safe printing function."""
    with print_lock:
        print(*args, **kwargs)


def calculate_elasticity_threaded(args):
    """Thread-safe version of elasticity calculation."""
    stat_name, baseline_probs, improvement_pct, num_points, thread_id = args
    
    thread_safe_print(f"[Thread {thread_id}] Analyzing {stat_name}...")
    start_time = time.time()
    
    try:
        # Create baseline state machine
        baseline_sm = create_beach_volleyball_state_machine()
        baseline_template = convert_state_machine_to_template(baseline_sm)
        
        # Simulate baseline win rate
        baseline_win_rate = simulate_match_points(baseline_template, baseline_template, num_points)
        
        # Create improved state machine
        improvement_factor = 1.0 + improvement_pct
        improved_sm = create_modified_state_machine(baseline_probs, stat_name, improvement_factor)
        improved_template = convert_state_machine_to_template(improved_sm)
        
        # Simulate improved win rate (team with improvement vs baseline team)
        improved_win_rate = simulate_match_points(improved_template, baseline_template, num_points)
        
        # Calculate elasticity
        win_rate_change = improved_win_rate - baseline_win_rate
        elasticity = win_rate_change / (baseline_win_rate * improvement_pct)
        
        elapsed_time = time.time() - start_time
        thread_safe_print(f"[Thread {thread_id}] {stat_name} completed in {elapsed_time:.1f}s - Elasticity: {elasticity:+.3f}")
        
        return stat_name, elasticity, baseline_probs[stat_name]
        
    except Exception as e:
        thread_safe_print(f"[Thread {thread_id}] Error calculating elasticity for {stat_name}: {e}")
        return stat_name, 0.0, baseline_probs.get(stat_name, 0.0)


def run_threaded_elasticity_analysis(improvement_pct: float = 0.05, num_points: int = 100000, 
                                    max_workers: int = None) -> List[Tuple[str, float, float]]:
    """Run elasticity analysis using multiple threads."""
    
    print("Beach Volleyball Threaded Elasticity Analysis")
    print("=" * 60)
    print(f"Improvement: {improvement_pct*100:.1f}% per stat")
    print(f"Simulation points: {num_points:,} per stat")
    print(f"Max workers: {max_workers if max_workers else 'Auto-detect'}")
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
    
    # Filter to only stats we have baseline data for
    valid_stats = [stat for stat in stats_to_analyze if stat in baseline_probs]
    
    print(f"Analyzing {len(valid_stats)} stats in parallel...")
    print()
    
    # Prepare arguments for each thread
    thread_args = []
    for i, stat_name in enumerate(valid_stats):
        thread_args.append((stat_name, baseline_probs, improvement_pct, num_points, i+1))
    
    # Run analysis in parallel
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_stat = {executor.submit(calculate_elasticity_threaded, args): args[0] 
                         for args in thread_args}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_stat):
            stat_name = future_to_stat[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                thread_safe_print(f"Error with {stat_name}: {exc}")
                results.append((stat_name, 0.0, baseline_probs.get(stat_name, 0.0)))
    
    total_time = time.time() - start_time
    print()
    print(f"All analyses completed in {total_time:.1f} seconds")
    print()
    
    # Sort by elasticity (highest impact first)
    results.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Display results
    print("RESULTS SUMMARY")
    print("=" * 50)
    
    for stat_name, elasticity, baseline_value in results:
        print(f"{stat_name:30} | Baseline: {baseline_value:6.1%} | Elasticity: {elasticity:+6.3f}")
    
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


def run_multiple_threaded_trials(num_trials: int = 3, improvement_pct: float = 0.05, 
                                num_points: int = 100000, max_workers: int = None):
    """Run multiple trials to assess consistency with threading."""
    print("MULTI-TRIAL CONSISTENCY ANALYSIS (THREADED)")
    print("=" * 60)
    print(f"Running {num_trials} trials with {num_points:,} points each")
    print(f"Each trial uses threading for parallel stat analysis")
    print()
    
    all_results = []
    total_start_time = time.time()
    
    for trial in range(num_trials):
        print(f"TRIAL {trial + 1}")
        print("-" * 30)
        trial_results = run_threaded_elasticity_analysis(improvement_pct, num_points, max_workers)
        all_results.append(trial_results)
        print("\n")
    
    total_time = time.time() - total_start_time
    print(f"All {num_trials} trials completed in {total_time:.1f} seconds")
    print()
    
    # Analyze consistency across trials
    print("CONSISTENCY ANALYSIS ACROSS TRIALS")
    print("=" * 40)
    
    if len(all_results) > 1:
        # Get all stat names
        stat_names = [stat for stat, _, _ in all_results[0]]
        
        print(f"{'Stat Name':25} | {'Mean':>6} | {'StdDev':>6} | {'Range':>6} | {'Min':>6} | {'Max':>6}")
        print("-" * 75)
        
        for stat_name in stat_names:
            elasticities = []
            for trial_results in all_results:
                for name, elast, _ in trial_results:
                    if name == stat_name:
                        elasticities.append(elast)
                        break
            
            if elasticities and len(elasticities) > 1:
                mean_elast = sum(elasticities) / len(elasticities)
                variance = sum((x - mean_elast) ** 2 for x in elasticities) / len(elasticities)
                std_dev = variance ** 0.5
                min_elast = min(elasticities)
                max_elast = max(elasticities)
                range_elast = max_elast - min_elast
                
                print(f"{stat_name:25} | {mean_elast:+6.3f} | {std_dev:6.3f} | {range_elast:6.3f} | {min_elast:+6.3f} | {max_elast:+6.3f}")
            else:
                print(f"{stat_name:25} | {'N/A':>6} | {'N/A':>6} | {'N/A':>6} | {'N/A':>6} | {'N/A':>6}")
        
        print()
        print("Interpretation:")
        print("- Low StdDev/Range = More reliable metric")
        print("- High StdDev/Range = Results vary significantly between runs")


if __name__ == "__main__":
    import multiprocessing
    
    # Get optimal number of workers (number of CPU cores)
    optimal_workers = multiprocessing.cpu_count()
    print(f"Detected {optimal_workers} CPU cores")
    print()
    
    # Single high-confidence threaded run
    print("SINGLE HIGH-CONFIDENCE THREADED RUN")
    print("=" * 50)
    results = run_threaded_elasticity_analysis(
        improvement_pct=0.05, 
        num_points=50000,  # Reasonable size for testing
        max_workers=optimal_workers
    )
    
    print("\n\n")
    
    # Multi-trial consistency analysis (smaller for testing)
    run_multiple_threaded_trials(
        num_trials=2, 
        improvement_pct=0.05, 
        num_points=30000, 
        max_workers=optimal_workers
    )