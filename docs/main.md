# main.py

Esse script orquestra todo o processo de treinamento e avaliação, executando os scripts ppo_train.py e show_racing.py. Ele também define os parâmetros do treinamento, como número de timesteps, taxa de aprendizado (learning_rate), frequência de avaliação (eval_freq), penalizações e incentivos para o agente.

---
### Execução

```bash
python main.py
```

### Código

> import subprocess

>from rich import print

#### Definir parâmetros do treinamento
- TIMESTEPS 
    - Define o número total de interações que o agente terá com o ambiente durante o treinamento.
        - Valores maiores permitem que o modelo aprenda mais, mas aumentam o tempo de treinamento.
        - Se for muito baixo, o agente pode não aprender padrões complexos de navegação.


- EVAL_FREQ 
    - Define a frequência (quantos passos de treinamento) para avaliar o desempenho do modelo e salvar o melhor modelo encontrado até aquele momento. 
        - Um valor muito alto pode fazer com que o agente treine por muito tempo sem salvar um bom modelo. 
        - Um valor muito baixo pode gerar salvamentos excessivos sem grandes melhorias.
- VERBOSE
    - Controla o nível de detalhamento dos logs do treinamento.
        - 0: Sem logs (silencioso, útil para rodar em produção).
        - 1: Exibe logs básicos sobre o progresso do treinamento.
        - 2: Exibe logs mais detalhados (recomendado para depuração).
- BATCH_SIZE
    - Define o tamanho do lote de amostras que o algoritmo processa em cada atualização da rede neural.
        - Lotes pequenos (512, 1024):
        > Permitem aprendizado mais detalhado, mas podem ser mais ruidosos.
    Podem gerar um treinamento instável se forem muito pequenos.

        - Lotes grandes (2048, 4096, 8192):
        > Tornam o treinamento mais estável, mas exigem mais memória.
    Permitem que o agente veja mais exemplos antes de atualizar a política.

- LEARNING_RATE
    - Define a taxa de aprendizado do modelo, ou seja, o quanto os pesos da rede neural mudam a cada atualização.
        - Muito alto (0.001 ou mais):
        > O modelo aprende rápido, mas pode ficar instável e "esquecer" padrões antigos.
        - Muito baixo (0.00001 ou menos):
        > O modelo aprende muito devagar e pode precisar de milhões de timesteps para melhorar.


#### Parâmetros de penalização
- MIN_SPEED
    -  Define a velocidade mínima abaixo da qual o carro recebe uma penalização (PENALTY_DEVAGAR).
        - Muito baixo (0.01 - 0.05): O carro pode andar devagar demais e não completar a corrida.
        - Muito alto (0.5 - 1.0): O carro pode ser forçado a correr rápido demais e perder o controle.
- PENALTY_CONTRAMAO
    -  Penaliza o carro caso ele ande para trás no eixo y (ou seja, na contramão).
        - Baixo (1-5): O agente pode aprender lentamente a evitar a contramão.
        - Muito alto (50+): Pode fazer com que o agente congele ou evite explorar curvas.
- PENALTY_OFFROAD
    -  Penaliza o carro se ele sair da pista (encostar na área verde).
        - Muito baixo (<10): O carro pode ignorar a punição e continuar saindo da pista.
        - Muito alto (>500): O agente pode ficar com medo de se aproximar das bordas e dirigir de forma estranha.
- PENALTY_DEVAGAR
    -  Penaliza o carro se ele estiver muito devagar (speed < MIN_SPEED).
        - Muito baixo (<5): O agente pode não dar importância para andar rápido.
        - Muito alto (>20): Pode forçar o carro a correr demais e perder o controle.

| Parâmetro          | Significado                                      | Valor Atual | Sugestão de Ajuste |
|--------------------|------------------------------------------------|------------|--------------------|
| `TIMESTEPS`       | Quantidade de interações no treino              | 100.000    | Aumentar para 1.000.000 para melhor aprendizado |
| `EVAL_FREQ`       | Frequência de avaliação do modelo               | 50.000     | 5% a 10% do `TIMESTEPS` |
| `VERBOSE`         | Detalhamento dos logs                           | 1          | 1 para monitoramento, 2 para depuração |
| `BATCH_SIZE`      | Tamanho do lote de aprendizado                  | 4096       | 1024 a 8192 |
| `LEARNING_RATE`   | Taxa de aprendizado do PPO                      | 0.0001     | Reduzir para 0.00005 se instável |
| `MIN_SPEED`         | Velocidade mínima antes de penalizar          | 0.2        | 0.15 a 0.3 |
| `PENALTY_CONTRAMAO` | Punição por andar para trás                   | 1          | 5 a 10 para melhor efeito |
| `PENALTY_OFFROAD`   | Punição por sair da pista                     | 100        | 100 a 300 |
| `PENALTY_DEVAGAR`   | Punição por andar devagar                     | 10         | 5 a 20 |

#### Executar o treinamento do modelo
```python
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
```
#### Executar a avaliação do modelo treinado
```python
subprocess.run(["python", "show_racing.py", str(TIMESTEPS)])
```

