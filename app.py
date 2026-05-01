import flet as ft
import os

def main(page: ft.Page):
    page.title = "SENNA - GESTÃO AGRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#000000" # Fundo totalmente preto
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    # Definição de cores da marca
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_CARD = "#121212" # Cinza escuro para contraste no preto

    # Texto de feedback (Resposta do sistema)
    texto_feedback = ft.Text("", size=16, weight="bold")

    # --- FUNÇÕES ---
    def salvar_dados(e, produto):
        if produto == "Cacau":
            valor = campo_cacau.value
            cor = COR_CACAU
        else:
            valor = campo_banana.value
            cor = COR_BANANA
            
        if valor:
            texto_feedback.value = f"✅ {produto}: {valor} registrado na Safra!"
            texto_feedback.color = cor
            campo_cacau.value = ""
            campo_banana.value = ""
            page.update()

    # --- CAMPOS DE ENTRADA ---
    campo_cacau = ft.TextField(label="Qtd @ Cacau", border_color=COR_CACAU, width=200)
    campo_banana = ft.TextField(label="Qtd Banana", border_color=COR_BANANA, width=200)

    # --- COMPONENTES DE INTERFACE ---

    # Cabeçalho: Nome do App à esquerda e SENNA (Logo) à direita
    header = ft.Row([
        ft.Text("BAHIA AGRO", size=18, weight="w500", color="#BBBBBB"),
        ft.Text("SENNA", size=26, weight="bold", italic=True, color=COR_BANANA)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Seção de Informações de Safra (Tabela Visual)
    info_safra = ft.Container(
        content=ft.Column([
            ft.Text("INFORMAÇÕES DE SAFRA 2026", size=18, weight="bold"),
            ft.Row([
                ft.Column([
                    ft.Text("CACAU", color=COR_CACAU, weight="bold"),
                    ft.Text("Temporada: Out-Mai"),
                    ft.Text("Status: Em colheita", color="green")
                ], expand=True),
                ft.VerticalDivider(),
                ft.Column([
                    ft.Text("BANANAS", color=COR_BANANA, weight="bold"),
                    ft.Text("Tipo: Prata/Terra"),
                    ft.Text("Status: Fluxo Contínuo")
                ], expand=True)
            ], alignment="start")
        ]),
        padding=20, bgcolor=COR_CARD, border_radius=15, border=ft.border.all(1, "#333333")
    )

    # Cards de Lançamento
    lancamentos = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("NOVO LANÇAMENTO", weight="bold"),
                campo_cacau,
                ft.ElevatedButton("CONFIRMAR CACAU", bgcolor=COR_CACAU, color="white", 
                                 on_click=lambda e: salvar_dados(e, "Cacau")),
                ft.Divider(height=10, color="transparent"),
                campo_banana,
                ft.ElevatedButton("CONFIRMAR BANANA", bgcolor=COR_BANANA, color="black",
                                 on_click=lambda e: salvar_dados(e, "Banana")),
            ], horizontal_alignment="center"),
            padding=25, bgcolor=COR_CARD, border_radius=15, width=300
        )
    ], alignment="center")

    # Montagem Final
    page.add(
        header,
        ft.Divider(color="#222222"),
        info_safra,
        ft.Text("PAINEL DE OPERAÇÕES", size=14, color="#666666"),
        lancamentos,
        ft.Container(content=texto_feedback, padding=10, alignment=ft.alignment.center)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
