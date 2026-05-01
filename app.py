import flet as ft
import os
import requests

def main(page: ft.Page):
    page.title = "BAHIA AGRO v4.2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.bgcolor = "#0f172a" 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_FUNDO_CARD = "#1e293b"

    # --- ABA 1: PLANILHAS ---
    conteudo_planilha = ft.Container(
        content=ft.Text("As planilhas serão exibidas aqui em breve.", size=20),
        padding=50
    )

    # --- ABA 2: LANÇAMENTO ---
    # (Criando os elementos primeiro para não dar erro de referência)
    card_cacau = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR CACAU", color=COR_CACAU, size=20, weight="bold"),
            ft.Dropdown(label="Variedade", options=[ft.dropdown.Option("PS-1319"), ft.dropdown.Option("CCN-51")]),
            ft.TextField(label="Quantidade em @", keyboard_type=ft.KeyboardType.NUMBER),
            ft.ElevatedButton("GRAVAR CACAU", bgcolor=COR_CACAU, color="white", width=400)
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_CACAU)
    )

    card_banana = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
            ft.Dropdown(label="Variedade", options=[ft.dropdown.Option("Prata"), ft.dropdown.Option("Terra")]),
            ft.TextField(label="Quantidade", keyboard_type=ft.KeyboardType.NUMBER),
            ft.ElevatedButton("GRAVAR BANANA", bgcolor=COR_BANANA, color="black", width=400)
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_BANANA)
    )

    conteudo_lancamento = ft.Row([card_cacau, card_banana], spacing=20, alignment="center")

    # --- ABA 3: CONHECIMENTO ---
    conteudo_conhecimento = ft.Container(
        content=ft.Text(">>> GUIA AGRO BAHIA <<<\n\nCacau: PS-1319, CCN-51\nBanana: Prata, Terra", font_family="monospace"),
        padding=40, bgcolor=COR_FUNDO_CARD, border_radius=15
    )

    # --- CONFIGURAÇÃO DAS ABAS (MÉTODO COMPATÍVEL) ---
    aba_planilha = ft.Tab(label="📊 Planilhas")
    aba_planilha.content = conteudo_planilha

    aba_lancamento = ft.Tab(label="➕ Novo Lançamento")
    aba_lancamento.content = conteudo_lancamento

    aba_conhecimento = ft.Tab(label="📖 Conhecimento")
    aba_conhecimento.content = conteudo_conhecimento

    tabs = ft.Tabs(
        selected_index=1,
        tabs=[aba_planilha, aba_lancamento, aba_conhecimento],
        expand=1
    )

    page.add(
        ft.Center(ft.Text("SISTEMA GESTÃO DE SAFRA", size=30, weight="bold")),
        ft.Container(height=20),
        tabs
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
