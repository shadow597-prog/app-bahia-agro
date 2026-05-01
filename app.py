import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO v4.4"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#0f172a" 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_FUNDO_CARD = "#1e293b"

    # --- ELEMENTOS DE INTERFACE ---
    container_principal = ft.Column(expand=True, scroll="auto")

    # Conteúdo: Lançamento
    layout_lancamento = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAR CACAU", color=COR_CACAU, size=20, weight="bold"),
                ft.TextField(label="Quantidade em @", border_color=COR_CACAU),
                ft.ElevatedButton("GRAVAR", bgcolor=COR_CACAU, color="white")
            ]),
            padding=20, border_radius=10, bgcolor=COR_FUNDO_CARD
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
                ft.TextField(label="Quantidade", border_color=COR_BANANA),
                ft.ElevatedButton("GRAVAR", bgcolor=COR_BANANA, color="black")
            ]),
            padding=20, border_radius=10, bgcolor=COR_FUNDO_CARD
        )
    ], spacing=20)

    # Conteúdo: Guia
    layout_guia = ft.Container(
        content=ft.Text("GUIA AGRO\n\nCacau: PS-1319, CCN-51\nBanana: Prata, Terra", size=18),
        padding=20
    )

    # Funções de Troca (Sem usar Tabs ou NavigationBar)
    def ir_para_lancamento(e):
        container_principal.controls = [layout_lancamento]
        page.update()

    def ir_para_guia(e):
        container_principal.controls = [layout_guia]
        page.update()

    # Menu Simples (Botões Normais)
    menu = ft.Row([
        ft.ElevatedButton("➕ NOVO", on_click=ir_para_lancamento),
        ft.ElevatedButton("📖 GUIA", on_click=ir_para_guia),
    ], alignment="center")

    # Iniciar com o lançamento na tela
    container_principal.controls = [layout_lancamento]

    page.add(
        ft.Center(ft.Text("GESTÃO BAHIA AGRO", size=25, weight="bold")),
        menu,
        ft.Divider(),
        container_principal
    )

if __name__ == "__main__":
    # Configuração vital para o Render
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
