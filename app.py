import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("senna_final_v1.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT UNIQUE, senha TEXT, cargo TEXT DEFAULT 'pendente')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    try:
        cursor.execute("INSERT INTO usuarios (login, senha, cargo) VALUES (?, ?, ?)", ("shadow", "1234", "ceo"))
    except: pass
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - GESTÃO"
    page.bgcolor = "#000000"
    
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"
    COR_CARD = "#121212"

    def mostrar_aviso(msg, cor):
        snack = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def alterar_status(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        mostrar_aviso("Status atualizado!", "green")
        montar_sistema()

    # --- ABAS ---
    def criar_aba_vendas():
        in_qtd = ft.TextField(label="Quantidade", border_color=COR_BANANA, width=280)
        
        def salvar(prod, preco, cor):
            if not in_qtd.value: return
            try:
                qtd = float(in_qtd.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], prod, qtd, qtd * preco))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"Venda de {prod} salva!", cor)
            except: mostrar_aviso("Erro no número", "red")

        return ft.Column([
            ft.Text("REGISTRAR PRODUÇÃO", size=18, weight="bold", color=COR_BANANA),
            ft.Container(
                content=ft.Column([
                    in_qtd,
                    ft.Row([
                        ft.ElevatedButton("CACAU", on_click=lambda _: salvar("Cacau", 600, COR_CACAU), bgcolor=COR_CACAU, color="white"),
                        ft.ElevatedButton("BANANA", on_click=lambda _: salvar("Banana", 50, COR_BANANA), bgcolor=COR_BANANA, color="black"),
                    ], alignment="center"),
                ], horizontal_alignment="center"),
                padding=20, bgcolor=COR_CARD, border_radius=10
            )
        ], scroll=ft.ScrollMode.ALWAYS)

    def criar_aba_equipe():
        cursor = db.cursor()
        cursor.execute("SELECT id, login FROM usuarios WHERE cargo = 'pendente'")
        pendentes = cursor.fetchall()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE cargo != 'pendente'")
        ativos = cursor.fetchall()

        col = ft.Column([ft.Text("SOLICITAÇÕES", weight="bold")])
        for p in pendentes:
            col.controls.append(ft.Row([
                ft.Text(p[1]),
                ft.TextButton("ACEITAR", on_click=lambda _, idx=p[0]: alterar_status(idx, "operador"))
            ]))
        
        col.controls.append(ft.Divider())
        col.controls.append(ft.Text("FUNCIONÁRIOS ATIVOS", weight="bold"))
        for a in ativos:
            col.controls.append(ft.Text(f"• {a[0]} ({a[1]})"))
        
        return col

    def criar_aba_planilha():
        cursor = db.cursor()
        cursor.execute("SELECT user, produto, qtd, valor, data FROM lancamentos ORDER BY id DESC")
        dados = cursor.fetchall()

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Quem")),
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Qtd")),
                ft.DataColumn(ft.Text("Total")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(d[0]))),
                    ft.DataCell(ft.Text(str(d[1]))),
                    ft.DataCell(ft.Text(str(d[2]))),
                    ft.DataCell(ft.Text(f"R${d[3]:.2f}")),
                ]) for d in dados
            ]
        )
        return ft.Column([tabela], scroll=ft.ScrollMode.ALWAYS)

    def montar_sistema():
        page.controls.clear()
        
        header = ft.Row([
            ft.Text("SENNA", size=20, weight="bold", color=COR_BANANA),
            ft.TextButton("SAIR", on_click=lambda _: page.window_destroy())
        ], alignment="spaceBetween")

        if sessao["cargo"] == "pendente":
            page.add(header, ft.Text("Aguarde o Shadow liberar seu acesso.", color="red"))
            return

        # Ajuste aqui: Usando 'label' em vez de 'text' para compatibilidade
        abas_lista = [
            ft.Tab(label="VENDAS", content=criar_aba_vendas()),
        ]

        if sessao["cargo"] == "ceo":
            abas_lista.append(ft.Tab(label="EQUIPE", content=criar_aba_equipe()))
            abas_lista.append(ft.Tab(label="PLANILHA", content=criar_aba_planilha()))

        page.add(header, ft.Tabs(tabs=abas_lista, expand=1))
        page.update()

    # --- LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            montar_sistema()
        else: mostrar_aviso("Erro de login", "red")

    def cadastrar(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (ui_user.value, ui_pass.value))
            db.commit()
            mostrar_aviso("Pedido enviado!", "blue")
        except: mostrar_aviso("Usuário já existe", "red")

    ui_user = ft.TextField(label="Login", border_color=COR_BANANA)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    page.add(ft.Column([
        ft.Text("SENNA AGRO", size=30, color=COR_BANANA, weight="bold"),
        ui_user, ui_pass,
        ft.ElevatedButton("ENTRAR", on_click=logar, bgcolor=COR_BANANA, color="black", width=250),
        ft.TextButton("CRIAR CONTA", on_click=cadastrar)
    ], horizontal_alignment="center"))

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
