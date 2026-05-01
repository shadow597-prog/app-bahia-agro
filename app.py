import flet as ft
import os

def main(page: ft.Page):
    # Configurações da Página
    page.title = "SENNA - GESTÃO AGRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#000000" # Fundo Preto solicitado
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    # Cores da Marca
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_CARD = "#121212"

    # --- ELEMENTOS DE INTERFACE ---
    
    # Logo e Título (Sincronizado: Logo na direita)
    header = ft.Row([
        ft.Text("BAHIA AGRO", size=18, weight="w500", color="#666666"),
        ft.Text("SENNA", size=26, weight="bold", italic=True, color=COR_BANANA)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Feedback de Resposta
    texto_feedback = ft.Text("", size=16, weight="bold")

    # Campos de Texto
    campo_cacau = ft.TextField(label="Qtd em @", border_color=COR_CACAU, width=250, border_radius=10)
    campo_banana = ft.TextField(label="Qtd Banana", border_color=COR_BANANA, width=250, border_radius=10)

    # --- FUNÇÕES ---
    def confirmar_cacau(e):
        if campo_cacau.value:
            texto_feedback.value = f"✅ SENNA: {campo_cacau.value}@ de Cacau registrados!"
            texto_feedback.color = COR_CACAU
            campo_cacau.value = ""
            page.update()

    def confirmar_banana(e):
        if campo_banana.value:
            texto_feedback.value = f"✅ SENNA: {campo_banana.value} de Banana registrados!"
            texto_feedback.color = COR_BANANA
            campo_banana.value = ""
            page.update()

    # --- LAYOUT DOS CARDS ---
    card_cacau = ft.Container(
        content=ft.Column([
            ft.Text("SAFRA DE CACAU", color=COR_CACAU, weight="bold", size=18),
            campo_cacau,
            ft.ElevatedButton("CONFIRMAR", bgcolor=COR_CACAU, color="white", on_click=confirmar_cacau)
        ], horizontal_alignment="center"),
        padding=20, bgcolor=COR_CARD, border_radius=15
    )

    card_banana = ft.Container(
        content=ft.Column([
            ft.Text("SAFRA DE BANANA", color=COR_BANANA, weight="bold", size=18),
            campo_banana,
            ft.ElevatedButton("CONFIRMAR", bgcolor=COR_BANANA, color="black", on_click=confirmar_banana)
        ], horizontal_alignment="center"),
        padding=20, bgcolor=COR_CARD, border_radius=15
    )

    # Adicionando tudo à página na ordem correta
    page.add(
        header,
        ft.Divider(color="#222222", height=30),
        ft.Column([
            card_cacau,
            ft.Divider(height=10, color="transparent"),
            card_banana,
            ft.Container(content=texto_feedback, padding=20)
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # ft.app é o comando que o Render e seu PC reconhecem melhor nesta versão
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
