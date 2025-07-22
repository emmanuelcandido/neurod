# utils/logger.py

import logging
import os
from datetime import datetime

LOG_DIR = os.path.join("data", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"neurodeamon_{datetime.now().strftime('%Y%m%d')}.log")

def setup_logging():
    """Configura o sistema de logging."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO, # Nível padrão de logging
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE), # Log para arquivo
            logging.StreamHandler() # Log para console
        ]
    )

    # Desabilita logs de bibliotecas de terceiros que podem ser muito verbosos
    logging.getLogger('googleapiclient').setLevel(logging.WARNING)
    logging.getLogger('oauthlib').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('pydub').setLevel(logging.WARNING)
    logging.getLogger('git').setLevel(logging.WARNING)

    return logging.getLogger('NeuroDeamon')

logger = setup_logging()

# Exemplo de uso:
if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message (won't show with INFO level).")
