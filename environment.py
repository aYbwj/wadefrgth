import random
from models import FactoryAction

class CyberPhysicalEnv:
    def __init__(self):
        self.state = {"reported_temperature": 70.0, "wear_level": 0.0, "sensor_health": "Online"}

    def reset(self):
        self.state = {
            "reported_temperature": random.choice([70.0, 95.0, 105.0]),
            "wear_level": random.choice([0.0, 0.5, 0.9]),
            "sensor_health": random.choice(["Online", "Offline", "Erratic"])
        }
        return self.state

    def step(self, action: FactoryAction):
        # Base reward logic scaled 0.0 to 1.0
        if action.action_type == "cool_down":
            self.state["reported_temperature"] = 70.0
            reward = 1.0 if self.state["reported_temperature"] > 90.0 else 0.5
        elif action.action_type == "replace_parts":
            self.state["wear_level"] = 0.0
            reward = 1.0 if self.state["wear_level"] > 0.5 else 0.5
        elif action.action_type == "calibrate_sensor":
            self.state["sensor_health"] = "Online"
            reward = 1.0 if self.state["sensor_health"] != "Online" else 0.5
        elif action.action_type == "run_diagnostic":
            reward = 0.8
        else:
            reward = 0.0 

        done = False 
        return self.state, reward, done

    def get_state(self):
        return self.state