import flet as ft
import os

def main(page: ft.Page):
    page.title = "SENNA - BAHIA AGRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    # Alteração estética: Fundo Preto solicitado
    page.bgcolor = "#000000" 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_CARD = "#121212" # Cinza quase preto para os cards

    # Texto de retorno (Resposta do que o usuário quer)
    texto_resultado = ft.Text("", size=16, color="green", weight="bold")

    # --- FUNÇÕES DE AÇÃO ---
    def salvar_cacau(e):
        qtd = campo_cacau.value
        if qtd:
            texto_resultado.value = f"✅ Sucesso: {qtd} @ de Cacau lançadas!"
            campo_cacau.value = ""
            page.update()

    def salvar_banana(e):
        qtd = campo_banana.value
        if qtd:
            texto_resultado.value = f"✅ Sucesso: {qtd} de Banana lançadas!"
            campo_banana.value = ""
            page.update()

    # --- CAMPOS DE ENTRADA ---
    campo_cacau = ft.TextField(label="Quantidade (@)", border_color=COR_CACAU, color="white")
    campo_banana = ft.TextField(label="Quantidade", border_color=COR_BANANA, color="white")

    # --- INTERFACE ---
    
    # Cabeçalho com Logo "SENNA" à direita
    cabecalho = ft.Row([
        ft.Text("BAHIA AGRO", size=20, weight="bold"),
        ft.Text("SENNA", size=24, weight="bold", color=COR_BANANA, italic=True)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Cards de Lançamento
    cards = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAMENTO DE CACAU", color=COR_CACAU, weight="bold"),
                campo_cacau,
                ft.ElevatedButton("CONFIRMAR", bgcolor=COR_CACAU, color="white", on_click=salvar_cacau)
            ]),
            padding=20, bgcolor=COR_CARD, border_radius=15, width=350
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAMENTO DE BANANA", color=COR_BANANA, weight="bold"),
                campo_banana,
                ft.ElevatedButton("CONFIRMAR", bgcolor=COR_BANANA, color="black", on_click=salvar_banana)
            ]),
            padding=20, bgcolor=COR_CARD, border_radius=15, width=350
        ),
        # Espaço para a resposta aparecer
        ft.Container(content=texto_resultado, padding=10)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    # Montagem da Página
    page.add(
        cabecalho,
        ft.Divider(color="#333333"),
        ft.VerticalDivider(visible=False, width=20),
        cards
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Usando o comando padrão de execução
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
