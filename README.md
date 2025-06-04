# 🎮 Automatic Player with Playwright

[🇧🇷 Português](#-pt-br---instruções-em-português) | [🇺🇸 English](#-en---instructions-in-english)

---

## 🇧🇷 PT-BR — Instruções em Português

### 📌 Descrição

Código desenvolvido para automatizar a reprodução de vídeos. O script:

* Acessa automaticamente as URLs dos vídeos.
* Detecta a página de login e realiza o login com suas credenciais.
* Fecha pop-ups automáticos que aparecem.
* Reproduz os vídeos automaticamente.
* Detecta se o vídeo terminou ou travou.
* Passa automaticamente para o próximo vídeo da lista.

### ⚙️ Requisitos

* Python 3.7+
* Playwright

### 📦 Instalação

```bash
pip install playwright
playwright install
```

### 🚀 Execução

1. Clone ou copie o repositório com o código.
2. Edite as variáveis `EMAIL`, `SENHA` e `video_urls` no código.
3. Execute o script:

```bash
python nome_do_arquivo.py
```

> Certifique-se de que o Chrome está instalado no caminho definido em `chrome_path`, ou altere para o caminho correto.

### 📁 Estrutura

* `EMAIL` e `SENHA`: suas credenciais de login.
* `video_urls`: array com os links dos vídeos a serem assistidos.
* `aguardar_video_terminar`: função que monitora o progresso do vídeo e avança para o próximo quando terminar.
* Lógica para login, fechamento de pop-ups e autoplay.

---

## 🇺🇸 EN — Instructions in English

### 📌 Description

This script automates video playback. It:

* Automatically accesses video URLs.
* Detects and completes login if needed.
* Closes any pop-ups that appear.
* Automatically starts video playback.
* Detects if the video has finished or stalled.
* Proceeds to the next video in the list.

### ⚙️ Requirements

* Python 3.7+
* Playwright

### 📦 Installation

```bash
pip install playwright
playwright install
```

### 🚀 Run

1. Clone or copy this repository.
2. Edit the variables `EMAIL`, `SENHA`, and `video_urls` in the script.
3. Run the script:

```bash
python filename.py
```

> Make sure Chrome is installed at the `chrome_path`, or update it with the correct path.

### 📁 Structure

* `EMAIL` and `SENHA`: your login credentials.
* `video_urls`: array of video links to watch.
* `aguardar_video_terminar`: function that monitors video progress and proceeds when done.
* Logic for login, pop-up dismissal, and autoplay.
