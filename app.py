import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS (Prevenção de erro de conexão) ---
def init_db():
    conn = sqlite3.connect("senna_agro.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - SISTEMA AGRO"
    page.bgcolor = "#000000" # Estética solicitada: Fundo Preto
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variáveis de Estado
    usuario_logado = ft.Ref[ft.Text]()
    
    # Cores SENNA
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"

    # --- TELAS ---
    container_principal = ft.Column(horizontal_alignment="center", spacing=20)

    # Função de feedback (Prevenção de erro: Feedback limpo)
    def mostrar_aviso(texto, cor):
        aviso = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(aviso)
        aviso.open = True
        page.update()

    # --- LÓGICA DE NEGÓCIO ---
    def salvar_venda(produto, qtd_field, preco_unidade, cor):
        try:
            if not qtd_field.value:
                return
            qtd = float(qtd_field.value.replace(",", "."))
            total = qtd * preco_unidade
            user = usuario_logado.current.value if usuario_logado.current else "Admin"
            
            cursor = db.cursor()
            cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                           (user, produto, qtd, total))
            db.commit()
            
            qtd_field.value = ""
            mostrar_aviso(f"Registrado: {qtd} de {produto} (R$ {total:.2f})", cor)
            page.update()
        except ValueError:
            mostrar_aviso("Erro: Digite apenas números!", "red")

    # --- INTERFACE: LOGIN ---
    def fazer_login(e):
        if campo_user.value:
            page.session.set("user", campo_user.value)
            montar_dashboard()
        else:
            mostrar_aviso("Digite seu nome para entrar", "red")

    campo_user = ft.TextField(label="Nome do Funcionário/Dono", border_color=COR_BANANA)
    tela_login = ft.Column([
        ft.Text("SENNA", size=40, weight="bold", italic=True, color=COR_BANANA),
        ft.Text("Acesse o sistema rural", color="#666666"),
        campo_user,
        ft.ElevatedButton("ENTRAR", on_click=fazer_login, bgcolor=COR_BANANA, color="black")
    ], horizontal_alignment="center")

    # --- INTERFACE: DASHBOARD (NOVO + HISTÓRICO) ---
    def montar_dashboard():
        user_nome = page.session.get("user")
        
        # Campos de entrada
        in_cacau = ft.TextField(label="Qtd em @", border_color=COR_CACAU, width=200)
        in_banana = ft.TextField(label="Qtd Cento/Kg", border_color=COR_BANANA, width=200)

        # Cabeçalho com Logo SENNA na Direita
        cabecalho = ft.Row([
            ft.Text("BAHIA AGRO", size=18, color="#666666"),
            ft.Text(user_nome, ref=usuario_logado, size=16, color=COR_BANANA, weight="bold"),
            ft.Text("SENNA", size=24, weight="bold", italic=True, color=COR_BANANA)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Lista de Histórico
        lista_historico = ft.Column(spacing=10)
        
        def atualizar_historico(e):
            cursor = db.cursor()
            cursor.execute("SELECT produto, qtd, valor FROM lancamentos ORDER BY id DESC LIMIT 5")
            vendas = cursor.fetchall()
            lista_historico.controls = [ft.Text("ÚLTIMOS LANÇAMENTOS:", weight="bold")]
            for v in vendas:
                lista_historico.controls.append(
                    ft.Text(f"• {v[0]}: {v[1]} (R$ {v[2]:.2f})", size=14)
                )
            page.update()

        # Botão de Atualizar Histórico
        btn_refresh = ft.TextButton("VER HISTÓRICO RECENTE", on_click=atualizar_historico)

        container_principal.controls = [
            cabecalho,
            ft.Divider(color="#222222"),
            ft.Container(
                content=ft.Column([
                    ft.Text("LANÇAR PRODUÇÃO", weight="bold"),
                    in_cacau,
                    ft.ElevatedButton("CONFIRMAR CACAU (R$ 600/@)", on_click=lambda _: salvar_venda("Cacau", in_cacau, 600, COR_CACAU)),
                    ft.Divider(height=10, color="transparent"),
                    in_banana,
                    ft.ElevatedButton("CONFIRMAR BANANA (R$ 50/Cento)", on_click=lambda _: salvar_venda("Banana", in_banana, 50, COR_BANANA)),
                ], horizontal_alignment="center"),
                padding=20, bgcolor="#121212", border_radius=15
            ),
            btn_refresh,
            lista_historico
        ]
        page.update()

    # Inicialização
    container_principal.controls = [tela_login]
    page.add(container_principal)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
