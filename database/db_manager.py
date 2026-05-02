import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contacts.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                nama          TEXT    NOT NULL,
                telepon       TEXT,
                email         TEXT,
                kategori      TEXT,
                tanggal_lahir TEXT
            )
        """)
        conn.commit()

def create_contact(nama: str, telepon: str, email: str,
                   kategori: str, tanggal_lahir: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (nama, telepon, email, kategori, tanggal_lahir)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, telepon, email, kategori, tanggal_lahir))
        conn.commit()
        return cursor.lastrowid

def read_all_contacts() -> list:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY nama COLLATE NOCASE")
        return cursor.fetchall()

def search_contacts(keyword: str) -> list:
    pattern = f"%{keyword}%"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM contacts
            WHERE nama    LIKE ?
               OR telepon LIKE ?
               OR email   LIKE ?
            ORDER BY nama COLLATE NOCASE
        """, (pattern, pattern, pattern))
        return cursor.fetchall()

def get_contact_by_id(contact_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        return cursor.fetchone()

def update_contact(contact_id: int, nama: str, telepon: str, email: str,
                   kategori: str, tanggal_lahir: str) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contacts
            SET nama=?, telepon=?, email=?, kategori=?, tanggal_lahir=?
            WHERE id=?
        """, (nama, telepon, email, kategori, tanggal_lahir, contact_id))
        conn.commit()

def delete_contact(contact_id: int) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()