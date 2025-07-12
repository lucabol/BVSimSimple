# /// script
# requires-python = ">=3.9"
# dependencies = ["networkx", "matplotlib", "plotly"]
# ///
"""Interactive visualization using NetworkX and Plotly."""

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from state_definitions import create_beach_volleyball_state_machine
from state_machine import RallyStateMachine


def create_networkx_graph(sm: RallyStateMachine) -> nx.DiGraph:
    """Create a NetworkX directed graph from the state machine."""
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for state in sm.get_all_states():
        node_type = 'terminal' if sm.is_terminal_state(state) else 'continuation'
        team = 'serving' if state.startswith('s_') else 'receiving' if state.startswith('r_') else 'neutral'
        G.add_node(state, type=node_type, team=team)
    
    # Add edges with probabilities
    for state, transitions in sm.transitions.items():
        for next_state, probability, action_type in transitions:
            G.add_edge(state, next_state, 
                      probability=float(probability), 
                      action=action_type.value,
                      weight=float(probability))
    
    return G


def plot_matplotlib_graph(sm: RallyStateMachine, filename: str = "state_machine_matplotlib.png") -> None:
    """Create a matplotlib visualization."""
    G = create_networkx_graph(sm)
    
    plt.figure(figsize=(20, 16))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Color nodes by type and team
    node_colors = []
    for node in G.nodes():
        if sm.is_terminal_state(node):
            node_colors.append('red')
        elif node.startswith('s_'):
            node_colors.append('lightblue')
        elif node.startswith('r_'):
            node_colors.append('lightgreen')
        else:
            node_colors.append('gray')
    
    # Draw the graph
    nx.draw(G, pos, 
            node_color=node_colors,
            node_size=1000,
            font_size=8,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            edge_color='gray',
            alpha=0.7)
    
    # Add edge labels for probabilities
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        edge_labels[(u, v)] = f"{data['probability']:.2f}"
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)
    
    plt.title("Beach Volleyball State Machine", size=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Matplotlib graph saved as {filename}")


def create_interactive_plotly(sm: RallyStateMachine, filename: str = "interactive_state_machine.html") -> None:
    """Create an interactive Plotly visualization."""
    G = create_networkx_graph(sm)
    
    # Use spring layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Prepare node trace
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        
        if sm.is_terminal_state(node):
            node_colors.append(0)  # Red for terminal
        elif node.startswith('s_'):
            node_colors.append(1)  # Blue for serving team
        elif node.startswith('r_'):
            node_colors.append(2)  # Green for receiving team
        else:
            node_colors.append(3)  # Gray for other
    
    # Prepare edge traces
    edge_x = []
    edge_y = []
    edge_info = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        prob = G[edge[0]][edge[1]]['probability']
        action = G[edge[0]][edge[1]]['action']
        edge_info.append(f"{edge[0]} → {edge[1]}<br>Probability: {prob:.1%}<br>Action: {action}")
    
    # Create edge trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                           line=dict(width=1, color='#888'),
                           hoverinfo='none',
                           mode='lines')
    
    # Create node trace
    node_trace = go.Scatter(x=node_x, y=node_y,
                           mode='markers+text',
                           hoverinfo='text',
                           text=node_text,
                           textposition="middle center",
                           hovertext=[f"State: {text}" for text in node_text],
                           marker=dict(size=20,
                                     color=node_colors,
                                     colorscale=[[0, 'red'], [0.33, 'lightblue'], [0.66, 'lightgreen'], [1, 'gray']],
                                     line=dict(width=2)))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                        title=dict(text='Interactive Beach Volleyball State Machine', font=dict(size=16)),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Node colors: Blue=Serving, Green=Receiving, Red=Terminal",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002,
                            xanchor="left", yanchor="bottom",
                            font=dict(size=12, color="black")
                        )],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    fig.write_html(filename)
    print(f"Interactive graph saved as {filename}")
    print("Open in browser to explore the state machine interactively!")


def analyze_graph_metrics(sm: RallyStateMachine) -> None:
    """Analyze graph-theoretic properties of the state machine."""
    G = create_networkx_graph(sm)
    
    print("Graph Analysis:")
    print("=" * 40)
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Density: {nx.density(G):.3f}")
    print(f"Is DAG (Directed Acyclic Graph): {nx.is_directed_acyclic_graph(G)}")
    
    # Calculate centrality measures
    print("\nCentrality Analysis (Top 5 nodes):")
    in_centrality = nx.in_degree_centrality(G)
    out_centrality = nx.out_degree_centrality(G)
    
    print("Highest in-degree (most reached states):")
    for state, centrality in sorted(in_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {centrality:.3f}")
    
    print("Highest out-degree (most branching states):")
    for state, centrality in sorted(out_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {centrality:.3f}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive visualization of state machine")
    parser.add_argument('--matplotlib', action='store_true', help='Create matplotlib visualization')
    parser.add_argument('--plotly', action='store_true', help='Create interactive Plotly visualization')
    parser.add_argument('--analyze', action='store_true', help='Analyze graph metrics')
    parser.add_argument('--all', action='store_true', help='Create all visualizations')
    
    args = parser.parse_args()
    
    sm = create_beach_volleyball_state_machine()
    
    if args.all or not any([args.matplotlib, args.plotly, args.analyze]):
        plot_matplotlib_graph(sm)
        create_interactive_plotly(sm)
        analyze_graph_metrics(sm)
    else:
        if args.matplotlib:
            plot_matplotlib_graph(sm)
        if args.plotly:
            create_interactive_plotly(sm)
        if args.analyze:
            analyze_graph_metrics(sm)