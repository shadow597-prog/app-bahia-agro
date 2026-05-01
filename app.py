import flet as ft
import os

def main(page: ft.Page):
    # Configurações básicas que funcionam em qualquer versão
    page.title = "BAHIA AGRO v4.6"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#0f172a"
    
    # Previsão de erro: Se o Flet for antigo, o 'Center' quebra. 
    # Solução: Usar o alinhamento da própria página.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_FUNDO_CARD = "#1e293b"

    # --- ELEMENTOS DE INTERFACE ---
    container_principal = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Layout de Lançamento (Variáveis: Cacau e Banana)
    layout_lancamento = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAR CACAU", color=COR_CACAU, size=20, weight="bold"),
                ft.TextField(label="Quantidade (@)", border_color=COR_CACAU),
                ft.ElevatedButton("GRAVAR", bgcolor=COR_CACAU, color="white")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, border_radius=10, bgcolor=COR_FUNDO_CARD, width=320
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
                ft.TextField(label="Quantidade", border_color=COR_BANANA),
                ft.ElevatedButton("GRAVAR", bgcolor=COR_BANANA, color="black")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, border_radius=10, bgcolor=COR_FUNDO_CARD, width=320
        )
    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Conteúdo: Guia
    layout_guia = ft.Container(
        content=ft.Text("GUIA AGRO\n\nCacau: PS-1319, CCN-51\nBanana: Prata, Terra", size=18, text_align=ft.TextAlign.CENTER),
        padding=20
    )

    # Funções de Troca de Tela (Simulando abas)
    def ir_para_lancamento(e):
        container_principal.controls = [layout_lancamento]
        page.update()

    def ir_para_guia(e):
        container_principal.controls = [layout_guia]
        page.update()

    # Menu com Botões Simples (Prevenindo erro de NavigationBar)
    menu = ft.Row([
        ft.TextButton("➕ NOVO", on_click=ir_para_lancamento),
        ft.TextButton("📖 GUIA", on_click=ir_para_guia),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Iniciar com o lançamento na tela
    container_principal.controls = [layout_lancamento]

    # Adicionando os elementos à página
    page.add(
        ft.Text("GESTÃO BAHIA AGRO", size=24, weight="bold"),
        menu,
        ft.Divider(),
        container_principal
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Usando o comando padrão que o Render já aceitou no log anterior
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
