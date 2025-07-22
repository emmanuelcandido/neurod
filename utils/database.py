import sqlite3
import os

DB_FILE = os.path.join("data", "neurodeamon.db")

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Cria as tabelas do banco de dados se elas não existirem."""
    if os.path.exists(DB_FILE):
        return

    print("Inicializando banco de dados...")
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de cursos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        directory_path TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_videos INTEGER DEFAULT 0,
        processing_stage TEXT DEFAULT 'not_started',
        metadata_json TEXT
    );
    """)

    # Tabela de operações/logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER REFERENCES courses(id),
        operation_type TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        error_message TEXT,
        details_json TEXT
    );
    """)

    # Tabela de configurações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

if __name__ == '__main__':
    initialize_database()
