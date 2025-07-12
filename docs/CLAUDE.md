# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running Tests
```bash
# Run comprehensive tests and demonstrations
python main.py --test
uv run main.py --test

# Run individual test functions (modify tests/test_functions.py as needed)
python -c "from tests.test_functions import test_state_machine_creation; test_state_machine_creation()"
```

### Basic Usage
```bash
# Show usage information and examples
python main.py
uv run main.py

# Simulate rally points
python main.py --points 10
uv run main.py --points 20

# Direct module usage examples
python -c "from state_definitions import create_beach_volleyball_state_machine; from rally_simulator import simulate_complete_rally; sm = create_beach_volleyball_state_machine(); print(simulate_complete_rally(sm))"
```

### Visualization and Analysis
```bash
# Text-based state machine analysis
cd utils && uv run text_state_diagram.py

# Interactive web visualization  
cd utils && uv run interactive_visualization.py --plotly

# Probability analysis
cd utils && uv run visualize_state_machine.py --analyze
```

### Python Environment
- Requires Python 3.9+
- Uses `uv` as package manager (PEP 723 script dependencies)
- No external dependencies required - uses only Python standard library

## Architecture Overview

This is a **beach volleyball rally state machine simulation** system with a functional, dictionary-based approach:

### Core Components

1. **State Machine (`state_machine.py`)**
   - `RallyStateMachine` class: Dictionary-based state machine with transitions, probabilities, and terminal states
   - Validates probability distributions and manages state transitions
   - Methods: `get_next_states()`, `is_terminal_state()`, `get_acting_team()`

2. **Types and Constants (`types_.py`)**
   - `ActionType` enum: serve, reception, set, attack, dig, block, transition
   - `StateTransitionTuple`: (next_state, probability, action_type)
   - `ProbabilityTransitions`: Dict mapping states to transition lists

3. **State Definitions (`state_definitions.py`)**
   - `create_beach_volleyball_state_machine()`: Creates the complete 47-state machine
   - State naming convention: `s_` (serving team), `r_` (receiving team), terminal states
   - Realistic volleyball probability distributions for each action outcome

4. **Simulation Layers**
   - **Rally Level** (`rally_simulator.py`): Single rally simulation from serve to terminal state
   - **Match Level** (`match_simulator.py`): Multiple points with alternating serve teams
   - Uses weighted random selection based on state transition probabilities

5. **Team Templates (`team_templates.py`)**
   - Predefined skill-level templates (elite, intermediate, beginner teams)
   - Allows customization of team-specific probability distributions

6. **State Machine Builder (`state_machine_builder.py`)**
   - `create_state_machine_from_teams()`: Builds custom state machines from team templates
   - Combines serving and receiving states from different teams

### Key Design Patterns

- **Functional Approach**: Uses dictionaries and pure functions rather than OOP state patterns
- **Probability-Based**: All transitions include Decimal probabilities for precise simulation
- **Team-Agnostic Core**: Base state machine with team-specific overlays
- **Immutable State**: State transitions create new states rather than modifying existing ones

### State Machine Structure

- **47 total states**: 30 continuation states + 17 terminal states
- **6 volleyball phases**: serve, reception, setting, attack, defense, transition
- **Team Convention**: Team A always serves first, Team B receives first
- **Realistic Modeling**: Based on actual volleyball rules and outcome probabilities

## Project Structure

### Core Application Files (Root Directory)
- `main.py`: Main entry point with CLI interface
- `state_definitions.py`: Core state machine definition and probabilities
- `state_machine.py`: State machine class and logic
- `rally_simulator.py`: Single rally simulation functions
- `match_simulator.py`: Match-level simulation with multiple points
- `team_templates.py`: Predefined team skill templates
- `state_machine_builder.py`: Custom state machine creation utilities
- `types_.py`: Type definitions and constants
- `BVRallyStateMachineDict.py`: Extended/comprehensive implementation

### Utilities (`utils/` directory)
- `text_state_diagram.py`: Comprehensive text-based analysis and flow diagrams
- `visualize_state_machine.py`: Graphviz-based static visualizations
- `interactive_visualization.py`: NetworkX and Plotly interactive graphs
- `display.py`: Display utilities and formatting functions
- Generated files (HTML visualizations, PNG graphs, etc.)

### Tests (`tests/` directory)
- `test_functions.py`: Comprehensive test suite and validation

### Documentation (`docs/` directory)
- `CLAUDE.md`: This file - development guidance
- `README.md`: Project overview and usage instructions

## Key Files for Modification

- `state_definitions.py`: Modify base probabilities or add new states
- `team_templates.py`: Add new team skill templates
- `tests/test_functions.py`: Add new test scenarios or validation logic
- `match_simulator.py`: Modify match-level simulation logic

## Validation and Testing

The system includes comprehensive validation:
- Probability sum validation (must equal 1.0 for each state)
- State transition validation 
- Win condition testing for all terminal states
- Match simulation with identical teams (should approach 50% win rate)