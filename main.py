import flet as ft
import os

def main(page: ft.Page):
    # Configurações de Aparência
    page.title = "BAHIA AGRO - Gestão de Safra"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Cores da Identidade
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"

    # Função de Clique para Salvar
    def salvar_dados(e):
        if not qtd_input.value or not var_dropdown.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro: Preencha todos os campos!"), 
                bgcolor="red"
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ Gravado: {var_dropdown.value} - {qtd_input.value}"), 
                bgcolor="green"
            )
            qtd_input.value = "" # Limpa o campo após salvar
        page.snack_bar.open = True
        page.update()

    # --- ABA DE LANÇAMENTO ---
    var_dropdown = ft.Dropdown(
        label="Variedade",
        options=[
            ft.dropdown.Option("Cacau PS-1319"),
            ft.dropdown.Option("Cacau CCN-51"),
            ft.dropdown.Option("Banana Prata"),
            ft.dropdown.Option("Banana Terra"),
        ]
    )
    
    qtd_input = ft.TextField(
        label="Quantidade (Kg)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.icons.NUMBERS
    )

    aba_lancar = ft.Column([
        ft.Text("Registro de Colheita", size=25, weight="bold"),
        ft.Divider(),
        var_dropdown,
        qtd_input,
        ft.ElevatedButton(
            "ENVIAR PARA CENTRAL",
            icon=ft.icons.SEND,
            bgcolor=COR_CACAU,
            color="white",
            width=400,
            height=50,
            on_click=salvar_dados
        ),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ABA DE RELATÓRIO (SIMULADA) ---
    aba_relatorio = ft.Column([
        ft.Text("Últimos Lançamentos", size=25, weight="bold"),
        ft.Divider(),
        ft.ListTile(
            leading=ft.Icon(ft.icons.CHEVRON_RIGHT),
            title=ft.Text("Cacau PS-1319"),
            subtitle=ft.Text("Aguardando sincronização..."),
        ),
    ])

    # --- NAVEGAÇÃO POR ABAS ---
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Lançar", icon=ft.icons.ADD_TASK, content=aba_lancar),
            ft.Tab(text="Relatórios", icon=ft.icons.LIST_ALT, content=aba_relatorio),
        ],
        expand=1
    )

    page.add(tabs)

# --- CONFIGURAÇÃO PARA O RENDER ---
if __name__ == "__main__":
    # Mantendo a porta dinâmica que funcionou no Render
    port = int(os.environ.get("PORT", 8080))
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=port
    )
