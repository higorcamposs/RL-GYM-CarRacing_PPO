# RL-GYM-CarRacing_PPO
---
## 📌 Documentação - Treinamento PPO para CarRacing-v3
Este repositório contém um conjunto de scripts para treinar um agente de Aprendizado por Reforço (RL) no ambiente CarRacing-v3 usando Proximal Policy Optimization (PPO) da biblioteca Stable-Baselines3.
O objetivo é fazer com que o carro permaneça na pista, evite sair para a área verde e mantenha uma velocidade adequada para completar a corrida da melhor forma possível.
---
## 🛠️ Estrutura dos Arquivos
> 📂 docs/ - Contém a documentação do projeto
> 📂 models/ - Armazena os modelos treinados
📂 logs/ - Contém logs do treinamento e tensorboard
📂 videos/ - Guarda gravações dos modelos treinados
📜 main.py - Script principal que gerencia o fluxo de execução
📜 ppo_train.py - Script responsável pelo treinamento do agente
📜 show_racing.py - Script que carrega e exibe o desempenho do agente
📜 wrapper.py - Define um wrapper para penalizar comportamentos indesejados
