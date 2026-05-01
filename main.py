import flet as ft
import os
import requests

# URL da Planilha que você configurou no Google
URL_PLANILHA = "SUA_URL_AQUI"

def main(page: ft.Page):
    page.title = "BAHIA AGRO - Central de Comando"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Função para buscar os dados salvos e mostrar no seu app
    def atualizar_relatorio(e=None):
        # Aqui o seu app vai "ler" a planilha
        # Por enquanto, vamos simular a chegada dos dados
        lista_vendas.controls.clear()
        lista_vendas.controls.append(ft.Text("Sincronizando com o servidor..."))
        page.update()
        
        # Em um próximo passo, podemos fazer ele ler o Google Sheets aqui
        # Para agora, ele mostrará a confirmação de envio
        pass

    def enviar_dados(fruta, var, peso):
        dados = {"fruta": fruta, "variedade": var, "peso": peso}
        try:
            requests.post(URL_PLANILHA, json=dados)
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ {fruta} enviado!"), bgcolor="green")
        except:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao enviar"), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    # --- UI DO SEU APP ---
    lista_vendas = ft.ListView(expand=True, spacing=10)

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Lançar", icon=ft.icons.ADD, content=ft.Column([
                ft.Text("Novo Registro", size=20),
                ft.ElevatedButton("Atualizar Banco de Dados", on_click=atualizar_relatorio)
            ])),
            ft.Tab(text="Ver Resultados", icon=ft.icons.ANALYTICS, content=lista_vendas),
        ],
        expand=1
    )

    page.add(tabs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
