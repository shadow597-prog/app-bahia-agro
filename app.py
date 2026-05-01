import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO - ESTÁVEL"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#0f172a"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"

    # Container principal que muda o conteúdo
    conteudo_dinamico = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- TELA DE LANÇAMENTO ---
    tela_vendas = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("CACAU", color=COR_CACAU, size=22, weight="bold"),
                ft.TextField(label="Quantidade em @", border_color=COR_CACAU),
                ft.ElevatedButton("SALVAR CACAU", bgcolor=COR_CACAU, color="white", width=250)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, bgcolor="#1e293b", border_radius=10
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("BANANA", color=COR_BANANA, size=22, weight="bold"),
                ft.TextField(label="Quantidade", border_color=COR_BANANA),
                ft.ElevatedButton("SALVAR BANANA", bgcolor=COR_BANANA, color="black", width=250)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, bgcolor="#1e293b", border_radius=10
        )
    ], spacing=20)

    # --- FUNÇÕES DE NAVEGAÇÃO (Sem ler .text para evitar erros) ---
    def ir_vendas(e):
        conteudo_dinamico.controls = [tela_vendas]
        page.update()

    def ir_config(e):
        conteudo_dinamico.controls = [ft.Text("Configurações (Em breve)", size=20)]
        page.update()

    # Menu de Navegação
    menu = ft.Row([
        ft.ElevatedButton("➕ NOVO", on_click=ir_vendas),
        ft.ElevatedButton("⚙️ CONFIG", on_click=ir_config),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Iniciar com a tela de vendas
    conteudo_dinamico.controls = [tela_vendas]

    page.add(
        ft.Text("BAHIA AGRO", size=28, weight="bold"),
        menu,
        ft.Divider(),
        conteudo_dinamico
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Voltando para ft.app que é mais estável na sua versão 0.84.0
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
