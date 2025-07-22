# services/security_service.py

import base64
import json
import os

API_KEYS_FILE = os.path.join("config", "api_keys.json")
# Chave simples para "embaralhar" os dados. Em um app real, isso seria mais robusto.
SECRET_KEY = "neurodeamon_secret_key".encode('utf-8')

def _xor_cipher(data, key):
    """Criptografia XOR simples."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt_key(raw_key: str) -> str:
    """Criptografa uma chave usando XOR e Base64."""
    if not raw_key:
        return ""
    encrypted = _xor_cipher(raw_key.encode('utf-8'), SECRET_KEY)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_key(encrypted_key: str) -> str:
    """Descriptografa uma chave."""
    if not encrypted_key:
        return ""
    try:
        decoded_b64 = base64.b64decode(encrypted_key.encode('utf-8'))
        decrypted = _xor_cipher(decoded_b64, SECRET_KEY)
        return decrypted.decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        # Se a chave estiver em texto plano (não criptografada), retorne-a diretamente
        return encrypted_key

def load_api_keys(encrypted: bool = True) -> dict:
    """Carrega as chaves de API do arquivo JSON."""
    if not os.path.exists(API_KEYS_FILE):
        return {}
    
    with open(API_KEYS_FILE, 'r') as f:
        keys = json.load(f)
    
    if encrypted:
        return {key: decrypt_key(value) for key, value in keys.items()}
    return keys

def save_api_keys(keys: dict):
    """Salva as chaves de API no arquivo JSON, criptografando-as."""
    encrypted_keys = {key: encrypt_key(value) for key, value in keys.items()}
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(encrypted_keys, f, indent=4)

# Exemplo de como usar:
if __name__ == "__main__":
    # Criar um arquivo de chaves de exemplo
    sample_keys = {
        "openai_api_key": "sk-12345",
        "anthropic_api_key": "anth-xyz",
        "gemini_api_key": "gem-abc",
        "github_token": "ghp_def"
    }
    save_api_keys(sample_keys)
    print(f"Arquivo {API_KEYS_FILE} salvo com chaves criptografadas.")

    # Carregar e descriptografar
    loaded_keys = load_api_keys()
    print("Chaves carregadas e descriptografadas:")
    for name, key in loaded_keys.items():
        print(f"  {name}: {key}")
