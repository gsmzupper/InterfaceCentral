from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QListWidget, QPushButton,
    QLineEdit, QMessageBox, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from products import Products

class ShowWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Softwares")
        self.products = Products()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Mensagem de boas-vindas
        welcome = QLabel("Bem-vindo à Central de Software!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Aba de busca e instalação
        self.tab_search = QWidget()
        self.tabs.addTab(self.tab_search, "Instalar Apps")
        self.init_tab_search()

        # Aba de apps instalados
        self.tab_installed = QWidget()
        self.tabs.addTab(self.tab_installed, "Apps Instalados")
        self.init_tab_installed()

    def init_tab_search(self):
        layout = QVBoxLayout(self.tab_search)
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite o nome do app para buscar...")
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)

        self.btn_search = QPushButton("Buscar")
        self.btn_search.clicked.connect(self.update_search_results)
        search_layout.addWidget(self.btn_search)

        layout.addLayout(search_layout)

        self.list_search = QListWidget()
        layout.addWidget(self.list_search)

        self.btn_install = QPushButton("Instalar")
        self.btn_install.clicked.connect(self.install_app)
        layout.addWidget(self.btn_install)

        self.list_search.clear()  # Começa vazia

    def init_tab_installed(self):
        layout = QVBoxLayout(self.tab_installed)
        self.list_installed = QListWidget()
        layout.addWidget(self.list_installed)

        self.btn_uninstall = QPushButton("Desinstalar")
        self.btn_uninstall.clicked.connect(self.uninstall_app)
        layout.addWidget(self.btn_uninstall)

        self.update_installed_list()

    def update_search_results(self):
        search_text = self.search_input.text().strip().lower()
        self.list_search.clear()
        if not search_text:
            return  # Não mostra nada se o campo está vazio

        found = False
        for app in self.products.list_to_install():
            if search_text in app.lower():
                self.list_search.addItem(app)
                found = True

        if found:
            return

        # Se não encontrou nada, verificar se está instalado
        for app in self.products.list_installed():
            if search_text in app.lower():
                QMessageBox.information(
                    self, "Já instalado", f"O software '{app}' já está instalado."
                )
                return

        # Se não encontrou em nenhum lugar
        QMessageBox.information(
            self, "Não encontrado", f"Software '{self.search_input.text()}' não encontrado."
        )

    def update_installed_list(self):
        self.list_installed.clear()
        for app in self.products.list_installed():
            self.list_installed.addItem(app)

    def install_app(self):
        selected = self.list_search.currentItem()
        if selected:
            app = selected.text()
            if app in self.products.list_installed():
                QMessageBox.information(
                    self, "Atenção", f"O software '{app}' já está instalado."
                )
            else:
                if self.products.install(app):
                    self.update_installed_list()
                    self.list_search.clear()  # Limpa após instalar
                    QMessageBox.information(
                        self, "Sucesso", f"Software '{app}' instalado com sucesso!"
                    )
                else:
                    QMessageBox.warning(
                        self, "Erro", f"Não foi possível instalar '{app}'."
                    )
        else:
            QMessageBox.warning(self, "Atenção", "Selecione um app para instalar.")

    def uninstall_app(self):
        selected = self.list_installed.currentItem()
        if selected:
            app = selected.text()
            if self.products.uninstall(app):
                self.update_installed_list()
                QMessageBox.information(
                    self, "Sucesso", f"Software '{app}' desinstalado com sucesso!"
                )
            else:
                QMessageBox.warning(
                    self, "Erro", f"Não foi possível desinstalar '{app}'."
                )
        else:
            QMessageBox.warning(self, "Atenção", "Selecione um app para desinstalar.")