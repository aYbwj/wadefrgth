import os
from openai import OpenAI
from environment import CyberPhysicalEnv
from models import FactoryAction

def run_real_inference():
    print("[START]")
    
    API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1")
    MODEL_NAME = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
    HF_TOKEN = os.environ.get("HF_TOKEN")

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    env = CyberPhysicalEnv()
    
    for step_num in range(1, 4):
        obs = env.reset()
        temp = obs.get('reported_temperature', 70)
        wear = obs.get('wear_level', 0)
        
        prompt = f"Factory state: Temp={temp}, Wear={wear}. Choose ONE action word: 'cool_down', 'replace_parts', 'calibrate_sensor', or 'run_diagnostic'. Reply with the word only."
        
        try:
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            chosen_action = res.choices[0].message.content.strip().lower()
            if chosen_action not in ['cool_down', 'replace_parts', 'calibrate_sensor', 'run_diagnostic']:
                chosen_action = "run_diagnostic"
                
            action = FactoryAction(action_type=chosen_action)
            next_obs, reward, done = env.step(action)
            
            print(f"[STEP] {step_num}: State [{temp}C, Wear {wear}] | Action taken: {chosen_action} | Grader Reward: {reward}")
            
        except Exception as e:
            print(f"[STEP] {step_num}: Error - {str(e)}")

    print("[END]")

if __name__ == "__main__":
    run_real_inference()