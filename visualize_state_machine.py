# /// script
# requires-python = ">=3.9"
# dependencies = ["graphviz"]
# ///
"""Visualization tools for the beach volleyball state machine."""

import graphviz
from state_definitions import create_beach_volleyball_state_machine
from state_machine import RallyStateMachine


def create_state_machine_graph(sm: RallyStateMachine, filename: str = "bv_state_machine") -> None:
    """Create a Graphviz visualization of the state machine."""
    
    dot = graphviz.Digraph(comment='Beach Volleyball State Machine')
    dot.attr(rankdir='TB', size='20,20')
    dot.attr('node', shape='box', style='rounded,filled')
    
    # Color scheme for different teams and states
    serving_color = '#E3F2FD'  # Light blue
    receiving_color = '#E8F5E8'  # Light green
    terminal_color = '#FFEBEE'  # Light red
    
    # Add nodes
    for state in sm.get_all_states():
        if sm.is_terminal_state(state):
            dot.node(state, state, fillcolor=terminal_color, shape='doublecircle')
        elif state.startswith('s_'):
            dot.node(state, state, fillcolor=serving_color)
        elif state.startswith('r_'):
            dot.node(state, state, fillcolor=receiving_color)
        else:
            dot.node(state, state)
    
    # Add edges with probabilities
    for state, transitions in sm.transitions.items():
        for next_state, probability, action_type in transitions:
            # Format probability as percentage
            prob_str = f"{float(probability):.1%}"
            label = f"{prob_str}\\n{action_type.value}"
            
            # Color edges by action type
            edge_colors = {
                'serve': 'blue',
                'reception': 'green',
                'set': 'orange',
                'attack': 'red',
                'dig': 'purple',
                'block': 'brown',
                'transition': 'gray'
            }
            color = edge_colors.get(action_type.value, 'black')
            
            dot.edge(state, next_state, label=label, color=color)
    
    # Render the graph
    dot.render(filename, format='png', cleanup=True)
    dot.render(filename, format='svg', cleanup=True)
    print(f"State machine graph saved as {filename}.png and {filename}.svg")


def create_simplified_graph(sm: RallyStateMachine, filename: str = "bv_state_machine_simple") -> None:
    """Create a simplified visualization showing only main flow."""
    
    # Key states to include in simplified view
    key_states = {
        's_serve_ready', 's_serve_ace', 's_serve_error', 's_serve_in_play',
        'r_reception_perfect', 'r_reception_good', 'r_reception_error',
        'r_set_perfect', 'r_set_good', 'r_set_error',
        'r_attack_kill', 'r_attack_error', 'r_attack_defended',
        's_dig_perfect', 's_dig_good', 's_dig_error',
        's_set_perfect', 's_set_good', 's_attack_kill', 's_attack_error'
    }
    
    dot = graphviz.Digraph(comment='Beach Volleyball State Machine (Simplified)')
    dot.attr(rankdir='TB', size='16,12')
    dot.attr('node', shape='box', style='rounded,filled')
    
    # Add only key nodes
    for state in key_states:
        if state in sm.get_all_states():
            if sm.is_terminal_state(state):
                dot.node(state, state, fillcolor='#FFEBEE', shape='doublecircle')
            elif state.startswith('s_'):
                dot.node(state, state, fillcolor='#E3F2FD')
            elif state.startswith('r_'):
                dot.node(state, state, fillcolor='#E8F5E8')
    
    # Add edges between key states only
    for state in key_states:
        if state in sm.transitions:
            for next_state, probability, action_type in sm.transitions[state]:
                if next_state in key_states:
                    prob_str = f"{float(probability):.1%}"
                    dot.edge(state, next_state, label=prob_str)
    
    dot.render(filename, format='png', cleanup=True)
    print(f"Simplified state machine graph saved as {filename}.png")


def analyze_probabilities(sm: RallyStateMachine) -> None:
    """Analyze and print probability statistics."""
    
    print("Probability Analysis:")
    print("=" * 50)
    
    # Analyze serving outcomes
    serve_transitions = sm.get_next_states('s_serve_ready')
    print("Serve outcomes:")
    for next_state, prob, _ in serve_transitions:
        print(f"  {next_state}: {float(prob):.1%}")
    
    # Analyze reception quality distribution
    if 's_serve_in_play' in sm.transitions:
        reception_transitions = sm.get_next_states('s_serve_in_play')
        print("\nReception quality from serve:")
        for next_state, prob, _ in reception_transitions:
            print(f"  {next_state}: {float(prob):.1%}")
    
    # Analyze attack success from perfect sets
    perfect_set_states = ['r_set_perfect', 's_set_perfect']
    for set_state in perfect_set_states:
        if set_state in sm.transitions:
            attack_transitions = sm.get_next_states(set_state)
            print(f"\nAttack outcomes from {set_state}:")
            for next_state, prob, _ in attack_transitions:
                print(f"  {next_state}: {float(prob):.1%}")
    
    # Count terminal states by winner
    serving_wins = 0
    receiving_wins = 0
    for terminal_state in sm.terminal_states:
        from state_definitions import get_winning_team
        winner = get_winning_team(terminal_state)
        if winner == 'serving':
            serving_wins += 1
        else:
            receiving_wins += 1
    
    print(f"\nTerminal states: {len(sm.terminal_states)} total")
    print(f"  Serving team wins: {serving_wins}")
    print(f"  Receiving team wins: {receiving_wins}")


def create_probability_heatmap() -> None:
    """Create a text-based probability heatmap for key transitions."""
    sm = create_beach_volleyball_state_machine()
    
    print("\nProbability Heatmap (Key Transitions):")
    print("=" * 60)
    
    # Key transition categories
    categories = {
        "Serve Quality": [('s_serve_ready', ['s_serve_ace', 's_serve_error', 's_serve_in_play'])],
        "Reception Quality": [('s_serve_in_play', ['r_reception_perfect', 'r_reception_good', 'r_reception_error'])],
        "Attack Success (Perfect Set)": [('r_set_perfect', ['r_attack_kill', 'r_attack_error', 'r_attack_defended'])],
        "Attack Success (Good Set)": [('r_set_good', ['r_attack_kill', 'r_attack_error', 'r_attack_defended'])]
    }
    
    for category, transitions in categories.items():
        print(f"\n{category}:")
        for from_state, to_states in transitions:
            if from_state in sm.transitions:
                state_transitions = sm.get_next_states(from_state)
                for next_state, prob, _ in state_transitions:
                    if next_state in to_states:
                        # Create visual bar
                        bar_length = int(float(prob) * 20)  # Scale to 20 chars
                        bar = "█" * bar_length + "░" * (20 - bar_length)
                        print(f"  {next_state:20} {bar} {float(prob):6.1%}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize beach volleyball state machine")
    parser.add_argument('--full', action='store_true', help='Create full state machine graph')
    parser.add_argument('--simple', action='store_true', help='Create simplified graph')
    parser.add_argument('--analyze', action='store_true', help='Analyze probabilities')
    parser.add_argument('--all', action='store_true', help='Create all visualizations')
    
    args = parser.parse_args()
    
    sm = create_beach_volleyball_state_machine()
    
    if args.all or not any([args.full, args.simple, args.analyze]):
        # Default: create all
        create_state_machine_graph(sm)
        create_simplified_graph(sm)
        analyze_probabilities(sm)
        create_probability_heatmap()
    else:
        if args.full:
            create_state_machine_graph(sm)
        if args.simple:
            create_simplified_graph(sm)
        if args.analyze:
            analyze_probabilities(sm)
            create_probability_heatmap()