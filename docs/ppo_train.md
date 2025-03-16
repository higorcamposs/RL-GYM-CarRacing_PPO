# Documentação do ppo_train.py

## Visão Geral
O script `ppo_train.py` é responsável pelo treinamento de um agente de aprendizado por reforço no ambiente **CarRacing-v3**, utilizando o algoritmo **Proximal Policy Optimization (PPO)** da biblioteca Stable-Baselines3.

## Fluxo de Execução
1. Captura os argumentos de treinamento via **linha de comando**.
2. Define o ambiente de treinamento, incluindo penalizações para comportamentos indesejados.
3. Configura e inicia o treinamento do modelo.
4. Salva os modelos treinados e cria logs do treinamento.
5. Garante que o melhor modelo encontrado seja armazenado separadamente.

---

## Parâmetros de Entrada
Os seguintes argumentos são passados via linha de comando pelo **main.py**:

| Argumento            | Tipo    | Descrição |
|----------------------|---------|------------|
| TIMESTEPS           | `int`   | Quantidade total de timesteps para treinamento |
| EVAL_FREQ           | `int`   | Frequência de avaliação do modelo |
| VERBOSE             | `int`   | Nível de detalhamento do log (0: silenciado, 1: informações básicas, 2: detalhado) |
| BATCH_SIZE          | `int`   | Tamanho dos lotes de amostras para treinamento |
| LEARNING_RATE       | `float` | Taxa de aprendizado da rede neural |
| MIN_SPEED           | `float` | Velocidade mínima para evitar penalização |
| PENALTY_CONTRAMAO   | `float` | Penalização para andar na contramão |
| PENALTY_OFFROAD     | `float` | Penalização para sair da pista |
| PENALTY_DEVAGAR     | `float` | Penalização por andar muito devagar |

---

## Etapas do Script
### 1. Captura de Argumentos
Os argumentos são lidos da linha de comando e convertidos para seus respectivos tipos.

### 2. Criação do Ambiente de Treinamento
O ambiente **CarRacing-v3** é criado e envolvido pelo **CarRacingPenaltiesWrapper**, que aplica penalizações configuráveis para corrigir o comportamento do agente.

```python
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
```

### 3. Configuração do Callback para Salvar o Melhor Modelo
Utiliza-se `EvalCallback` para avaliar periodicamente o agente e armazenar o melhor modelo encontrado.
```python
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./models/",
    log_path="./logs/",
    eval_freq=EVAL_FREQ,
    deterministic=True,
    render=False
)
```

### 4. Configuração do Modelo PPO
O agente PPO é configurado com hiperparâmetros que controlam sua aprendizagem.
```python
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
```

### 5. Execução do Treinamento
O modelo é treinado pelo número especificado de `TIMESTEPS`, utilizando `EvalCallback` para monitoramento.
```python
model.learn(total_timesteps=TIMESTEPS, callback=eval_callback)
```

### 6. Salvamento do Melhor Modelo
Após o treinamento, o melhor modelo encontrado é copiado para um arquivo nomeado dinamicamente com `TIMESTEPS` e `DATETIME`.
```python
best_model_src = "./models/best_model.zip"
best_model_dest = f"./models/best_model_from_{TIMESTEPS}_{start_datetime}.zip"

if os.path.exists(best_model_src):
    import shutil
    shutil.copyfile(best_model_src, best_model_dest)
    print(f"Melhor modelo copiado para: {best_model_dest}")
```

### 7. Registro do Log do Treinamento
Um arquivo de log é criado para armazenar informações sobre o treinamento, incluindo tempos de início/fim, hiperparâmetros utilizados e modelo salvo.
```python
with open(log_filename, "w") as log_file:
    log_file.write(f"INICIO: {start_datetime}\n")
    log_file.write(f"FIM: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n")
    log_file.write(f"TEMPO TOTAL (segundos): {elapsed_time:.2f}\n")
    log_file.write(f"MODELO FINAL SALVO COMO: {model_filename}\n")
```

### 8. Liberação de Recursos
Para evitar vazamentos de memória, o ambiente é fechado após o treinamento.
```python
del model
env.close()
eval_env.close()
```

---

## Como Executar
O script `ppo_train.py` é chamado pelo `main.py`, que define os hiperparâmetros e inicia o treinamento. Para rodá-lo separadamente:
```bash
python ppo_train.py 100000 50000 1 4096 0.0001 0.2 1 100 10
```
Substitua os valores conforme desejado.

---

## Possíveis Melhorias
- Testar diferentes penalizações para encontrar um balanço entre exploração e segurança na pista.
- Ajustar hiperparâmetros como `clip_range` e `gae_lambda` para melhor estabilidade do aprendizado.
- Implementar diferentes `Policies` como `CnnLstmPolicy` para um aprendizado mais contextual.

---

Este documento visa auxiliar na compreensão e execução do treinamento de um agente PPO no ambiente CarRacing-v3.

