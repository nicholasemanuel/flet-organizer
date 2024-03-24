import flet as ft
import os

def main(page: ft.Page):

    # pasta inicial
    caminho_inicial = ft.TextField(
        label="Pasta inicial",
        expand=1,
        autofocus=True,
    )

    # botão para escolher a pasta
    botao_escolher_pasta = ft.buttons.ElevatedButton(  # Use buttons.ElevatedButton
        text="Escolher pasta",
        on_click=lambda _: _escolher_pasta(page, caminho_inicial)
    )

    # Área de texto para feedback
    texto_feedback = ft.Text(
        expand=1,
        text_color="red",
        max_lines=5,
    )

    # dicionário de pastas e extensões
    locais = {
        "imagens": [".png", ".jpg"],
        "planilhas": [".xlsx"],
        "pdfs": [".pdf"],
        "documentos": [".doc", ".docx"],
        "textos": [".txt"],
        "slides": [".pptx"],
    }

    def _escolher_pasta(page: ft.Page, campo_caminho: ft.TextField):
        caminho = ft.dialog.show_folder_picker(title="Selecione a pasta")
        if caminho:
            campo_caminho.value = caminho

    def _organizar_arquivos(page: ft.Page, caminho: str, locais: dict, texto_feedback: ft.Text):
        try:
            texto_feedback.value = ""
            lista_arquivos = os.listdir(caminho)
            for arquivo in lista_arquivos:
                nome, extensao = os.path.splitext(os.path.join(caminho, arquivo))
                pasta_destino = _obter_pasta_destino(extensao, locais)
                if pasta_destino:
                    novo_caminho = os.path.join(caminho, pasta_destino, arquivo)
                    os.rename(os.path.join(caminho, arquivo), novo_caminho)
                    texto_feedback.value += f"Arquivo {arquivo} movido para {pasta_destino}\n"
        except Exception as e:
            texto_feedback.value = f"Erro: {e}"

    def _obter_pasta_destino(extensao: str, locais: dict) -> str:
        for pasta, extensoes in locais.items():
            if extensao in extensoes:
                return pasta
        return None

    # botão para organizar os arquivos
    botao_organizar = ft.buttons.ElevatedButton(  # Use buttons.ElevatedButton
        text="Organizar arquivos",
        on_click=lambda _: _organizar_arquivos(page, caminho_inicial.value, locais, texto_feedback)
    )

    # conteúdo da página
    page.content = ft.Column(
        [
            caminho_inicial,
            botao_escolher_pasta,
            botao_organizar,
            texto_feedback,
        ],
        spacing=10,
    )

ft.app(target=main)
