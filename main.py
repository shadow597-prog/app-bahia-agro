import flet as ft
import os

def main(page: ft.Page):
    page.title = "BAHIA AGRO - Gestão Especializada"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"

    def salvar(e, fruta):
        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ {fruta} registrado com sucesso!"), 
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    # --- ABA CACAU ---
    aba_cacau = ft.Column([
        ft.Icon(ft.icons.CHEVRON_RIGHT, color=COR_CACAU, size=40),
        ft.Text("Colheita de Cacau", size=25, weight="bold"),
        ft.Dropdown(
            label="Variedade de Cacau",
            options=[ft.dropdown.Option("PS-1319"), ft.dropdown.Option("CCN-51")]
        ),
        ft.TextField(label="Peso (Arrobas/Kg)", keyboard_type=ft.KeyboardType.NUMBER),
        ft.ElevatedButton("Gravar Cacau", bgcolor=COR_CACAU, color="white", on_click=lambda e: salvar(e, "Cacau"))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ABA BANANA ---
    aba_banana = ft.Column([
        ft.Icon(ft.icons.CHEVRON_RIGHT, color=COR_BANANA, size=40),
        ft.Text("Colheita de Banana", size=25, weight="bold"),
        ft.Dropdown(
            label="Tipo de Banana",
            options=[ft.dropdown.Option("Prata"), ft.dropdown.Option("Terra")]
        ),
        ft.TextField(label="Quantidade (Cachos/Kg)", keyboard_type=ft.KeyboardType.NUMBER),
        ft.ElevatedButton("Gravar Banana", bgcolor=COR_BANANA, color="white", on_click=lambda e: salvar(e, "Banana"))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ABA DIFERENCIAIS (INFORMAÇÕES) ---
    aba_info = ft.ListView([
        ft.Text("Guia de Variedades", size=25, weight="bold"),
        ft.Divider(),
        
        ft.Text("🍫 CACAU", color=COR_CACAU, weight="bold", size=20),
        ft.Text("• PS-1319: Alta produtividade e resistência à Vassoura de Bruxa. Ótimo para clima úmido."),
        ft.Text("• CCN-51: Variedade clonada, muito rústica e com alta carga de gordura na amêndoa."),
        
        ft.VerticalDivider(height=20),
        
        ft.Text("🍌 BANANA", color=COR_BANANA, weight="bold", size=20),
        ft.Text("• Prata: Maior durabilidade pós-colheita e sabor levemente ácido. Preferida para mesa."),
        ft.Text("• Terra: Frutos grandes, ideais para cozimento e fritura. Alta demanda comercial."),
    ], spacing=10, padding=10)

    # --- NAVEGAÇÃO PRINCIPAL ---
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Cacau", icon=ft.icons.SPA, content=aba_cacau),
            ft.Tab(text="Banana", icon=ft.icons.LUNCH_DINING, content=aba_banana),
            ft.Tab(text="Diferenciais", icon=ft.icons.INFO_OUTLINE, content=aba_info),
        ],
        expand=1
    )

    page.add(tabs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
