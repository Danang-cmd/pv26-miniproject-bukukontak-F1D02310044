from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QPushButton, QHBoxLayout,
    QVBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QDate

KATEGORI_LIST = ["Keluarga", "Teman", "Rekan Kerja", "Kenalan", "Lainnya"]

class ContactDialog(QDialog):

    def __init__(self, parent=None, mode: str = "tambah", data: tuple = None):
        super().__init__(parent)
        self.mode = mode
        self.setWindowTitle("Tambah Kontak" if mode == "tambah" else "Edit Kontak")
        self.setMinimumWidth(420)
        self.setModal(True)

        self._build_ui()

        if mode == "edit" and data:
            self._populate(data)

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        judul = QLabel("Tambah Kontak Baru" if self.mode == "tambah" else "Edit Data Kontak")
        judul.setObjectName("dialogTitle")
        judul.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(judul)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan nama lengkap...")
        self.input_nama.setObjectName("formInput")
        form.addRow("Nama *:", self.input_nama)

        self.input_telepon = QLineEdit()
        self.input_telepon.setPlaceholderText("Contoh: 08123456789")
        self.input_telepon.setObjectName("formInput")
        form.addRow("No. Telepon *:", self.input_telepon)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Contoh: nama@email.com")
        self.input_email.setObjectName("formInput")
        form.addRow("Email:", self.input_email)

        self.input_tgl_lahir = QDateEdit()
        self.input_tgl_lahir.setObjectName("formInput")
        self.input_tgl_lahir.setCalendarPopup(True)
        self.input_tgl_lahir.setDate(QDate.currentDate())
        self.input_tgl_lahir.setDisplayFormat("dd MMMM yyyy")
        form.addRow("Tanggal Lahir:", self.input_tgl_lahir)

        self.input_kategori = QComboBox()
        self.input_kategori.setObjectName("formInput")
        self.input_kategori.addItems(KATEGORI_LIST)
        form.addRow("Kategori:", self.input_kategori)

        main_layout.addLayout(form)

        catatan = QLabel("* Field wajib diisi")
        catatan.setObjectName("catatan")
        main_layout.addWidget(catatan)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnSecondary")
        self.btn_batal.clicked.connect(self.reject)

        self.btn_simpan = QPushButton("Simpan" if self.mode == "tambah" else "Perbarui")
        self.btn_simpan.setObjectName("btnPrimary")
        self.btn_simpan.clicked.connect(self._on_simpan)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        main_layout.addLayout(btn_layout)

    def _populate(self, data: tuple):
        _, nama, telepon, email, kategori, tanggal_lahir = data
        self.input_nama.setText(nama or "")
        self.input_telepon.setText(telepon or "")
        self.input_email.setText(email or "")

        idx = self.input_kategori.findText(kategori or "")
        if idx >= 0:
            self.input_kategori.setCurrentIndex(idx)

        if tanggal_lahir:
            qdate = QDate.fromString(tanggal_lahir, "yyyy-MM-dd")
            if qdate.isValid():
                self.input_tgl_lahir.setDate(qdate)

    def _on_simpan(self):
        if not self.input_nama.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama tidak boleh kosong!")
            self.input_nama.setFocus()
            return
        
        if not self.input_telepon.text().strip():
            QMessageBox.warning(self, "Validasi", "Nomor Telepon tidak boleh kosong!")
            self.input_telepon.setFocus()
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "nama": self.input_nama.text().strip(),
            "telepon": self.input_telepon.text().strip(),
            "email": self.input_email.text().strip(),
            "kategori": self.input_kategori.currentText(),
            "tanggal_lahir": self.input_tgl_lahir.date().toString("yyyy-MM-dd"),
        }