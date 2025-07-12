# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Pre-defined team probability templates for different skill levels."""

from typing import Dict, List, Tuple
from decimal import Decimal
from types_ import ProbabilityTransitions


def get_common_state_templates() -> Dict[str, ProbabilityTransitions]:
    """Get common probability templates for different team skill levels."""
    
    templates = {
        "elite_serving": {
            "s_serve_ready": [
                ("s_serve_ace", Decimal("0.12")),
                ("s_serve_error", Decimal("0.05")),
                ("s_serve_in_play", Decimal("0.83"))
            ],
            # ... other elite serving states
        },
        "elite_receiving": {
            # ... elite receiving states
        },
        "novice_serving": {
            # ... novice serving states
        },
        "novice_receiving": {
            # ... novice receiving states
        },
        # ... other templates
    }
    
    return templates
