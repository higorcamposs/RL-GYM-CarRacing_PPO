# Documentação do wrapper.py

## Visão Geral
O script `wrapper.py` define um **wrapper** personalizado para o ambiente **CarRacing-v3**, da biblioteca Gymnasium. Este wrapper **penaliza comportamentos indesejados** e **incentiva boas práticas de condução**, ajudando no treinamento de um agente de aprendizado por reforço (**RL - Reinforcement Learning**).

## Objetivo
O **CarRacingPenaltiesWrapper** adiciona **penalizações e recompensas** para guiar o comportamento do agente dentro da pista. Ele:

- **Penaliza** andar na contramão.
- **Penaliza** sair da pista.
- **Penaliza** andar muito devagar.
- **Recompensa** manter velocidade adequada.

## Implementação

### 1. Importação de Bibliotecas
O `wrapper.py` utiliza a biblioteca Gymnasium para modificar o ambiente.
```python
import gymnasium as gym
```

### 2. Classe `CarRacingPenaltiesWrapper`
A classe **herda de `gym.Wrapper`**, permitindo modificar o comportamento do ambiente base.

#### Inicialização (`__init__`)
O método **`__init__`** recebe o ambiente e parâmetros de penalização e velocidade mínima.
```python
def __init__(
    self,
    env,
    min_speed=0.1,
    penalty_contramao=1,
    penalty_offroad=1,
    penalty_devagar=1
):
    super().__init__(env)
    self.prev_x = None
    self.prev_y = None
    self.min_speed = min_speed
    self.penalty_contramao = penalty_contramao
    self.penalty_offroad = penalty_offroad
    self.penalty_devagar = penalty_devagar
```

- **`min_speed`**: Define a velocidade mínima aceitável.
- **`penalty_contramao`**: Penaliza o agente ao andar na contramão.
- **`penalty_offroad`**: Penaliza o agente ao sair da pista.
- **`penalty_devagar`**: Penaliza o agente por andar devagar.

#### Reset do Ambiente (`reset`)
Reinicia o ambiente e as coordenadas anteriores do carro.
```python
def reset(self, **kwargs):
    obs, info = self.env.reset(**kwargs)
    self.prev_x = None
    self.prev_y = None
    return obs, info
```

#### Passo do Agente (`step`)
Este método **modifica as recompensas** com base no comportamento do agente.
```python
def step(self, action):
    obs, reward, done, truncated, info = self.env.step(action)
```

##### Penaliza Contramão
Se a posição Y do carro diminuiu, significa que ele está indo para trás.
```python
if self.prev_y is not None:
    dy = info.get("y_position", 0) - self.prev_y
    if dy < 0:
        reward -= self.penalty_contramao
```

##### Penaliza Saída da Pista
Se o **reward do ambiente for menor que -1**, o carro tocou na área verde.
```python
if reward < -1:
    reward -= self.penalty_offroad
    truncated = False
```

##### Penaliza Velocidade Baixa e Recompensa Alta Velocidade
Se a velocidade estiver abaixo de `min_speed`, aplica penalização. Caso contrário, dá um **grande incentivo** para manter a velocidade alta.
```python
speed = info.get("speed", None)
if speed is not None:
    if speed < self.min_speed:
        reward -= self.penalty_devagar
    else:
        reward += 100  
else:
    if self.prev_x is not None and self.prev_y is not None:
        dx = info.get("x_position", 0) - self.prev_x
        dy = info.get("y_position", 0) - self.prev_y
        dist = (dx**2 + dy**2) ** 0.5
        if dist < self.min_speed:
            reward -= self.penalty_devagar
        else:
            reward += 100  
```

Atualiza as coordenadas do carro para o próximo passo.
```python
self.prev_x = info.get("x_position", 0)
self.prev_y = info.get("y_position", 0)
```

Retorna as observações, a recompensa ajustada e se o episódio terminou.
```python
return obs, reward, done, truncated, info
```

---

## Conclusão
O `wrapper.py` é essencial para orientar o aprendizado do agente, aplicando penalizações e incentivos adequados. Ele garante que o modelo aprenda a **andar na pista**, **evitar contramão** e **manter uma boa velocidade**.

Possíveis melhorias incluem:
- Ajustar **pesos das penalizações** para equilibrar melhor o aprendizado.
- Criar um sistema adaptativo que **aumente ou reduza penalidades** conforme o progresso do agente.
