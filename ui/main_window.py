import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QStatusBar, QMenuBar, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QFont

from ui.contact_dialog import ContactDialog
from logic import contact_logic

NAMA_MAHASISWA = "Danang Adiwijaya"
NIM_MAHASISWA  = "NIM: F1D02310044"
NAMA_APLIKASI  = "Buku Kontak Digital"
DESKRIPSI_APP  = (
    "Aplikasi manajemen kontak berbasis desktop menggunakan PySide6 dan SQLite. "
    "Mendukung penambahan, pengeditan, penghapusan, dan pencarian kontak."
)

KOLOM_HEADER = ["ID", "Nama", "No. Telepon", "Email", "Kategori", "Tanggal Lahir"]
COL_ID, COL_NAMA, COL_TEL, COL_EMAIL, COL_KAT, COL_TGL = range(6)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(NAMA_APLIKASI)
        self.setMinimumSize(900, 600)
        self._build_menu_bar()
        self._build_central()
        self._build_status_bar()
        self.load_table()

    def _build_menu_bar(self):
        menu_bar = self.menuBar()

        menu_kontak = menu_bar.addMenu("Kontak")

        act_tambah = QAction("Tambah Kontak Baru", self)
        act_tambah.setShortcut("Ctrl+N")
        act_tambah.triggered.connect(self.aksi_tambah) 
        menu_kontak.addAction(act_tambah)

        act_edit = QAction("Edit Kontak", self)
        act_edit.setShortcut("Ctrl+E")
        act_edit.triggered.connect(self.aksi_edit)
        menu_kontak.addAction(act_edit)

        act_hapus = QAction("Hapus Kontak", self)
        act_hapus.setShortcut("Del")
        act_hapus.triggered.connect(self.aksi_hapus)
        menu_kontak.addAction(act_hapus)

        menu_kontak.addSeparator()

        act_keluar = QAction("Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_kontak.addAction(act_keluar)

        menu_tentang = menu_bar.addMenu("Tentang Aplikasi")
        act_tentang = QAction("Informasi Aplikasi", self)
        act_tentang.triggered.connect(self.tampil_tentang)
        menu_tentang.addAction(act_tentang)

    def _build_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 14, 20, 14)

        left_header = QVBoxLayout()
        lbl_app = QLabel(NAMA_APLIKASI)
        lbl_app.setObjectName("appTitle")
        lbl_deskripsi = QLabel("Simpan & kelola kontak Anda dengan mudah")
        lbl_deskripsi.setObjectName("appSubtitle")
        left_header.addWidget(lbl_app)
        left_header.addWidget(lbl_deskripsi)

        right_header = QVBoxLayout()
        right_header.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_nama = QLabel(NAMA_MAHASISWA)
        self.lbl_nama.setObjectName("labelNama")
        self.lbl_nama.setAlignment(Qt.AlignRight)
        self.lbl_nim = QLabel(NIM_MAHASISWA)
        self.lbl_nim.setObjectName("labelNIM")
        self.lbl_nim.setAlignment(Qt.AlignRight)
        right_header.addWidget(self.lbl_nama)
        right_header.addWidget(self.lbl_nim)

        header_layout.addLayout(left_header, stretch=1)
        header_layout.addLayout(right_header)
        root.addWidget(header)

        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbarFrame")
        toolbar = QHBoxLayout(toolbar_frame)
        toolbar.setContentsMargins(16, 10, 16, 10)
        toolbar.setSpacing(10)

        self.input_cari = QLineEdit()
        self.input_cari.setObjectName("searchInput")
        self.input_cari.setPlaceholderText("🔍  Cari nama, telepon, atau email...")
        self.input_cari.textChanged.connect(self._on_cari) 

        self.btn_tambah = QPushButton("＋  Tambah")
        self.btn_tambah.setObjectName("btnPrimary")
        self.btn_tambah.clicked.connect(self.aksi_tambah)  

        self.btn_edit = QPushButton("✎  Edit")
        self.btn_edit.setObjectName("btnSecondary")
        self.btn_edit.clicked.connect(self.aksi_edit)  

        self.btn_hapus = QPushButton("✕  Hapus")
        self.btn_hapus.setObjectName("btnDanger")
        self.btn_hapus.clicked.connect(self.aksi_hapus)  

        toolbar.addWidget(self.input_cari, stretch=1)
        toolbar.addWidget(self.btn_tambah)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_hapus)
        root.addWidget(toolbar_frame)

        self.table = QTableWidget()
        self.table.setObjectName("contactTable")
        self.table.setColumnCount(len(KOLOM_HEADER))
        self.table.setHorizontalHeaderLabels(KOLOM_HEADER)
        self.table.setColumnHidden(COL_ID, True)        
        self.table.horizontalHeader().setSectionResizeMode(COL_NAMA, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(COL_TEL,  QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(COL_EMAIL, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(COL_KAT,  QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(COL_TGL,  QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self.aksi_edit)  
        root.addWidget(self.table)

    def _build_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.lbl_status = QLabel()
        self.status_bar.addWidget(self.lbl_status)

    def set_status(self, pesan: str, ms: int = 3000):
        self.lbl_status.setText(pesan)
        QTimer.singleShot(ms, lambda: self.lbl_status.setText(""))

    def load_table(self, keyword: str = ""):
        if keyword:
            rows = contact_logic.cari_kontak(keyword)
        else:
            rows = contact_logic.ambil_semua_kontak()
        
        self.table.setRowCount(0)
        for row_data in rows:
            contact_id, nama, telp, email, kat, tgl = row_data
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, COL_ID, QTableWidgetItem(str(contact_id)))
            self.table.setItem(row, COL_NAMA, QTableWidgetItem(nama))
            self.table.setItem(row, COL_TEL, QTableWidgetItem(telp))
            self.table.setItem(row, COL_EMAIL, QTableWidgetItem(email))
            self.table.setItem(row, COL_KAT, QTableWidgetItem(kat))
            self.table.setItem(row, COL_TGL, QTableWidgetItem(tgl))
            
        total = self.table.rowCount()
        self.set_status(f"Total kontak: {total}", 0)

    def _on_cari(self, text: str):
        self.load_table(keyword=text)

    def aksi_tambah(self):
        dialog = ContactDialog(self, mode="tambah")
        if dialog.exec():
            d = dialog.get_data()
            ok, pesan = contact_logic.tambah_kontak(
                d["nama"], d["telepon"], d["email"],
                d["kategori"], d["tanggal_lahir"]
            )
            if ok:
                self.load_table(self.input_cari.text())
                self.set_status(f"✔  {pesan}")
            else:
                QMessageBox.warning(self, "Gagal Menyimpan", pesan)

    def aksi_edit(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.information(self, "Pilih Kontak", "Silakan pilih kontak yang ingin diedit.")
            return

        contact_id = int(self.table.item(selected, COL_ID).text())

        from database.db_manager import get_contact_by_id
        data = get_contact_by_id(contact_id)

        dialog = ContactDialog(self, mode="edit", data=data)
        if dialog.exec():
            d = dialog.get_data()
            ok, pesan = contact_logic.edit_kontak(
                contact_id, d["nama"], d["telepon"], d["email"],
                d["kategori"], d["tanggal_lahir"]
            )
            if ok:
                self.load_table(self.input_cari.text())
                self.set_status(f"✔  {pesan}")
            else:
                QMessageBox.warning(self, "Gagal Memperbarui", pesan)

    def aksi_hapus(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.information(self, "Pilih Kontak", "Silakan pilih kontak yang ingin dihapus.")
            return

        nama = self.table.item(selected, COL_NAMA).text()
        contact_id = int(self.table.item(selected, COL_ID).text())

        jawab = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus kontak:\n\n  {nama}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if jawab == QMessageBox.Yes:
            contact_logic.hapus_kontak(contact_id)
            self.load_table(self.input_cari.text())
            self.set_status(f"✔  Kontak '{nama}' berhasil dihapus.")

    def tampil_tentang(self):
        QMessageBox.about(
            self,
            "Tentang Aplikasi",
            f"<h3>{NAMA_APLIKASI}</h3>"
            f"<p>{DESKRIPSI_APP}</p>"
            f"<hr>"
            f"<p><b>Nama:</b> {NAMA_MAHASISWA}<br>"
            f"<b>NIM:</b> {NIM_MAHASISWA.replace('NIM: ', '')}<br>"
            f"<b>Teknologi:</b> Python · PySide6 · SQLite</p>"
        )