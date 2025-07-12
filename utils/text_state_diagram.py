# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Text-based state machine visualization."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state_definitions import create_beach_volleyball_state_machine


def print_state_flow_diagram():
    """Print a text-based flow diagram of the state machine."""
    sm = create_beach_volleyball_state_machine()
    
    print("BEACH VOLLEYBALL STATE MACHINE FLOW")
    print("=" * 60)
    print()
    
    # Group states by phase
    phases = {
        "SERVE PHASE": ["s_serve_ready"],
        "RECEPTION PHASE": ["s_serve_in_play", "r_reception_perfect", "r_reception_good", "r_reception_error"],
        "SET PHASE": ["r_set_perfect", "r_set_good", "r_set_poor", "r_set_error"],
        "ATTACK PHASE": ["r_attack_kill", "r_attack_error", "r_attack_blocked", "r_attack_defended"],
        "DEFENSE PHASE": ["s_dig_perfect", "s_dig_good", "s_dig_error", "s_block_kill", "s_block_error"],
        "COUNTER ATTACK": ["s_set_perfect", "s_set_good", "s_set_poor", "s_set_error", "s_attack_kill", "s_attack_error"]
    }
    
    for phase, states in phases.items():
        print(f"\n{phase}:")
        print("-" * len(phase))
        
        for state in states:
            if state in sm.transitions:
                transitions = sm.get_next_states(state)
                print(f"\n  {state}:")
                for next_state, prob, action in transitions:
                    arrow = "  ├─→" if transitions.index((next_state, prob, action)) < len(transitions) - 1 else "  └─→"
                    terminal = " [TERMINAL]" if sm.is_terminal_state(next_state) else ""
                    print(f"{arrow} {next_state} ({prob:.1%}){terminal}")
            elif state in sm.terminal_states:
                from state_definitions import get_winning_team
                winner = get_winning_team(state)
                print(f"\n  {state}: [TERMINAL - {winner} team wins]")


def print_probability_summary():
    """Print a summary of key probability decisions."""
    sm = create_beach_volleyball_state_machine()
    
    print("\n\nKEY PROBABILITY DECISIONS")
    print("=" * 40)
    
    key_states = [
        ("s_serve_ready", "Serve Quality"),
        ("s_serve_in_play", "Reception Quality"), 
        ("r_set_perfect", "Attack from Perfect Set"),
        ("r_set_good", "Attack from Good Set"),
        ("r_attack_defended", "Dig Quality"),
        ("s_dig_perfect", "Counter-Set Quality")
    ]
    
    for state, description in key_states:
        if state in sm.transitions:
            print(f"\n{description} ({state}):")
            transitions = sm.get_next_states(state)
            for next_state, prob, action in transitions:
                outcome = next_state.split('_')[-1].upper()
                print(f"  {outcome:12} {prob:6.1%}  {'█' * int(float(prob) * 20)}")


def print_terminal_analysis():
    """Analyze terminal states and win conditions."""
    sm = create_beach_volleyball_state_machine()
    
    print("\n\nTERMINAL STATES ANALYSIS")
    print("=" * 35)
    
    serving_wins = []
    receiving_wins = []
    
    for terminal_state in sorted(sm.terminal_states):
        from state_definitions import get_winning_team
        winner = get_winning_team(terminal_state)
        if winner == 'serving':
            serving_wins.append(terminal_state)
        else:
            receiving_wins.append(terminal_state)
    
    print(f"\nSERVING TEAM WINS ({len(serving_wins)} ways):")
    for state in serving_wins:
        action = state.split('_')[1] if len(state.split('_')) > 1 else 'unknown'
        team_prefix = 'OWN' if state.startswith('s_') else 'OPP'
        print(f"  {state:20} - {team_prefix} {action.upper()}")
    
    print(f"\nRECEIVING TEAM WINS ({len(receiving_wins)} ways):")
    for state in receiving_wins:
        action = state.split('_')[1] if len(state.split('_')) > 1 else 'unknown'
        team_prefix = 'OWN' if state.startswith('r_') else 'OPP'
        print(f"  {state:20} - {team_prefix} {action.upper()}")
    
    print(f"\nBalance: {len(serving_wins)} vs {len(receiving_wins)} terminal states")


def print_state_machine_stats():
    """Print overall statistics about the state machine."""
    sm = create_beach_volleyball_state_machine()
    
    print("\n\nSTATE MACHINE STATISTICS")
    print("=" * 30)
    
    all_states = sm.get_all_states()
    serving_states = [s for s in all_states if s.startswith('s_')]
    receiving_states = [s for s in all_states if s.startswith('r_')]
    
    print(f"Total states:        {len(all_states)}")
    print(f"Continuation states: {len(sm.get_continuation_states())}")
    print(f"Terminal states:     {len(sm.terminal_states)}")
    print(f"Serving team states: {len(serving_states)}")
    print(f"Receiving states:    {len(receiving_states)}")
    
    # Calculate average branching factor
    total_transitions = sum(len(transitions) for transitions in sm.transitions.values())
    avg_branching = total_transitions / len(sm.transitions) if sm.transitions else 0
    print(f"Average branching:   {avg_branching:.2f}")
    
    print(f"\nProbability validation: {'✓ PASS' if sm.validate_probabilities() else '✗ FAIL'}")


if __name__ == "__main__":
    print_state_flow_diagram()
    print_probability_summary()
    print_terminal_analysis()
    print_state_machine_stats()