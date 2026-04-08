import os
from openai import OpenAI
from fastapi import FastAPI
import gradio as gr

from environment import CyberPhysicalEnv
from models import FactoryAction

app = FastAPI()

# Environment Variables
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
env = CyberPhysicalEnv()

# FastAPI Endpoints
@app.post("/reset")
@app.get("/reset") # This allows both types just in case
def reset():
    obs = env.reset()
    return obs # Ensure it returns the observation object directly

@app.post("/step")
def step(action: FactoryAction):
    # Ensure this is exactly as written before
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}
@app.get("/state")
def get_state():
    return env.get_state() if hasattr(env, 'get_state') else {}

# UI Functions
def fetch_telemetry():
    obs, _, _ = env.step(FactoryAction(action_type="run_diagnostic"))
    temp = obs.get('reported_temperature', 0)
    wear = obs.get('wear_level', 0)
    sensor = obs.get('sensor_health', 'Unknown')
    return f"{temp} °C", f"{wear} / 1.0", f"🟢 {sensor}", temp, wear, sensor

def ask_llama(temp, wear, sensor):
    prompt = f"You are an AI factory monitor. Current state -> Temperature: {temp}, Wear Level: {wear}, Sensor: {sensor}. Give a 2-sentence diagnostic report and suggest one actionable maintenance step."
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"🛑 Connection Error: {str(e)}"

# Web UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🏭 Industrial AI Command Center</h1>")
    gr.Markdown("<p style='text-align: center;'>Real-time telemetry and predictive maintenance powered by <b>Meta Llama 3.1</b></p>")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📡 Live Sensor Feed")
            status_btn = gr.Button("Fetch Live Telemetry", variant="primary")
            
            with gr.Group():
                temp_disp = gr.Textbox(label="Core Temperature")
                wear_disp = gr.Textbox(label="Mechanical Wear Level")
                sensor_disp = gr.Textbox(label="Sensor Status")
            
            h_temp = gr.Number(visible=False)
            h_wear = gr.Number(visible=False)
            h_sensor = gr.Textbox(visible=False)
            
        with gr.Column(scale=2):
            gr.Markdown("### 🧠 Llama 3.1 Diagnostic Engine")
            explain_btn = gr.Button("Generate AI Maintenance Report")
            advice_out = gr.Textbox(label="Predictive Action Plan", lines=8)

    status_btn.click(fetch_telemetry, outputs=[temp_disp, wear_disp, sensor_disp, h_temp, h_wear, h_sensor])
    explain_btn.click(ask_llama, inputs=[h_temp, h_wear, h_sensor], outputs=advice_out)

app = gr.mount_gradio_app(FastAPI(), demo, path="/")
