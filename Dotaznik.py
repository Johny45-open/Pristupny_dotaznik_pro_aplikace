import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QRadioButton, QPushButton, QButtonGroup)
from PyQt6.QtCore import Qt

class Questionnaire(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Přístupný dotazník")
        self.setGeometry(200, 200, 500, 200)

        # Profil uživatele
        self.profile = {
            "user_name": "",
            "assistive_tech": {"screen_reader": "", "magnification": False, "speech": False},
            "preferences": {"verbosity": "normal", "action_feedback": True, "announce_shortcuts": True},
            "interface": {"input_method": [], "text_size": "normal"},
            "profile_scope": "local"
        }

        # Otázky jako seznam funkcí
        self.questions = [
            self.ask_screen_reader,
            self.ask_magnification,
            self.ask_speech,
            self.ask_verbosity
        ]
        self.current_question = 0
        self.questions[self.current_question]()

    def clear_layout(self):
        """Odstraní všechny widgety z layoutu"""
        if hasattr(self, 'layout'):
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.questions[self.current_question]()
        else:
            self.finish()

    # ----------------- Otázky -----------------
    def ask_screen_reader(self):
        self.clear_layout()
        label = QLabel("Jaký odečítač používáš?")
        self.layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["NVDA", "Narrator", "JAWS", "Jiný / nevím"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.layout.addWidget(btn)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_screen_reader(group))
        self.layout.addWidget(next_btn)
        self.show()

    def save_screen_reader(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["assistive_tech"]["screen_reader"] = btn.text()
                break
        self.next_question()

    def ask_magnification(self):
        self.clear_layout()
        label = QLabel("Používáš zvětšení?")
        self.layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.layout.addWidget(yes)
        self.layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_magnification(group))
        self.layout.addWidget(next_btn)
        self.show()

    def save_magnification(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["assistive_tech"]["magnification"] = (btn.text() == "Ano")
                break
        self.next_question()

    def ask_speech(self):
        self.clear_layout()
        label = QLabel("Používáš hlasový výstup?")
        self.layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.layout.addWidget(yes)
        self.layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_speech(group))
        self.layout.addWidget(next_btn)
        self.show()

    def save_speech(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["assistive_tech"]["speech"] = (btn.text() == "Ano")
                break
        self.next_question()

    def ask_verbosity(self):
        self.clear_layout()
        label = QLabel("Jak moc má být aplikace ukecaná?")
        self.layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["minimal", "normal", "verbose"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.layout.addWidget(btn)

        next_btn = QPushButton("Dokončit")
        next_btn.clicked.connect(lambda: self.save_verbosity(group))
        self.layout.addWidget(next_btn)
        self.show()

    def save_verbosity(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["preferences"]["verbosity"] = btn.text()
                break
        self.next_question()

    # ----------------- Konec -----------------
    def finish(self):
        # uloží profil do JSON souboru
        with open("profile.json", "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

        self.clear_layout()
        label = QLabel("Hotovo! Profil byl uložen jako 'profile.json'.")
        self.layout.addWidget(label)
        self.show()

# ----------------- Spuštění -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Questionnaire()
    window.show()
    sys.exit(app.exec())
