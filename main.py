import flet as ft
import os
import requests

# Link da sua planilha (coloque o seu link aqui)
URL_PLANILHA = "SUA_URL_DO_GOOGLE_SCRIPTS_AQUI"

def main(page: ft.Page):
    page.title = "BAHIA AGRO v4.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.bgcolor = "#1a1c23" # Fundo escuro igual da imagem
    
    # Cores do Sistema
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_CARD = "#252934"

    def salvar_dados(fruta, variedade, quantidade, extra=""):
        try:
            dados = {
                "fruta": fruta, 
                "variedade": variedade, 
                "peso": f"{quantidade} {extra}".strip()
            }
            requests.post(URL_PLANILHA, json=dados)
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ {fruta} gravado!"), bgcolor="green")
        except:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao salvar"), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    # --- CABEÇALHO ---
    header = ft.Column([
        ft.Text("SISTEMA GESTÃO DE SAFRA", size=32, weight="bold", color="white"),
        ft.Row([
            ft.TextButton("📊 Planilhas", icon=ft.icons.TABLE_CHART),
            ft.ElevatedButton("+ Novo Lançamento", bgcolor="#3b82f6", color="white"),
            ft.TextButton("📖 Conhecimento", icon=ft.icons.MENU_BOOK),
        ], alignment="center", spacing=20)
    ], horizontal_alignment="center", spacing=20)

    # --- CARD LANÇAR CACAU ---
    card_cacau = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR CACAU", color="#d97706", size=20, weight="bold"),
            ft.Dropdown(label="Variedade", border_color="#4b5563", options=[ft.dropdown.Option("PS-1319"), ft.dropdown.Option("CCN-51")]),
            ft.Dropdown(label="Processo", border_color="#4b5563", options=[ft.dropdown.Option("Fermentado"), ft.dropdown.Option("Seco")]),
            ft.TextField(label="Quantidade em @", border_color="#4b5563"),
            ft.Container(height=10),
            ft.ElevatedButton(
                "GRAVAR CACAU", 
                bgcolor=COR_CACAU, 
                color="white", 
                width=400, 
                height=50,
                on_click=lambda _: salvar_dados("Cacau", "Variedade", "10", "@")
            )
        ], horizontal_alignment="center", spacing=15),
        padding=30,
        border_radius=15,
        bgcolor=COR_CARD,
        border=ft.border.all(1, "#4b5563"),
        expand=True
    )

    # --- CARD LANÇAR BANANA ---
    unidade_banana = ft.SegmentedButton(
        selected={"Kg"},
        segments=[
            ft.Segment(value="Kg", label=ft.Text("Kg")),
            ft.Segment(value="Cento", label=ft.Text("Cento")),
            ft.Segment(value="Caixa", label=ft.Text("Caixa")),
        ],
    )

    card_banana = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
            ft.Dropdown(label="Variedade", border_color="#4b5563", options=[ft.dropdown.Option("Prata"), ft.dropdown.Option("Terra")]),
            ft.Dropdown(label="Tipo", border_color="#4b5563", options=[ft.dropdown.Option("Primeira"), ft.dropdown.Option("Segunda")]),
            ft.Row([unidade_banana], alignment="center"),
            ft.TextField(label="Quantidade", border_color="#4b5563"),
            ft.ElevatedButton(
                "GRAVAR BANANA", 
                bgcolor=COR_BANANA, 
                color="black", 
                width=400, 
                height=50,
                on_click=lambda _: salvar_dados("Banana", "Variedade", "20", "Unid")
            )
        ], horizontal_alignment="center", spacing=15),
        padding=30,
        border_radius=15,
        bgcolor=COR_CARD,
        border=ft.border.all(1, COR_BANANA), # Borda amarela como na foto
        expand=True
    )

    # --- LAYOUT PRINCIPAL ---
    layout = ft.Column([
        header,
        ft.Container(height=20),
        ft.Row([
            card_cacau,
            card_banana
        ], spacing=30, alignment="center")
    ])

    page.add(layout)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
