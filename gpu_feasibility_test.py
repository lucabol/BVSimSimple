# /// script
# requires-python = ">=3.9"
# dependencies = ["numpy"]
# ///
"""Test feasibility of GPU acceleration for beach volleyball simulation."""

import numpy as np
import time
from state_definitions import create_beach_volleyball_state_machine

def test_gpu_feasibility():
    """Test if we can vectorize the simulation for GPU acceleration."""
    
    print("GPU Acceleration Feasibility Test")
    print("=" * 40)
    
    # Check if we have the right structure for vectorization
    sm = create_beach_volleyball_state_machine()
    
    print(f"Total states: {len(sm.get_all_states())}")
    print(f"Continuation states: {len(sm.get_continuation_states())}")
    print(f"Terminal states: {len(sm.terminal_states)}")
    
    # Create state-to-index mapping
    all_states = sorted(sm.get_all_states())
    state_to_idx = {state: i for i, state in enumerate(all_states)}
    
    print(f"\nState mapping created: {len(state_to_idx)} states")
    
    # Create transition probability matrix
    num_states = len(all_states)
    transition_matrix = np.zeros((num_states, num_states))
    
    for state, transitions in sm.transitions.items():
        from_idx = state_to_idx[state]
        for next_state, probability, _ in transitions:
            to_idx = state_to_idx[next_state]
            transition_matrix[from_idx, to_idx] = float(probability)
    
    print(f"Transition matrix shape: {transition_matrix.shape}")
    print(f"Non-zero transitions: {np.count_nonzero(transition_matrix)}")
    
    # Test vectorized simulation concept
    print(f"\nTesting vectorized simulation concept...")
    
    # Simulate concept: batch rally simulation
    batch_size = 10000
    max_steps = 50
    
    # Start all rallies at initial state
    initial_state_idx = state_to_idx[sm.initial_state]
    current_states = np.full(batch_size, initial_state_idx, dtype=np.int32)
    
    # Track which rallies are still active
    active_rallies = np.ones(batch_size, dtype=bool)
    rally_lengths = np.zeros(batch_size, dtype=np.int32)
    
    start_time = time.time()
    
    for step in range(max_steps):
        if not np.any(active_rallies):
            break
            
        # Get transition probabilities for current states
        active_indices = np.where(active_rallies)[0]
        
        for i in active_indices:
            current_state = current_states[i]
            state_name = all_states[current_state]
            
            # Check if terminal
            if sm.is_terminal_state(state_name):
                active_rallies[i] = False
                continue
            
            # Get probabilities for this state
            probs = transition_matrix[current_state]
            
            if np.sum(probs) > 0:
                # Sample next state
                next_state_idx = np.random.choice(num_states, p=probs/np.sum(probs))
                current_states[i] = next_state_idx
                rally_lengths[i] += 1
    
    elapsed_time = time.time() - start_time
    
    print(f"Vectorized simulation completed in {elapsed_time:.3f} seconds")
    print(f"Simulated {batch_size} rallies")
    print(f"Average rally length: {np.mean(rally_lengths):.1f} steps")
    print(f"Completed rallies: {np.sum(~active_rallies)}")
    
    # Calculate theoretical speedup potential
    print(f"\nSpeedup Analysis:")
    print(f"Current threading: ~28 seconds for 350k simulations")
    print(f"This test: {elapsed_time:.3f} seconds for 10k simulations")
    estimated_time_350k = (elapsed_time / batch_size) * 350000
    estimated_speedup = 28 / estimated_time_350k
    print(f"Estimated time for 350k: {estimated_time_350k:.1f} seconds")
    print(f"Potential speedup: {estimated_speedup:.1f}x")
    
    # GPU package availability
    print(f"\nGPU Package Recommendations:")
    try:
        import cupy
        print("✅ CuPy available - Can use NVIDIA GPU acceleration")
    except ImportError:
        print("❌ CuPy not available - Install with: pip install cupy-cuda12x")
    
    try:
        import jax
        print("✅ JAX available - Can use XLA compilation (CPU/GPU/TPU)")
    except ImportError:
        print("❌ JAX not available - Install with: pip install jax jaxlib")
    
    try:
        import torch
        print("✅ PyTorch available - Can use GPU tensors")
        if torch.cuda.is_available():
            print(f"   - CUDA devices: {torch.cuda.device_count()}")
        else:
            print("   - CUDA not available")
    except ImportError:
        print("❌ PyTorch not available - Install with: pip install torch")
    
    return transition_matrix, state_to_idx, all_states


def create_optimized_gpu_simulation():
    """Outline for a full GPU-optimized implementation."""
    
    print(f"\nOptimized GPU Implementation Strategy:")
    print("=" * 50)
    
    print("1. State Machine Conversion:")
    print("   - Convert to transition probability matrix")
    print("   - Map states to integer indices")
    print("   - Pre-compute all transition probabilities")
    
    print("2. Vectorized Rally Simulation:")
    print("   - Batch 10k+ rallies simultaneously")
    print("   - Use GPU random number generation")
    print("   - Process all active rallies in parallel")
    
    print("3. Elasticity Calculation:")
    print("   - Run baseline vs improved simulations")
    print("   - Calculate win rates from batch results")
    print("   - All 7 stats could run in <1 second")
    
    print("4. Expected Performance:")
    print("   - Current: 28 seconds (CPU threading)")
    print("   - GPU optimized: 0.5-2 seconds")
    print("   - Speedup: 15-50x faster")
    
    print("5. Implementation Options:")
    print("   a) CuPy: Easiest migration (replace np with cp)")
    print("   b) JAX: Best performance + automatic compilation")
    print("   c) PyTorch: Good for complex probability distributions")


if __name__ == "__main__":
    transition_matrix, state_mapping, states = test_gpu_feasibility()
    create_optimized_gpu_simulation()