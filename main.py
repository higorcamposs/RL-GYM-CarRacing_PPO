import subprocess
from rich import print

TIMESTEPS = 100_000
EVAL_FREQ = 50_000
VERBOSE = 1
BATCH_SIZE = 4096
LEARNING_RATE = 0.0001
MIN_SPEED = 0.2
PENALTY_CONTRAMAO = 1
PENALTY_OFFROAD = 100
PENALTY_DEVAGAR = 10    


print(f"[bold cyan]========== INICIANDO TREINAMENTO ==========[/bold cyan]")
print(f"[bold yellow] -> Timesteps: {TIMESTEPS}\n -> EVAL_FREQ: {EVAL_FREQ} \n -> VERBOSE: {VERBOSE}\n -> BATCH_SIZE: {BATCH_SIZE}\n -> LR: {LEARNING_RATE}[/bold yellow]")
print(f"[bold yellow] -> MIN_SPEED: {MIN_SPEED}\n -> PENALTY_CONTRAMAO: {PENALTY_CONTRAMAO} \n -> PENALTY_OFFROAD: {PENALTY_OFFROAD}\n -> PENALTY_DEVAGAR: {PENALTY_DEVAGAR}[/bold yellow]")

subprocess.run([
    "python",
    "ppo_train.py",
    str(TIMESTEPS),
    str(EVAL_FREQ),
    str(VERBOSE),
    str(BATCH_SIZE),
    str(LEARNING_RATE),
    str(MIN_SPEED),
    str(PENALTY_CONTRAMAO),
    str(PENALTY_OFFROAD),
    str(PENALTY_DEVAGAR)
])

subprocess.run(["python", "show_racing.py", str(TIMESTEPS)])

print("\n[bold green]========== PROCESSO CONCLUÍDO ==========[/bold green]")
