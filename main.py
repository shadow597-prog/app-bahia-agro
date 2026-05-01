import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Conteúdo simples para teste
    page.add(
        ft.Text("BAHIA AGRO - SISTEMA ATIVO", size=30, weight="bold", color="#8B4513"),
        ft.Text("O sistema está online e pronto para uso."),
        ft.TextField(label="Quantidade de Colheita", width=300),
        ft.ElevatedButton("Enviar Dados", bgcolor="#8B4513", color="white")
    )

if __name__ == "__main__":
    # O Render exige que a porta seja lida da variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    
    # IMPORTANTE: host="0.0.0.0" e view=ft.AppView.WEB_BROWSER
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=port
    )