import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO v4.3"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.bgcolor = "#0f172a" 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_FUNDO_CARD = "#1e293b"

    # --- CONTEÚDOS ---
    # Conteúdo da Aba Lançamento
    card_cacau = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR CACAU", color=COR_CACAU, size=20, weight="bold"),
            ft.Dropdown(label="Variedade", options=[ft.dropdown.Option("PS-1319")]),
            ft.TextField(label="Quantidade em @"),
            ft.ElevatedButton("GRAVAR CACAU", bgcolor=COR_CACAU, color="white", width=300)
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_CACAU)
    )

    card_banana = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
            ft.Dropdown(label="Variedade", options=[ft.dropdown.Option("Prata")]),
            ft.TextField(label="Quantidade"),
            ft.ElevatedButton("GRAVAR BANANA", bgcolor=COR_BANANA, color="black", width=300)
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_BANANA)
    )

    aba_lancamento = ft.Row([card_cacau, card_banana], spacing=20, alignment="center")

    # Conteúdo da Aba Conhecimento
    aba_conhecimento = ft.Container(
        content=ft.Text(">>> GUIA AGRO BAHIA <<<\n\nCacau: PS-1319, CCN-51\nBanana: Prata, Terra", font_family="monospace"),
        padding=40, bgcolor=COR_FUNDO_CARD, border_radius=15
    )

    # --- SISTEMA DE NAVEGAÇÃO (MÉTODO ALTERNATIVO) ---
    # Se o 'Tabs' está dando erro, vamos usar um seletor simples que funciona sempre
    exibicao = ft.Container(content=aba_lancamento, expand=True)

    def mudar_aba(e):
        if e.control.selected_index == 0:
            exibicao.content = ft.Text("Planilhas em breve...", size=20)
        elif e.control.selected_index == 1:
            exibicao.content = aba_lancamento
        else:
            exibicao.content = aba_conhecimento
        page.update()

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.TABLE_CHART, label="Planilhas"),
            ft.NavigationDestination(icon=ft.icons.ADD_CIRCLE, label="Lançamento"),
            ft.NavigationDestination(icon=ft.icons.BOOK, label="Conhecimento"),
        ],
        selected_index=1,
        on_change=mudar_aba,
        bgcolor="#1e293b"
    )

    page.add(
        ft.Center(ft.Text("SISTEMA GESTÃO DE SAFRA", size=30, weight="bold")),
        ft.Container(height=20),
        exibicao,
        nav
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
