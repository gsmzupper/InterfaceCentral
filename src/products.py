class Products:
    """Classe para gerenciar produtos disponíveis para instalar e já instalados."""

    def __init__(self):
        self.to_install = ["git", "intelliJ", "pycharme", "VSCode"]
        self.installed = []

    def list_to_install(self):
        return self.to_install

    def list_installed(self):
        return self.installed

    def install(self, app):
        if app in self.to_install:
            self.to_install.remove(app)
            self.installed.append(app)
            return True
        return False

    def uninstall(self, app):
        if app in self.installed:
            self.installed.remove(app)
            self.to_install.append(app)
            return True
        return False