import flet as ft
import os
import requests

# Link da sua planilha (opcional)
URL_PLANILHA = "COLE_SEU_LINK_AQUI"

def main(page: ft.Page):
    page.title = "BAHIA AGRO v4.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.bgcolor = "#0f172a" # Fundo escuro profissional
    
    # Cores baseadas no seu design
    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_FUNDO_CARD = "#1e293b"

    def salvar_dados(cultura, var, proc, qtd, uni):
        if not qtd:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira uma quantidade"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Envio para planilha se houver URL
        if URL_PLANILHA != "COLE_SEU_LINK_AQUI":
            try:
                dados = {"fruta": cultura, "variedade": var, "peso": f"{qtd} {uni}"}
                requests.post(URL_PLANILHA, json=dados)
            except:
                pass
        
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ {cultura} {var} gravado com sucesso!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    # --- UI: CABEÇALHO ---
    header = ft.Column([
        ft.Text("SISTEMA GESTÃO DE SAFRA", size=32, weight="bold", color="white"),
    ], horizontal_alignment="center")

    # --- ABA: NOVO LANÇAMENTO ---
    # Coluna Cacau
    var_cacau = ft.Dropdown(label="Variedade", border_color="#4b5563", options=[
        ft.dropdown.Option("PS-1319"), ft.dropdown.Option("CCN-51"), 
        ft.dropdown.Option("Comum"), ft.dropdown.Option("Parazinho")
    ])
    proc_cacau = ft.Dropdown(label="Processo", border_color="#4b5563", options=[
        ft.dropdown.Option("Secado ao Sol"), ft.dropdown.Option("Fermentado"),
        ft.dropdown.Option("In Natura"), ft.dropdown.Option("Torrado (Nibs)")
    ])
    qtd_cacau = ft.TextField(label="Quantidade em @", border_color="#4b5563", keyboard_type=ft.KeyboardType.NUMBER)
    
    card_cacau = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR CACAU", color=COR_CACAU, size=20, weight="bold"),
            var_cacau, proc_cacau, qtd_cacau,
            ft.ElevatedButton("GRAVAR CACAU", bgcolor=COR_CACAU, color="white", width=400, height=50,
                             on_click=lambda _: salvar_dados("Cacau", var_cacau.value, proc_cacau.value, qtd_cacau.value, "@"))
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_CACAU), expand=True
    )

    # Coluna Banana
    var_banana = ft.Dropdown(label="Variedade", border_color="#4b5563", options=[
        ft.dropdown.Option("Prata"), ft.dropdown.Option("Nanica"), 
        ft.dropdown.Option("Terra"), ft.dropdown.Option("Maçã")
    ])
    tipo_banana = ft.Dropdown(label="Tipo", border_color="#4b5563", options=[
        ft.dropdown.Option("De Primeira"), ft.dropdown.Option("De Segunda"),
        ft.dropdown.Option("Madura"), ft.dropdown.Option("Verde")
    ])
    uni_banana = ft.SegmentedButton(
        selected={"Cento"},
        segments=[
            ft.Segment(value="Kg", label=ft.Text("Kg")),
            ft.Segment(value="Cento", label=ft.Text("Cento")),
            ft.Segment(value="Caixa", label=ft.Text("Caixa"))
        ]
    )
    qtd_banana = ft.TextField(label="Quantidade", border_color="#4b5563", keyboard_type=ft.KeyboardType.NUMBER)

    card_banana = ft.Container(
        content=ft.Column([
            ft.Text("LANÇAR BANANA", color=COR_BANANA, size=20, weight="bold"),
            var_banana, tipo_banana, uni_banana, qtd_banana,
            ft.ElevatedButton("GRAVAR BANANA", bgcolor=COR_BANANA, color="black", width=400, height=50,
                             on_click=lambda _: salvar_dados("Banana", var_banana.value, tipo_banana.value, qtd_banana.value, list(uni_banana.selected)[0]))
        ], horizontal_alignment="center", spacing=15),
        padding=30, border_radius=15, bgcolor=COR_FUNDO_CARD, border=ft.border.all(1, COR_BANANA), expand=True
    )

    aba_lancamento = ft.Row([card_cacau, card_banana], spacing=20, alignment="center")

    # --- ABA: CONHECIMENTO ---
    guia_texto = """
>>> GUIA DE VARIEDADES - GESTÃO AGRO BAHIA <<<

[ CACAU ]
----------------------------------------------------------
* PS-1319: Alta produtividade e amêndoas pesadas. Resistente.
* CCN-51:  O 'trator' do cacau. Alta manteiga, exige fermentação fria.
* COMUM:   Sabor chocolate intenso. Cultivado na sombra (Cabruca).
* PARAZINHO: Variedade fina, amêndoas de alto sabor aromático.

[ BANANA ]
----------------------------------------------------------
* PRATA:   Melhor durabilidade pós-colheita. Equilíbrio doce/ácido.
* NANICA:  Porte baixo, muito doce. Ótima para indústria de doces.
* TERRA:   Grande, para cozinhar/fritar. Alto valor de mercado.
* MAÇÃ:    Sabor premium, aroma de maçã. Rara e valorizada.
    """
    aba_conhecimento = ft.Container(
        content=ft.Text(guia_texto, font_family="monospace", size=16),
        padding=40, bgcolor=COR_FUNDO_CARD, border_radius=15, border=ft.border.all(1, "#334155")
    )

    # --- NAVEGAÇÃO POR ABAS (CORRIGIDO PARA O SITE) ---
    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(label="📊 Planilhas", content=ft.Container(ft.Text("Visualização de planilhas em breve...", size=20), padding=50)),
            ft.Tab(label="➕ Novo Lançamento", content=aba_lancamento),
            ft.Tab(label="📖 Conhecimento", content=aba_conhecimento),
        ],
        expand=1
    )

    page.add(header, ft.Container(height=20), tabs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
