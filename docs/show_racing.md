# Documentação do show_racing.py

## Visão Geral
O script `show_racing.py` é responsável por carregar um modelo treinado previamente e exibir seu desempenho no ambiente **CarRacing-v3**. Ele avalia o modelo, grava um vídeo da execução e permite a visualização do comportamento do agente.

## Fluxo de Execução
1. Captura o argumento de timesteps para encontrar o modelo correspondente.
2. Localiza o melhor modelo salvo com base nos timesteps.
3. Avalia a performance do modelo utilizando um ambiente de teste.
4. Grava um vídeo da execução do agente no ambiente.
5. Exibe o vídeo salvo.

---

## Parâmetro de Entrada
O script recebe um argumento obrigatório:

| Argumento  | Tipo  | Descrição |
|------------|-------|------------|
| TIMESTEPS  | `int` | Quantidade de timesteps do modelo a ser carregado |

---

## Etapas do Script

### 1. Captura de Argumento
O script captura o argumento `TIMESTEPS` passado via linha de comando e verifica se foi informado corretamente.
```python
if len(sys.argv) < 2:
    print("[bold red]ERRO: Número de timesteps não especificado![/bold red]")
    sys.exit(1)

TIMESTEPS = int(sys.argv[1])
```

### 2. Localização do Melhor Modelo
Utiliza-se a função `find_latest_model()` para encontrar o modelo treinado mais recente com base no padrão de nomeação.
```python
def find_latest_model(timesteps: int) -> Path:
    folder = Path("./models")
    pattern = f"best_model_from_{timesteps}_*.zip"
    candidates = list(folder.glob(pattern))
    
    if not candidates:
        print(f"[bold red]ERRO: Nenhum modelo encontrado no padrão '{pattern}' em {folder}[/bold red]")
        sys.exit(1)
    
    latest = max(candidates, key=lambda x: x.stat().st_mtime)
    return latest
```

### 3. Avaliação do Modelo
A função `evaluate_policy()` é utilizada para testar o modelo em 5 episódios e calcular a recompensa média.
```python
mean_reward, std_reward = evaluate_policy(best_model, eval_env, n_eval_episodes=5, deterministic=False)
print(f"[bold magenta]Melhor modelo - Recompensa média:[/bold magenta] {mean_reward:.2f} +/- {std_reward:.2f}")
```

### 4. Gravação do Vídeo
A função `record_video()` é responsável por capturar um vídeo da execução do agente no ambiente.
```python
def record_video(env_id, model, video_length=1000, prefix="car_racing_video", video_folder="videos/"):
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
```

### 5. Exibição do Vídeo
O vídeo salvo é exibido no ambiente do usuário por meio da função `show_videos()`.
```python
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
```

---

## Como Executar
O script pode ser executado após o treinamento de um modelo PPO, utilizando a seguinte linha de comando:
```bash
python show_racing.py 100000
```
Substitua `100000` pelo número de timesteps correspondente ao modelo treinado.

---

## Possíveis Melhorias
- Adicionar opção para gravar e exibir mais de um vídeo por execução.
- Testar diferentes abordagens para seleção do melhor modelo.
- Incluir mais estatísticas na avaliação do desempenho do agente.

Este documento serve para auxiliar no entendimento e execução do `show_racing.py`, garantindo que os modelos treinados possam ser devidamente avaliados e analisados.
