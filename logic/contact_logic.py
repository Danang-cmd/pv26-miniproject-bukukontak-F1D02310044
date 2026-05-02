import re
from database import db_manager

def validate_contact(nama: str, telepon: str, email: str) -> tuple[bool, str]:
    if not nama.strip():
        return False, "Nama tidak boleh kosong."

    if not telepon.strip():
        return False, "Nomor telepon tidak boleh kosong."
        
    if not re.fullmatch(r"[0-9+\-\s()]{7,20}", telepon.strip()):
        return False, "Format nomor telepon tidak valid."

    if email.strip() and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip()):
        return False, "Format email tidak valid."

    return True, ""

def tambah_kontak(nama: str, telepon: str, email: str,
                  kategori: str, tanggal_lahir: str) -> tuple[bool, str]:
    valid, pesan = validate_contact(nama, telepon, email)
    if not valid:
        return False, pesan
    db_manager.create_contact(nama.strip(), telepon.strip(), email.strip(),
                               kategori, tanggal_lahir)
    return True, "Kontak berhasil ditambahkan."

def edit_kontak(contact_id: int, nama: str, telepon: str, email: str,
                kategori: str, tanggal_lahir: str) -> tuple[bool, str]:
    valid, pesan = validate_contact(nama, telepon, email)
    if not valid:
        return False, pesan
    db_manager.update_contact(contact_id, nama.strip(), telepon.strip(),
                               email.strip(), kategori, tanggal_lahir)
    return True, "Kontak berhasil diperbarui."

def hapus_kontak(contact_id: int) -> None:
    db_manager.delete_contact(contact_id)

def ambil_semua_kontak() -> list:
    return db_manager.read_all_contacts()

def cari_kontak(keyword: str) -> list:
    return db_manager.search_contacts(keyword)