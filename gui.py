import TKinterModernThemes as TKMT
from tkinter import ttk
from tkinter.filedialog import askdirectory
from main import borrar

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Font Demo", theme, mode,
                        usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        # Configuração de estilo
        s = ttk.Style()
        s.configure('.', font=('Courier', 20))  # Altera a fonte padrão
        s.configure('Borrador de foto', font=('Helvetica', 12))

        # Frame para os elementos da interface
        self.frame = self.addLabelFrame("Borrador de foto")
        self.frame.Label("Coloque o caminho da pasta")

        # Botão para selecionar a pasta
        self.caminho_pasta = None
        self.frame.Button("Escolha a pasta que contém as fotos", command=self.escolher_pasta)

        # Botão para borramento de fotos, executado somente quando uma pasta é selecionada
        self.frame.Button("Borrar fotos", command=lambda: borrar(self.caminho_pasta))
        
        self.run()

    def escolher_pasta(self):
        self.caminho_pasta = askdirectory(title='Escolha a pasta')
        if self.caminho_pasta:
            print("Pasta selecionada:", self.caminho_pasta)
        else:
            print("Nenhuma pasta foi selecionada.")

# Inicializa a interface
if __name__ == "__main__":
    App("park", "dark")