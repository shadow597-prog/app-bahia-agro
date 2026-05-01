import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("senna_corporation.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       login TEXT UNIQUE, 
                       senha TEXT, 
                       cargo TEXT DEFAULT 'pendente')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    try:
        cursor.execute("INSERT INTO usuarios (login, senha, cargo) VALUES (?, ?, ?)", ("shadow", "1234", "ceo"))
    except: pass
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - CORPORATE"
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"
    COR_CARD = "#121212"

    container_principal = ft.Column(horizontal_alignment="center", spacing=20)

    def mostrar_aviso(texto, cor):
        aviso = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(aviso)
        aviso.open = True
        page.update()

    # --- LÓGICA DE PROMOÇÃO ---
    def promover_usuario(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        mostrar_aviso(f"Sucesso! Cargo alterado para {novo_cargo}", "green")
        montar_dashboard()

    # --- INTERFACE: DASHBOARD ---
    def montar_dashboard():
        container_principal.controls.clear()
        
        cabecalho = ft.Row([
            ft.Column([
                ft.Text(f"SISTEMA SENNA", size=10, color="#666666"),
                ft.Text(f"{estado['user'].upper()} ({estado['cargo'].upper()})", size=14, color=COR_BANANA, weight="bold"),
            ]),
            ft.Text("SENNA", size=28, weight="bold", italic=True, color=COR_BANANA)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # BLOQUEIO DE SEGURANÇA
        if estado["cargo"] == "pendente":
            container_principal.controls = [
                cabecalho,
                ft.Container(
                    content=ft.Text("ACESSO RESTRITO\n\nAguarde o CEO Shadow liberar sua entrada.", 
                                   text_align="center", size=16, color="red"),
                    padding=40, bgcolor=COR_CARD, border_radius=15
                )
            ]
            page.update()
            return

        # PAINEL DO CEO (GESTÃO)
        painel_ceo = ft.Column()
        if estado["cargo"] == "ceo":
            cursor = db.cursor()
            cursor.execute("SELECT id, login, cargo FROM usuarios WHERE cargo != 'ceo'")
            equipe = cursor.fetchall()
            
            lista = ft.Column([ft.Text("GESTÃO DE ACESSOS", weight="bold", size=16)])
            for p in equipe:
                lista.controls.append(
                    ft.Row([
                        ft.Text(f"{p[1]}", width=100),
                        ft.ElevatedButton("OPERADOR", on_click=lambda _, idx=p[0]: promover_usuario(idx, "operador"), bgcolor="blue", color="white"),
                        ft.ElevatedButton("GERENTE", on_click=lambda _, idx=p[0]: promover_usuario(idx, "gerente"), bgcolor="green", color="white"),
                    ], alignment="center")
                )
            painel_ceo.controls = [ft.Container(content=lista, padding=15, bgcolor="#1A1A1A", border_radius=10)]

        # FORMULÁRIO DE PRODUÇÃO
        in_qtd = ft.TextField(label="Quantidade", border_color=COR_BANANA, width=250)
        
        def salvar(prod, preco):
            if not in_qtd.value: return
            try:
                qtd = float(in_qtd.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (estado["user"], prod, qtd, qtd * preco))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"Registrado por {estado['user']}", "green")
                page.update()
            except: mostrar_aviso("Valor inválido", "red")

        form = ft.Container(
            content=ft.Column([
                in_qtd,
                ft.Row([
                    ft.ElevatedButton("CACAU", on_click=lambda _: salvar("Cacau", 600), bgcolor=COR_CACAU, color="white"),
                    ft.ElevatedButton("BANANA", on_click=lambda _: salvar("Banana", 50), bgcolor=COR_BANANA, color="black"),
                ], alignment="center")
            ], horizontal_alignment="center"),
            padding=20, bgcolor=COR_CARD, border_radius=15
        )

        container_principal.controls = [cabecalho, ft.Divider(color="#222222"), painel_ceo, form]
        page.update()

    # --- TELA DE LOGIN ---
    def login_click(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (c_user.value, c_pass.value))
        res = cursor.fetchone()
        if res:
            estado["user"], estado["cargo"] = res[0], res[1]
            montar_dashboard()
        else: mostrar_aviso("Erro: Login ou Senha inválidos", "red")

    def cadastrar_click(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (c_user.value, c_pass.value))
            db.commit()
            mostrar_aviso("Pedido enviado! Fale com o CEO.", "blue")
        except: mostrar_aviso("Este usuário já existe", "red")

    c_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    c_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    container_principal.controls = [
        ft.Text("SENNA AGRO", size=32, weight="bold", color=COR_BANANA, italic=True),
        ft.Container(
            content=ft.Column([
                c_user, c_pass,
                ft.ElevatedButton("ENTRAR", on_click=login_click, bgcolor=COR_BANANA, color="black", width=250),
                ft.TextButton("CRIAR NOVA CONTA", on_click=cadastrar_click, color="#666666")
            ], horizontal_alignment="center"),
            padding=30, bgcolor=COR_CARD, border_radius=20
        )
    ]
    page.add(container_principal)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
