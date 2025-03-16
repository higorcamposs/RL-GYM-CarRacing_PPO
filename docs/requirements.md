# 📦 Dependências do Projeto

Este projeto utiliza diversas bibliotecas para **treinamento de agentes** no ambiente **CarRacing-v3** com **Stable-Baselines3**. Abaixo está um resumo do papel de cada uma.

---

## 🏎️ Bibliotecas Principais

| Biblioteca            | Descrição |
|-----------------------|-----------|
| `gymnasium`          | Biblioteca principal para criação e interação com ambientes de aprendizado por reforço. É a evolução do **OpenAI Gym**. |
| `box2d`              | Física de simulação de corpos rígidos 2D, usada para modelar colisões e dinâmicas no **CarRacing-v3**. |
| `gymnasium[box2d]`   | Extensão do Gymnasium para suportar ambientes baseados em física, como o **CarRacing-v3**. |
| `stable-baselines3`  | Framework que implementa algoritmos de aprendizado por reforço, incluindo **PPO** (usado neste projeto). |

---

## 📊 Bibliotecas para Visualização e Debug

| Biblioteca          | Descrição |
|--------------------|-----------|
| `matplotlib`      | Biblioteca para gerar gráficos e visualizar métricas do treinamento. |
| `tensorboard`     | Ferramenta para monitoramento do treinamento do agente em tempo real. |
| `numpy`           | Biblioteca para manipulação de arrays numéricos, essencial para cálculos matemáticos no aprendizado. |

---

## 🎥 Bibliotecas para Processamento de Vídeo e Imagem

| Biblioteca        | Descrição |
|------------------|-----------|
| `opencv-python`  | Processamento de imagens e vídeos, útil para manipular frames do ambiente. |
| `moviepy`        | Edição e manipulação de vídeos, usada para salvar e exibir gravações das corridas. |
| `pygame`         | Framework para renderização gráfica e interação com jogos. O **CarRacing-v3** pode utilizá-lo para exibir simulações. |

---

## 🔍 Bibliotecas de Debug e Output

| Biblioteca        | Descrição |
|------------------|-----------|
| `ipython`        | Versão interativa do Python, útil para testes e execução de código em notebooks. |
| `rich`           | Biblioteca para melhorar a visualização de logs no terminal, adicionando cores e formatação. |

---
