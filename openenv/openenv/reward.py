# openenv/reward.py

def calculate_reward(observation, action_type, ideal_action):
    """
    Strictly clamps rewards between 0.002 and 0.998 
    to satisfy Meta's Phase 2 edge-case requirements.
    """
    if action_type == ideal_action:
        return 0.998
    elif action_type == "run_diagnostic":
        return 0.500
    else:
        return 0.002
