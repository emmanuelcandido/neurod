# NeuroDeamon Course Processor - TODO

## Fase 1: Estrutura e Configuração Inicial (P0)

- [x] 1.1. Criar a estrutura de diretórios completa (`data/`, `config/`, `prompts/`, `services/`, `utils/`, `temp/`, `github/`).
- [x] 1.2. Criar o arquivo `main.py` com a estrutura básica do menu principal, utilizando as funções do `design.md`.
- [x] 1.3. Criar o arquivo `database.py` em `utils/` para inicializar o banco de dados SQLite e as tabelas (`courses`, `operations`, `settings`).
- [x] 1.4. Criar os arquivos de configuração iniciais (`settings.json`, `api_keys.json`, `directories.json`) em `config/` com valores padrão.
- [x] 1.5. Criar o arquivo `requirements.txt` com todas as dependências Python necessárias.
- [x] 1.6. Instalar as dependências do `requirements.txt`.
- [x] 1.7. Implementar a lógica de inicialização no `main.py` que verifica/cria o banco de dados e os arquivos de configuração.
- [ ] 1.8. **COMMIT: "feat: Initial project structure and setup"**

## Fase 2: Implementação do Menu e Navegação (P0)

- [x] 2.1. Implementar o menu principal em `main.py` conforme o `briefing.md`, com navegação para os submenus.
- [x] 2.2. Criar os módulos para cada submenu (`course_processor.py`, `settings.py`, etc.).
- [x] 2.3. Implementar a estrutura dos submenus `Course Processor` e `Settings` com todas as opções listadas, mesmo que as funções ainda não façam nada.
- [x] 2.4. Garantir que a navegação (entrar e voltar com '0') funcione perfeitamente entre todos os menus.
- [ ] 2.5. **COMMIT: "feat: Implement full UI menu navigation"**

## Fase 3: Funcionalidades de Configuração (P1)

- [x] 3.1. Implementar a tela de "API Keys & Validation" no `settings.py`.
- [x] 3.2. Criar uma função em `utils/` para criptografar/descriptografar as chaves de API.
- [x] 3.3. Implementar a lógica para salvar e carregar as chaves de API do arquivo `api_keys.json`.
- [x] 3.4. Implementar a função de validação que testa cada API (faz uma chamada simples) e mostra o status.
- [ ] 3.5. Implementar as outras telas de configuração (`Voice Settings`, `Output Directory`, etc.) para salvar os dados no `settings.json` ou `database.py`.
- [ ] 3.6. **COMMIT: "feat: Implement settings and API key management"**

## Fase 4: Implementação das Operações Individuais (Core) (P0)

- [x] 4.1. **Conversão:** Criar `video_service.py`. Implementar `Convert Courses to Audio` usando `ffmpeg`. A função deve escanear um diretório, encontrar vídeos e convertê-los para MP3.
- [x] 4.2. **Transcrição:** Criar `transcription_service.py`. Implementar `Transcribe Audio Files` usando a API do Whisper.
- [x] 4.3. **Resumos:** Criar `ai_service.py`. Implementar `Generate AI Course Summaries` usando a API da Anthropic (Claude). A função deve ler prompts da pasta `prompts/`.
- [x] 4.4. **Unificação:** Criar `audio_service.py`. Implementar `Create Unified Audio` para juntar múltiplos MP3s em um só.
- [x] 4.5. **Timestamps:** No `audio_service.py`, implementar `Generate Timestamps Only`.
- [x] 4.6. **TTS:** Criar `tts_service.py`. Implementar `Generate Course TTS Audio Notes` usando `edge-tts`.
- [ ] 4.7. **COMMIT: "feat: Implement individual processing operations"**

## Fase 5: Integrações com a Nuvem (P1)

- [x] 5.1. **Google Drive:** Criar `gdrive_service.py`. Implementar `Upload Course to Google Drive`.
- [x] 5.2. **RSS:** Criar `rss_service.py`. Implementar `Update courses.xml`.
- [x] 5.3. **GitHub:** Criar `github_service.py`. Implementar `Update GitHub Repository` para commitar e dar push no feed RSS.
- [ ] 5.4. **COMMIT: "feat: Implement cloud distribution services (Drive, RSS, GitHub)"**

## Fase 6: Orquestração do Fluxo Completo (P0)

- [x] 6.1. No `course_processor.py`, implementar a lógica principal de `Process Complete Course`.
- [x] 6.2. Esta função deve chamar os serviços individuais na sequência correta.
- [x] 6.3. Implementar o sistema de checkpoints no banco de dados (`courses` e `operations`) após cada etapa.
- [x] 6.4. Implementar a lógica para exibir o progresso geral usando as barras de progresso do `design.md`.
- [ ] 6.5. **COMMIT: "feat: Implement the complete course processing pipeline"**

## Fase 7: Robustez e Recuperação de Falhas (P1)

- [x] 7.1. Implementar a lógica de detecção de processos interrompidos na inicialização do app.
- [x] 7.2. Implementar a função de retomada automática, lendo o último checkpoint do banco de dados.
- [x] 7.3. Adicionar tratamento de erro robusto (try/except) em todas as chamadas de API e operações de arquivo.
- [x] 7.4. Implementar o sistema de logs em `utils/logger.py` e integrá-lo em todo o aplicativo.
- [ ] 7.5. **COMMIT: "feat: Implement failure recovery and robust logging"**

## Fase 8: Gerenciamento de Cursos e Finalização (P2)

- [x] 8.1. Implementar as funções de gerenciamento: `Course Status Check`, `Forget Course`, `Clear All Data`.
- [x] Corrigir `SyntaxError` em `ui/course_processor_menu.py`.
- [x] 8.2. Criar um `README.md` final com as instruções de uso para o usuário.
- [x] 8.3. Realizar uma limpeza final do código e verificar se todos os critérios de sucesso foram atendidos.
- [x] 8.4. **COMMIT: "feat: Add course management tools and finalize project"**
