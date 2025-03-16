# Instalação e Configuração do Ambiente

Este documento explica o funcionamento do script `install.sh` e como utilizá-lo para configurar o ambiente de desenvolvimento.

---

## 1. Visão Geral

O script `install.sh` é responsável por configurar um ambiente virtual e instalar todas as dependências necessárias para executar o projeto. Ele garante que as bibliotecas corretas sejam instaladas e que o ambiente esteja pronto para execução.

---

## 2. Estrutura do Script

Abaixo está um resumo das principais etapas do `install.sh`:

```bash
#!/bin/bash
```
Define que o script será executado no interpretador de comandos do Bash.

```bash
rm -rf venv/
```
Remove o diretório `venv/` caso ele já exista. Isso garante uma instalação limpa do ambiente virtual.

```bash
python -m venv venv
```
Cria um novo ambiente virtual chamado `venv`.

```bash
source venv/bin/activate
```
Ativa o ambiente virtual para garantir que todas as bibliotecas sejam instaladas dentro dele, evitando conflitos com outras versões do Python instaladas no sistema.

```bash
REQUIREMENTS_FILE="requirements.txt"
```
Define a variável `REQUIREMENTS_FILE` que aponta para o arquivo de dependências.

```bash
pip install --upgrade pip
```
Atualiza o gerenciador de pacotes `pip` para a versão mais recente.

```bash
pip install -r $REQUIREMENTS_FILE
```
Instala todas as bibliotecas listadas no arquivo `requirements.txt`.

```bash
echo "--------------------------------------"
echo "Instalação concluída com sucesso!"
echo "Para usar o ambiente, rode: source venv/bin/activate"
echo "--------------------------------------"
```
Exibe mensagens informando que a instalação foi concluída e como ativar o ambiente virtual.

---

## 3. Como Executar o Script

### 3.1 Garantir Permissão de Execução
Antes de rodar o script, é necessário garantir que ele tenha permissão para execução:
```bash
chmod +x install.sh
```
Isso permite que o script seja executado como um arquivo de programa.

### 3.2 Executar o Script
Para rodar o script e configurar o ambiente, use:
```bash
./install.sh
```
Esse comando irá criar e configurar o ambiente virtual automaticamente.

### 3.3 Ativar o Ambiente Virtual
Após a instalação, o ambiente virtual precisa ser ativado antes de rodar qualquer código do projeto:
```bash
source venv/bin/activate
```
Após ativado, o terminal indicará que o ambiente virtual está ativo, geralmente com um prefixo `(venv)` antes do caminho do diretório.

### 3.4 Verificar as Dependências Instaladas
Para verificar se todas as bibliotecas foram instaladas corretamente, utilize:
```bash
pip list
```
Esse comando exibirá a lista de pacotes instalados no ambiente virtual.

---

## 4. Como Desativar o Ambiente Virtual
Caso precise sair do ambiente virtual, basta executar:
```bash
deactivate
```
Isso restaurará o terminal para o ambiente global do sistema.

---

## 5. Conclusão

O script `install.sh` automatiza a instalação das dependências do projeto e garante que o ambiente virtual esteja corretamente configurado. Seguindo as instruções acima, o projeto estará pronto para execução de forma isolada, evitando conflitos com outras versões do Python ou pacotes instalados no sistema.

