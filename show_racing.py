import gymnasium as gym
import numpy as np
import os
import sys
import base64
from datetime import datetime
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from IPython.display import HTML, display
import subprocess
from rich import print  

def find_latest_model(timesteps: int) -> Path:

    folder = Path("./models")
    pattern = f"best_model_from_{timesteps}_*.zip"
    candidates = list(folder.glob(pattern))

    if not candidates:
        print(f"[bold red]ERRO: Nenhum modelo encontrado no padrão '{pattern}' em {folder}[/bold red]")
        sys.exit(1)

    latest = max(candidates, key=lambda x: x.stat().st_mtime)
    return latest

def record_video(env_id, model, video_length=1000, prefix="car_racing_video", video_folder="videos/"):
    print("\n[bold cyan]========== GRAVANDO O VÍDEO ==========[/bold cyan]")
    eval_env = DummyVecEnv([lambda: Monitor(gym.make(env_id, render_mode="rgb_array"))])
    eval_env = VecVideoRecorder(
        eval_env,
        video_folder=video_folder,
        record_video_trigger=lambda step: step == 0,
        video_length=video_length,
        name_prefix=prefix
    )

    obs = eval_env.reset()
    for _ in range(video_length):
        action, _ = model.predict(obs)
        obs, _, _, _ = eval_env.step(action)

    eval_env.close()
    print(f"[bold yellow]Vídeo salvo como:[/bold yellow] {prefix}.mp4 em {video_folder}")

def show_videos(video_path="videos", prefix="car_racing_video"):
    html = []
    video_file = None
    for mp4 in Path(video_path).glob(f"{prefix}*.mp4"):
        video_b64 = base64.b64encode(mp4.read_bytes())
        html.append(
            f'''
            <video alt="{mp4}" autoplay loop controls style="height: 400px;">
                <source src="data:video/mp4;base64,{video_b64.decode('ascii')}" type="video/mp4" />
            </video>
            '''
        )
        video_file = mp4

    if html:
        display(HTML("<br>".join(html)))

    if video_file:
        print(f"[bold yellow]Executando vídeo local:[/bold yellow] {video_file}")
        try:
            subprocess.run(["xdg-open", str(video_file)])
        except FileNotFoundError:
            pass

if len(sys.argv) < 2:
    print("[bold red]ERRO: Número de timesteps não especificado![/bold red]")
    sys.exit(1)

TIMESTEPS = int(sys.argv[1])
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

print("\n[bold cyan]========== INICIANDO EXIBIÇÃO DE RESULTADOS ==========[/bold cyan]")

model_path = find_latest_model(TIMESTEPS)
print(f"[bold yellow]Carregando modelo:[/bold yellow] {model_path}")

best_model = PPO.load(str(model_path))

eval_env = DummyVecEnv([lambda: Monitor(gym.make("CarRacing-v3"))])

mean_reward, std_reward = evaluate_policy(best_model, eval_env, n_eval_episodes=5, deterministic=False)
print(f"[bold magenta]Melhor modelo - Recompensa média:[/bold magenta] {mean_reward:.2f} +/- {std_reward:.2f}")

video_filename = f"car_racing_{TIMESTEPS}_{current_time}"

record_video("CarRacing-v3", best_model, video_length=1000, prefix=video_filename)
print("\n[bold cyan]========== EXIBINDO O VÍDEO ==========[/bold cyan]")
show_videos("videos", prefix=video_filename)

print("[bold green]========== EXIBIÇÃO CONCLUÍDA ==========[/bold green]")
