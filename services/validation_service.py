# services/validation_service.py

import anthropic
from services.security_service import load_api_keys
from utils.logger import logger

def test_anthropic_api() -> (bool, str):
    """Testa a conexão com a API da Anthropic (Claude)."""
    keys = load_api_keys()
    api_key = keys.get("anthropic_api_key")

    if not api_key or api_key == "your-key-here":
        logger.warning("Anthropic API key not set or is default. Skipping test.")
        return False, "API key not set."

    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=10.0)
        # Envia uma mensagem simples e de baixo custo para testar a autenticação
        client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello"}]
        )
        logger.info("Anthropic API connection successful.")
        return True, "Connection successful."
    except anthropic.AuthenticationError as e:
        logger.error(f"Anthropic Authentication failed: {e.__class__.__name__}")
        return False, f"Authentication failed: {e.__class__.__name__}"
    except Exception as e:
        logger.error(f"An error occurred during Anthropic API test: {e}")
        return False, f"An error occurred: {str(e)}"

# Adicionar funções de teste para outras APIs (OpenAI, Gemini, etc.) aqui.
