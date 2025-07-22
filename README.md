# NeuroDeamon Course Processor

Bem-vindo ao **NeuroDeamon Course Processor**! Esta é uma aplicação Python CLI robusta projetada para automatizar o processamento de cursos em vídeo, transformando-os em podcasts com transcrições, resumos gerados por IA e distribuição automática para plataformas como Google Drive e feeds RSS no GitHub.

## 🚀 Como Começar

Siga os passos abaixo para configurar e executar o NeuroDeamon Course Processor em sua máquina.

### 1. Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

*   **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
*   **pip**: Gerenciador de pacotes do Python (geralmente vem com o Python).
*   **ffmpeg**: Ferramenta essencial para conversão de vídeo/áudio. [Guia de Instalação do FFmpeg](https://ffmpeg.org/download.html)
    *   **Windows**: Baixe o executável e adicione-o ao seu PATH do sistema.
    *   **Linux**: `sudo apt update && sudo apt install ffmpeg`
    *   **macOS**: `brew install ffmpeg` (com Homebrew)
*   **Git**: Para gerenciar o repositório GitHub do feed RSS. [Download Git](https://git-scm.com/downloads)

### 2. Configuração do Projeto

1.  **Clone o Repositório (se ainda não o fez):**
    ```bash
    git clone https://github.com/emmanuelcandido/neurod.git
    cd neurod
    ```

2.  **Instale as Dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure suas Chaves de API:**
    O NeuroDeamon utiliza diversas APIs para suas funcionalidades. Você precisará configurar suas chaves:

    *   **OpenAI (Whisper):** Para transcrição de áudio.
    *   **Anthropic (Claude):** Para geração de resumos por IA.
    *   **Google Drive API:** Para upload de arquivos.
    *   **GitHub:** Para atualização do feed RSS.

    No menu principal do aplicativo, vá em `System` -> `Settings` -> `API Keys & Validation` -> `Configure API Keys` para inserir suas chaves. Para o Google Drive, você precisará de um arquivo `credentials.json` (renomeado de `client_secret.json` obtido do Google Cloud Console) na pasta `config/`.

4.  **Inicialize o Repositório GitHub para o Feed RSS:**
    O feed RSS (`cursos.xml`) será versionado em um repositório Git local dentro do projeto. Você precisa inicializá-lo e conectá-lo ao seu repositório remoto (se desejar que as atualizações sejam enviadas para o GitHub).

    ```bash
    cd github/neurodeamon-feeds
    git init
    git remote add origin https://github.com/emmanuelcandido/neurod.git # Substitua pelo URL do seu repositório de feeds
    # Se o repositório remoto já tiver conteúdo, faça um pull inicial:
    # git pull origin master
    cd ../..
    ```

### 3. Executando o Aplicativo

Para iniciar o NeuroDeamon Course Processor, execute o seguinte comando na raiz do projeto:

```bash
python main.py
```

## 🎓 Funcionalidades Principais

O aplicativo oferece um menu interativo com as seguintes opções:

*   **Course Processor:** Gerencia o fluxo completo de processamento de cursos, desde a conversão de vídeo até a distribuição, além de operações individuais como transcrição, resumo por IA e geração de timestamps.
*   **YouTube Manager (Em Breve):** Funcionalidades futuras para gerenciar conteúdo do YouTube.
*   **Feed Manager (Em Breve):** Funcionalidades futuras para gerenciar feeds de conteúdo.
*   **Snipd Tools (Em Breve):** Ferramentas adicionais.
*   **Settings:** Configurações do aplicativo, incluindo gerenciamento de chaves de API, diretórios de saída e preferências de processamento.
*   **Monitor (Em Breve):** Monitoramento de processos.
*   **Logs (Em Breve):** Visualização de logs do sistema.

## 🛠️ Uso

Navegue pelos menus usando os números correspondentes às opções. O aplicativo guiará você através das entradas necessárias para cada operação.

### Exemplo de Fluxo (Process Complete Course):

1.  No menu principal, selecione `1` para `Course Processor`.
2.  No submenu `Course Processor`, selecione `1` para `Process Complete Course`.
3.  O aplicativo pedirá o nome do curso, o diretório de origem dos vídeos e o diretório de saída. Forneça os caminhos completos.
4.  O NeuroDeamon iniciará o processamento sequencial, exibindo o progresso e registrando as etapas no banco de dados.

## 🐛 Resolução de Problemas Comuns

*   **`ffmpeg not found`**: Certifique-se de que o `ffmpeg` está instalado e seu caminho está configurado corretamente nas variáveis de ambiente do sistema.
*   **Erros de API**: Verifique suas chaves de API na seção `Settings` -> `API Keys & Validation`. Certifique-se de que estão corretas e que você tem créditos/permissões suficientes.
*   **Problemas de Autenticação Google Drive**: Se o `token.json` não for gerado automaticamente, siga as instruções no console para autorizar o acesso via navegador e insira o código de autorização.
*   **`GitPython` erros**: Certifique-se de que o diretório `github/neurodeamon-feeds` é um repositório Git válido e que você tem permissões de escrita.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no repositório do GitHub.

---

**NeuroDeamon Course Processor** - Automatizando seu aprendizado e distribuição de conteúdo.