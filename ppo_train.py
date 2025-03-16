import os
import sys
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from rich import print 
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import VecTransposeImage, DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from wrapper import CarRacingPenaltiesWrapper

if len(sys.argv) < 10:
    print("[bold red]ERRO: Parâmetros insuficientes![/bold red]")
    sys.exit(1)

TIMESTEPS = int(sys.argv[1])
EVAL_FREQ = int(sys.argv[2])
VERBOSE = int(sys.argv[3])
BATCH_SIZE = int(sys.argv[4])
LEARNING_RATE = float(sys.argv[5])

MIN_SPEED = float(sys.argv[6])
PENALTY_CONTRAMAO = float(sys.argv[7])
PENALTY_OFFROAD = float(sys.argv[8])
PENALTY_DEVAGAR = float(sys.argv[9])

start_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
model_filename = f"model_{TIMESTEPS}_{start_datetime}.zip"
log_filename = f"./logs/training_log_{TIMESTEPS}_{start_datetime}.log"

def make_training_env():
    def _init():
        base_env = gym.make("CarRacing-v3")
        base_env = CarRacingPenaltiesWrapper(
            base_env,
            min_speed=MIN_SPEED,
            penalty_contramao=PENALTY_CONTRAMAO,
            penalty_offroad=PENALTY_OFFROAD,
            penalty_devagar=PENALTY_DEVAGAR
        )
        return base_env
    return make_vec_env(_init, n_envs=4)

eval_env = gym.make("CarRacing-v3")
eval_env = CarRacingPenaltiesWrapper(eval_env)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecTransposeImage(eval_env)

env = make_training_env()
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./models/",
    log_path="./logs/",
    eval_freq=EVAL_FREQ,
    deterministic=True,
    render=False
)

model = PPO(
    "CnnPolicy",
    env,
    clip_range=0.3,
    ent_coef=0.01,
    gae_lambda=0.95,
    vf_coef=0.8,
    verbose=VERBOSE,
    batch_size=BATCH_SIZE,
    learning_rate=LEARNING_RATE,
    tensorboard_log="./ppo_car_racing_tensorboard/"
)

start_time = time.time()
model.learn(total_timesteps=TIMESTEPS, callback=eval_callback)
end_time = time.time()

elapsed_time = end_time - start_time

best_model_src = "./models/best_model.zip"
best_model_dest = f"./models/best_model_from_{TIMESTEPS}_{start_datetime}.zip"

if os.path.exists(best_model_src):
    import shutil
    shutil.copyfile(best_model_src, best_model_dest)
    print(f"[bold green]Melhor modelo copiado para:[/bold green] {best_model_dest}")
else:
    print("[bold red]AVISO:[/bold red] Nenhum 'best_model.zip' encontrado no EvalCallback.")

del model
env.close()
eval_env.close()

with open(log_filename, "w") as log_file:
    log_file.write(f"INICIO: {start_datetime}\n")
    log_file.write(f"FIM: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n")
    log_file.write(f"TEMPO TOTAL (segundos): {elapsed_time:.2f}\n")
    log_file.write(f"MODELO FINAL SALVO COMO: {model_filename}\n")
    log_file.write("TAMBÉM SALVO COMO: best_restult_from_last_run.zip\n")
    log_file.write(f"TIMESTEPS TREINADOS: {TIMESTEPS}\n")
    log_file.write(f"EVAL_FREQ: {EVAL_FREQ}\n")
    log_file.write(f"VERBOSE: {VERBOSE}\n")
    log_file.write(f"BATCH_SIZE: {BATCH_SIZE}\n")
    log_file.write(f"LEARNING_RATE: {LEARNING_RATE}\n")
    log_file.write(f"\n-- MELHOR MODELO COPIADO PARA: best_model_from_{TIMESTEPS}_{start_datetime}.zip\n")

print("[bold green]\n========== TREINAMENTO CONCLUIDO ========== [/bold green]")
print(f"[bold magenta]Modelo FINAL salvo como:[/bold magenta] {model_filename}")
print(f"[bold magenta]Também salvo como (final):[/bold magenta] best_restult_from_last_run.zip")

if os.path.exists(best_model_src):
    print(f"[bold magenta]Melhor modelo copiado como:[/bold magenta] {best_model_dest}")
else:
    print("[bold red]Não havia best_model.zip do EvalCallback para copiar.[/bold red]")

print(f"[bold magenta]Log de treinamento:[/bold magenta] {log_filename}")
