import flet as ft
import os

def main(page: ft.Page):
    # Configurações de Aparência (Igual ao VS Code)
    page.title = "BAHIA AGRO - Gestão Profissional"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Cores da Identidade Visual
    COR_CACAU = "#8B4513"  # Marrom
    COR_BANANA = "#EAB308" # Amarelo Ouro

    def salvar(e, fruta):
        # Feedback visual ao gravar
        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ Dados de {fruta} enviados com sucesso!"), 
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    # --- ABA 1: GESTÃO DE CACAU ---
    aba_cacau = ft.Column([
        ft.Container(height=10),
        ft.Icon(ft.icons.SPA, color=COR_CACAU, size=50),
        ft.Text("Colheita de Cacau", size=25, weight="bold"),
        ft.Divider(color=COR_CACAU),
        ft.Dropdown(
            label="Selecione a Variedade",
            options=[
                ft.dropdown.Option("Cacau PS-1319"),
                ft.dropdown.Option("Cacau CCN-51"),
                ft.dropdown.Option("Cacau Comum")
            ]
        ),
        ft.TextField(label="Peso Total (Kg)", keyboard_type=ft.KeyboardType.NUMBER),
        ft.ElevatedButton(
            "GRAVAR CACAU", 
            bgcolor=COR_CACAU, 
            color="white", 
            width=400, 
            height=50,
            on_click=lambda e: salvar(e, "Cacau")
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ABA 2: GESTÃO DE BANANA ---
    aba_banana = ft.Column([
        ft.Container(height=10),
        ft.Icon(ft.icons.LUNCH_DINING, color=COR_BANANA, size=50),
        ft.Text("Colheita de Banana", size=25, weight="bold"),
        ft.Divider(color=COR_BANANA),
        ft.Dropdown(
            label="Selecione o Tipo",
            options=[
                ft.dropdown.Option("Banana Prata"),
                ft.dropdown.Option("Banana Terra"),
                ft.dropdown.Option("Banana D'Água")
            ]
        ),
        ft.TextField(label="Quantidade (Cachos/Kg)", keyboard_type=ft.KeyboardType.NUMBER),
        ft.ElevatedButton(
            "GRAVAR BANANA", 
            bgcolor=COR_BANANA, 
            color="white", 
            width=400, 
            height=50,
            on_click=lambda e: salvar(e, "Banana")
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ABA 3: DIFERENCIAIS E INFORMAÇÕES ---
    aba_info = ft.ListView([
        ft.Text("Diferenciais das Frutas", size=25, weight="bold"),
        ft.Divider(),
        
        # Seção Cacau
        ft.ListTile(
            leading=ft.Icon(ft.icons.INFO, color=COR_CACAU),
            title=ft.Text("Cacau PS-1319", weight="bold"),
            subtitle=ft.Text("Alta produtividade e forte resistência à Vassoura de Bruxa. Ideal para adensamento."),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.INFO, color=COR_CACAU),
            title=ft.Text("Cacau CCN-51", weight="bold"),
            subtitle=ft.Text("Variedade rústica com alto teor de manteiga. Exige manejo de poda constante."),
        ),
        
        ft.Container(height=20), # Espaçador seguro
        
        # Seção Banana
        ft.ListTile(
            leading=ft.Icon(ft.icons.INFO, color=COR_BANANA),
            title=ft.Text("Banana Prata", weight="bold"),
            subtitle=ft.Text("Excelente aceitação no mercado de mesa. Longa durabilidade após colhida."),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.INFO, color=COR_BANANA),
            title=ft.Text("Banana Terra", weight="bold"),
            subtitle=ft.Text("Focada em indústria e culinária. Frutos grandes e alto valor calórico."),
        ),
    ], spacing=10, padding=20)

    # --- NAVEGAÇÃO POR TABS ---
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Cacau", icon=ft.icons.SPA, content=aba_cacau),
            ft.Tab(text="Banana", icon=ft.icons.LUNCH_DINING, content=aba_banana),
            ft.Tab(text="Informações", icon=ft.icons.DESCRIPTION, content=aba_info),
        ],
        expand=1
    )

    page.add(tabs)

# --- CONFIGURAÇÃO DE DEPLOY ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
