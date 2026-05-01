import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS (Usuários e Lançamentos) ---
def init_db():
    conn = sqlite3.connect("senna_agro.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabela de Usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT UNIQUE, senha TEXT)''')
    # Tabela de Lançamentos
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - SEGURANÇA MÁXIMA"
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variáveis de Controle
    estado = {"usuario_atual": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"
    COR_CARD = "#121212"

    container_principal = ft.Column(horizontal_alignment="center", spacing=20)

    def mostrar_aviso(texto, cor):
        aviso = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(aviso)
        aviso.open = True
        page.update()

    # --- LÓGICA DE CADASTRO E LOGIN ---
    def cadastrar_usuario(e):
        login = campo_new_user.value
        senha = campo_new_pass.value
        if login and senha:
            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (login, senha))
                db.commit()
                mostrar_aviso("Usuário cadastrado! Agora faça login.", "green")
                ir_para_login(None)
            except sqlite3.IntegrityError:
                mostrar_aviso("Este nome de usuário já existe!", "red")
        else:
            mostrar_aviso("Preencha todos os campos!", "orange")

    def validar_login(e):
        login = campo_login_user.value
        senha = campo_login_pass.value
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
        user = cursor.fetchone()
        
        if user:
            estado["usuario_atual"] = login
            montar_dashboard()
        else:
            mostrar_aviso("Login ou Senha incorretos!", "red")

    # --- INTERFACE: TROCA DE TELAS ---
    def ir_para_cadastro(e):
        container_principal.controls = [tela_cadastro]
        page.update()

    def ir_para_login(e):
        container_principal.controls = [tela_login]
        page.update()

    # --- TELAS (CADASTRO E LOGIN) ---
    campo_new_user = ft.TextField(label="Novo Usuário", border_color=COR_BANANA)
    campo_new_pass = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, border_color=COR_BANANA)
    
    tela_cadastro = ft.Column([
        ft.Text("CADASTRO SENNA", size=28, weight="bold", color=COR_BANANA),
        campo_new_user, campo_new_pass,
        ft.ElevatedButton("CADASTRAR", on_click=cadastrar_usuario, bgcolor=COR_BANANA, color="black"),
        ft.TextButton("Já tenho conta? Entrar", on_click=ir_para_login)
    ], horizontal_alignment="center")

    campo_login_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    campo_login_pass = ft.TextField(label="Senha", password=True, can_reveal_password=True, border_color=COR_BANANA)
    
    tela_login = ft.Column([
        ft.Text("SENNA AGRO", size=32, weight="bold", color=COR_BANANA, italic=True),
        ft.Container(
            content=ft.Column([
                campo_login_user, campo_login_pass,
                ft.ElevatedButton("ENTRAR", on_click=validar_login, bgcolor=COR_BANANA, color="black", width=200),
                ft.TextButton("Não tem conta? Cadastre-se", on_click=ir_para_cadastro)
            ], horizontal_alignment="center"),
            padding=30, bgcolor=COR_CARD, border_radius=15
        )
    ], horizontal_alignment="center")

    # --- INTERFACE: DASHBOARD ---
    def montar_dashboard():
        container_principal.controls.clear()
        
        in_cacau = ft.TextField(label="Qtd em @", border_color=COR_CACAU, width=250)
        in_banana = ft.TextField(label="Qtd Cento/Kg", border_color=COR_BANANA, width=250)
        lista_historico = ft.Column(spacing=5)

        def salvar_venda(produto, field, preco, cor):
            if not field.value: return
            try:
                qtd = float(field.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (estado["usuario_atual"], produto, qtd, qtd * preco))
                db.commit()
                field.value = ""
                mostrar_aviso(f"Salvo por {estado['usuario_atual']}!", cor)
                page.update()
            except: mostrar_aviso("Erro no valor!", "red")

        def ver_historico(e):
            cursor = db.cursor()
            cursor.execute("SELECT user, produto, qtd, valor FROM lancamentos ORDER BY id DESC LIMIT 5")
            vendas = cursor.fetchall()
            lista_historico.controls = [ft.Text("HISTÓRICO RECENTE:", weight="bold", color="#666666")]
            for v in vendas:
                lista_historico.controls.append(ft.Text(f"👤 {v[0]} | {v[1]}: {v[2]} (R$ {v[3]:.2f})", size=13))
            page.update()

        container_principal.controls = [
            ft.Row([
                ft.Text(f"ADMIN: {estado['usuario_atual']}", color=COR_BANANA, weight="bold"),
                ft.Text("SENNA", size=24, weight="bold", italic=True, color=COR_BANANA)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#222222"),
            ft.Container(
                content=ft.Column([
                    ft.Text("NOVO LANÇAMENTO", weight="bold"),
                    in_cacau,
                    ft.ElevatedButton("CONFIRMAR CACAU", bgcolor=COR_CACAU, on_click=lambda _: salvar_venda("Cacau", in_cacau, 600, COR_CACAU)),
                    ft.Divider(height=10, color="transparent"),
                    in_banana,
                    ft.ElevatedButton("CONFIRMAR BANANA", bgcolor=COR_BANANA, color="black", on_click=lambda _: salvar_venda("Banana", in_banana, 50, COR_BANANA)),
                ], horizontal_alignment="center"),
                padding=20, bgcolor=COR_CARD, border_radius=15
            ),
            ft.ElevatedButton("ATUALIZAR RELATÓRIO", on_click=ver_historico),
            lista_historico,
            ft.TextButton("SAIR", on_click=lambda _: page.window_destroy()) # Fecha ou reinicia
        ]
        page.update()

    # Iniciar no Login
    container_principal.controls = [tela_login]
    page.add(container_principal)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
