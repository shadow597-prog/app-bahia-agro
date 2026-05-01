import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("senna_agro_v2.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabela de usuários com status 'pendente' por padrão
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT UNIQUE, senha TEXT, cargo TEXT DEFAULT 'pendente')''')
    # Tabela de vendas/lançamentos
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # Garante que o seu acesso sempre exista
    try:
        cursor.execute("INSERT INTO usuarios (login, senha, cargo) VALUES (?, ?, ?)", ("shadow", "1234", "ceo"))
    except: pass
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA AGRO"
    page.bgcolor = "#000000"
    page.padding = 15
    
    sessao = {"user": None, "cargo": None}
    COR_DESTAQUE = "#EAB308" # Amarelo Senna

    # --- COMPONENTES DE INTERFACE ---
    conteudo_principal = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    def mostrar_aviso(msg, cor):
        snack = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- TELAS ---
    
    def view_vendas():
        in_qtd = ft.TextField(label="Qtd (Kg / Und / @)", border_color=COR_DESTAQUE, width=280)
        
        # Lista expandida de produtos do seu comércio rural
        produtos = [
            {"nome": "Cacau", "preco": 600, "cor": "#8B4513"},
            {"nome": "Banana Prata", "preco": 50, "cor": "#EAB308"},
            {"nome": "Banana Da Terra", "preco": 75, "cor": "#D4AF37"},
            {"nome": "Uva", "preco": 120, "cor": "#6A5ACD"},
            {"nome": "Mandioca", "preco": 30, "cor": "#F5F5DC"},
            {"nome": "Açúcar", "preco": 5, "cor": "#FFFFFF"}
        ]

        def salvar(p_nome, p_preco, p_cor):
            if not in_qtd.value:
                mostrar_aviso("Digite a quantidade!", "red")
                return
            try:
                qtd = float(in_qtd.value.replace(",", "."))
                total = qtd * p_preco
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], p_nome, qtd, total))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"{p_nome} registrado: R$ {total:.2f}", p_cor)
            except: mostrar_aviso("Erro no valor digitado", "red")

        grid_botoes = ft.Column(spacing=10, horizontal_alignment="center")
        for p in produtos:
            grid_botoes.controls.append(
                ft.ElevatedButton(
                    f"{p['nome'].upper()}", 
                    on_click=lambda e, n=p['nome'], pr=p['preco'], c=p['cor']: salvar(n, pr, c),
                    bgcolor=p['cor'], color="black" if p['cor'] != "#8B4513" else "white",
                    width=280, height=45
                )
            )

        return ft.Column([
            ft.Text("REGISTRAR SAÍDA/VENDA", size=18, weight="bold", color=COR_DESTAQUE),
            in_qtd,
            ft.Divider(color="#222222"),
            grid_botoes
        ], horizontal_alignment="center")

    def view_equipe():
        cursor = db.cursor()
        # Lista de Espera (Pendentes)
        cursor.execute("SELECT id, login FROM usuarios WHERE cargo = 'pendente'")
        pendentes = cursor.fetchall()
        
        lista_espera = ft.Column([ft.Text("⏳ FILA DE ESPERA", weight="bold", color="orange")])
        if not pendentes:
            lista_espera.controls.append(ft.Text("Ninguém aguardando.", size=12, italic=True))
        
        for p in pendentes:
            def aprovar(e, idx=p[0], nome=p[1]):
                db.cursor().execute("UPDATE usuarios SET cargo = 'operador' WHERE id = ?", (idx,))
                db.commit()
                mostrar_aviso(f"{nome} aprovado!", "green")
                navegar("equipe")

            lista_espera.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"👤 {p[1]}", expand=True),
                        ft.IconButton(ft.icons.CHECK_CIRCLE, icon_color="green", on_click=aprovar),
                    ]),
                    padding=10, bgcolor="#1a1a1a", border_radius=10
                )
            )
        return lista_espera

    def view_planilha():
        cursor = db.cursor()
        cursor.execute("SELECT user, produto, qtd, valor, data FROM lancamentos ORDER BY id DESC LIMIT 30")
        dados = cursor.fetchall()
        
        col = ft.Column([ft.Text("RELATÓRIO DE VENDAS", weight="bold", color=COR_DESTAQUE)])
        for d in dados:
            data_format = d[4][11:16] # Pega só a hora/minuto
            col.controls.append(
                ft.Text(f"[{data_format}] {d[0]} vendeu {d[2]} de {d[1]} (R$ {d[3]:.2f})", size=12)
            )
        return col

    # --- NAVEGAÇÃO ---
    def navegar(destino):
        conteudo_principal.controls.clear()
        if destino == "vendas":
            conteudo_principal.controls.append(view_vendas())
        elif destino == "equipe":
            conteudo_principal.controls.append(view_equipe())
        elif destino == "planilha":
            conteudo_principal.controls.append(view_planilha())
        page.update()

    def montar_sistema():
        page.controls.clear()
        
        btn_equipe = []
        if sessao["cargo"] == "ceo":
            btn_equipe = [
                ft.IconButton(ft.icons.PEOPLE, on_click=lambda _: navegar("equipe"), icon_color=COR_DESTAQUE),
                ft.IconButton(ft.icons.LIST_ALT, on_click=lambda _: navegar("planilha"), icon_color=COR_DESTAQUE),
            ]

        page.add(
            ft.Row([
                ft.Text("SENNA AGRO", size=20, weight="bold", color=COR_DESTAQUE),
                ft.Row([
                    ft.IconButton(ft.icons.ADD_SHOPPING_CART, on_click=lambda _: navegar("vendas"), icon_color="white"),
                    *btn_equipe,
                    ft.IconButton(ft.icons.EXIT_TO_APP, on_click=lambda _: page.window_destroy(), icon_color="red"),
                ])
            ], alignment="spaceBetween"),
            ft.Divider(color="#333333"),
            conteudo_principal
        )
        navegar("vendas")

    # --- LOGIN / CADASTRO ---
    def realizar_login(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            if res[1] == "pendente":
                mostrar_aviso("Sua conta ainda está na FILA DE ESPERA. Aguarde o Shadow.", "orange")
            else:
                sessao["user"], sessao["cargo"] = res[0], res[1]
                montar_sistema()
        else: mostrar_aviso("Usuário ou senha incorretos", "red")

    def realizar_cadastro(e):
        if not ui_user.value or not ui_pass.value: return
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (ui_user.value, ui_pass.value))
            db.commit()
            mostrar_aviso("Cadastro realizado! Aguarde a liberação do Shadow.", "blue")
        except: mostrar_aviso("Este usuário já existe", "red")

    ui_user = ft.TextField(label="Usuário", border_color=COR_DESTAQUE)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_DESTAQUE)

    page.add(
        ft.Column([
            ft.Text("SENNA LOGIN", size=32, weight="bold", color=COR_DESTAQUE),
            ft.Container(
                content=ft.Column([
                    ui_user, ui_pass,
                    ft.ElevatedButton("ENTRAR", on_click=realizar_login, bgcolor=COR_DESTAQUE, color="black", width=250),
                    ft.TextButton("CRIAR NOVA CONTA", on_click=realizar_cadastro)
                ], horizontal_alignment="center"),
                padding=20, bgcolor="#121212", border_radius=15
            )
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
