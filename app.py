import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO - SINCRONIZADO"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#0f172a"
    # Alinhamento nativo que funciona na v0.84.0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"

    # Container que vai segurar o que muda na tela
    conteudo_dinamico = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- TELA DE LANÇAMENTO ---
    tela_vendas = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("CACAU", color=COR_CACAU, size=22, weight="bold"),
                ft.TextField(label="Quantidade (@)", border_color=COR_CACAU),
                ft.ElevatedButton("SALVAR", bgcolor=COR_CACAU, color="white", width=200)
            ], horizontal_alignment="center"),
            padding=20, bgcolor="#1e293b", border_radius=10
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("BANANA", color=COR_BANANA, size=22, weight="bold"),
                ft.TextField(label="Quantidade (Kg/Cx)", border_color=COR_BANANA),
                ft.ElevatedButton("SALVAR", bgcolor=COR_BANANA, color="black", width=200)
            ], horizontal_alignment="center"),
            padding=20, bgcolor="#1e293b", border_radius=10
        )
    ], spacing=20)

    # --- FUNÇÃO DE NAVEGAÇÃO ---
    def navegar(e):
        if e.control.text == "➕ NOVO":
            conteudo_dinamico.controls = [tela_vendas]
        else:
            conteudo_dinamico.controls = [ft.Text("Configurações em breve...")]
        page.update()

    # Menu de Botões (Substitui as abas que estavam quebrando)
    menu = ft.Row([
        ft.ElevatedButton("➕ NOVO", on_click=navegar),
        ft.ElevatedButton("⚙️ CONFIG", on_click=navegar),
    ], alignment="center")

    # Início
    conteudo_dinamico.controls = [tela_vendas]

    page.add(
        ft.Text("BAHIA AGRO", size=28, weight="bold"),
        menu,
        ft.Divider(),
        conteudo_dinamico
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
