import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QRadioButton, QPushButton, QButtonGroup)
from PyQt6.QtCore import Qt

class Questionnaire(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Přístupný dotazník 1.0")
        self.setGeometry(200, 200, 500, 250)

        # Profil uživatele
        self.profile = {
            "user_name": "",
            "assistive_tech": {"screen_reader": "", "magnification": False, "speech": False},
            "preferences": {"verbosity": "normal", "action_feedback": True, "announce_shortcuts": True},
            "interface": {"input_method": [], "text_size": "normal"},
            "profile_scope": "local"
        }

        # Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Otázky jako seznam funkcí
        self.questions = [
            self.ask_screen_reader,
            self.ask_magnification,
            self.ask_speech,
            self.ask_verbosity,
            self.ask_action_feedback,
            self.ask_announce_shortcuts,
            self.ask_input_method,
            self.ask_text_size,
            self.ask_profile_scope
        ]
        self.current_question = 0
        self.questions[self.current_question]()

    def clear_layout(self):
        """Odstraní všechny widgety z layoutu"""
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["NVDA", "Narrator", "JAWS", "Jiný / nevím"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.main_layout.addWidget(btn)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_screen_reader(group))
        self.main_layout.addWidget(next_btn)
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
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.main_layout.addWidget(yes)
        self.main_layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_magnification(group))
        self.main_layout.addWidget(next_btn)
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
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.main_layout.addWidget(yes)
        self.main_layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_speech(group))
        self.main_layout.addWidget(next_btn)
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
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["minimal", "normal", "verbose"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.main_layout.addWidget(btn)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_verbosity(group))
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_verbosity(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["preferences"]["verbosity"] = btn.text()
                break
        self.next_question()

    def ask_action_feedback(self):
        self.clear_layout()
        label = QLabel("Chceš slyšet potvrzení akcí? (např. Uloženo, Hotovo)")
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.main_layout.addWidget(yes)
        self.main_layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_action_feedback(group))
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_action_feedback(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["preferences"]["action_feedback"] = (btn.text() == "Ano")
                break
        self.next_question()

    def ask_announce_shortcuts(self):
        self.clear_layout()
        label = QLabel("Chceš, aby aplikace hlásila klávesové zkratky?")
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        yes = QRadioButton("Ano")
        no = QRadioButton("Ne")
        group.addButton(yes)
        group.addButton(no)
        self.main_layout.addWidget(yes)
        self.main_layout.addWidget(no)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_announce_shortcuts(group))
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_announce_shortcuts(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["preferences"]["announce_shortcuts"] = (btn.text() == "Ano")
                break
        self.next_question()

    def ask_input_method(self):
        self.clear_layout()
        label = QLabel("Jak ovládáš aplikace nejčastěji? (může být víc možností)")
        self.main_layout.addWidget(label)

        self.input_buttons = []
        options = ["Klávesnice", "Myš", "Dotyk (tablet)"]
        for opt in options:
            btn = QRadioButton(opt)
            self.main_layout.addWidget(btn)
            self.input_buttons.append(btn)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(self.save_input_method)
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_input_method(self):
        selected = [btn.text() for btn in self.input_buttons if btn.isChecked()]
        self.profile["interface"]["input_method"] = selected
        self.next_question()

    def ask_text_size(self):
        self.clear_layout()
        label = QLabel("Jak chceš zobrazovat text?")
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["small", "normal", "large", "extra"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.main_layout.addWidget(btn)

        next_btn = QPushButton("Další")
        next_btn.clicked.connect(lambda: self.save_text_size(group))
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_text_size(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["interface"]["text_size"] = btn.text()
                break
        self.next_question()

    def ask_profile_scope(self):
        self.clear_layout()
        label = QLabel("Má se tenhle profil uložit pro všechny aplikace nebo jen tuto?")
        self.main_layout.addWidget(label)

        group = QButtonGroup(self)
        options = ["global", "local"]
        for opt in options:
            btn = QRadioButton(opt)
            group.addButton(btn)
            self.main_layout.addWidget(btn)

        next_btn = QPushButton("Dokončit")
        next_btn.clicked.connect(lambda: self.save_profile_scope(group))
        self.main_layout.addWidget(next_btn)
        self.show()

    def save_profile_scope(self, group):
        for btn in group.buttons():
            if btn.isChecked():
                self.profile["profile_scope"] = btn.text()
                break
        self.next_question()

    # ----------------- Konec -----------------
    def finish(self):
        with open("profile.json", "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

        self.clear_layout()
        label = QLabel("Hotovo! Profil byl uložen jako 'profile.json'.")
        self.main_layout.addWidget(label)
        self.show()

# ----------------- Spuštění -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Questionnaire()
    window.show()
    sys.exit(app.exec())
