# Beach Volleyball State Machine Visualization

This directory contains scripts to visualize the beach volleyball rally state machine as interactive graphs.

## Files

- `BVRallyStateMachine.py` - Main state machine implementation
- `visualize_state_machine.py` - Graph generation script  
- `graphs/` - Generated graph files

## Generated Graphs

The visualization script creates three types of graphs:

1. **Full State Machine** (`bv_state_machine_full.gv.png`)
   - Shows all 47 states and 93 transitions
   - Color-coded by team (blue=serving, green=receiving, red=terminal)
   - Grouped by volleyball phases (serve, reception, attack, etc.)

2. **Simplified Version** (`bv_state_machine_simple.gv.png`)
   - Shows only key states in the main rally flow
   - Easier to understand for beginners
   - Focuses on the most common state transitions

3. **SVG Web Version** (`bv_state_machine_web.gv.svg`)
   - Scalable vector format for web browsers
   - Can be embedded in documentation or presentations
   - High quality at any zoom level

## How to Use

### Prerequisites

1. **Install Graphviz system package:**
   - **Windows**: Download from https://graphviz.org/download/ or use `choco install graphviz`
   - **Linux**: `sudo apt-get install graphviz` (Ubuntu/Debian) or `sudo yum install graphviz` (RHEL/CentOS)
   - **macOS**: `brew install graphviz`

2. **Python dependencies** are automatically handled by UV

### Generate Graphs

```bash
# Generate all graph formats
uv run visualize_state_machine.py
```

The script will:
- Create the `graphs/` directory if it doesn't exist
- Generate PNG and SVG versions of the state machine
- Display statistics about the state machine
- Automatically open the graph on Windows

### View Results

- **PNG files**: Open with any image viewer
- **SVG files**: Open with web browser or vector graphics editor
- **Cross-platform**: Works on Windows, Linux, and macOS

## State Machine Legend

- **Blue boxes (S:)**: Serving team (Team A) actions
- **Green ellipses (R:)**: Receiving team (Team B) actions  
- **Red double circles (END:)**: Terminal states (rally ends)
- **Arrows**: Valid state transitions

## Understanding the Graph

The state machine shows how a beach volleyball rally progresses:

1. **Serve Phase**: Team A serves the ball
2. **Reception Phase**: Team B receives and passes
3. **Attack Phase**: Team B sets and attacks
4. **Defense Phase**: Team A digs and blocks
5. **Transition Phase**: Teams alternate attacking
6. **Terminal Phase**: Rally ends with a point

Each state represents a specific action outcome (perfect, good, poor, error) that determines the next possible states in the rally.

## Technical Details

- **Total States**: 47 (including terminal states)
- **Terminal States**: 17 (rally-ending conditions)
- **Continuation States**: 30 (rally continues)
- **Total Transitions**: 93 (possible state changes)
- **Team Convention**: Team A always serves, Team B always receives

The state machine follows volleyball rules and realistic probability distributions for each action outcome.
