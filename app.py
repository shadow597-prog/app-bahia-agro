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
    page.title = "SENNA - GESTÃO RURAL"
    page.bgcolor = "#000000"
    page.padding = 10
    
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"
    COR_CARD = "#121212"

    def mostrar_aviso(msg, cor):
        snack = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- LÓGICA DE GESTÃO ---
    def alterar_status(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        mostrar_aviso("Atualizado com sucesso!", "green")
        montar_sistema()

    # --- CONTEÚDO DAS ABAS ---
    def criar_aba_vendas():
        in_qtd = ft.TextField(label="Quantidade", border_color=COR_BANANA, width=300)
        
        def salvar(prod, preco, cor):
            if not in_qtd.value: return
            try:
                qtd = float(in_qtd.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], prod, qtd, qtd * preco))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"Registrado!", cor)
            except: mostrar_aviso("Erro no valor", "red")

        return ft.Column([
            ft.Text("LANÇAR PRODUÇÃO", size=18, weight="bold"),
            ft.Container(
                content=ft.Column([
                    in_qtd,
                    ft.Row([
                        ft.ElevatedButton("CACAU", on_click=lambda _: salvar("Cacau", 600, COR_CACAU), bgcolor=COR_CACAU, color="white"),
                        ft.ElevatedButton("BANANA", on_click=lambda _: salvar("Banana", 50, COR_BANANA), bgcolor=COR_BANANA, color="black"),
                    ], alignment="center"),
                ], horizontal_alignment="center"),
                padding=20, bgcolor=COR_CARD, border_radius=15
            )
        ])

    def criar_aba_equipe():
        cursor = db.cursor()
        # Solicitações Pendentes
        cursor.execute("SELECT id, login FROM usuarios WHERE cargo = 'pendente'")
        pendentes = cursor.fetchall()
        # Funcionários Ativos
        cursor.execute("SELECT login, cargo FROM usuarios WHERE cargo != 'pendente'")
        ativos = cursor.fetchall()

        col_pendentes = ft.Column([ft.Text("SOLICITAÇÕES DE CONTA", color=COR_BANANA, weight="bold")])
        for p in pendentes:
            col_pendentes.controls.append(ft.Row([
                ft.Text(p[1], width=100),
                ft.ElevatedButton("ACEITAR", on_click=lambda _, idx=p[0]: alterar_status(idx, "operador"), bgcolor="green", color="white")
            ]))

        col_ativos = ft.Column([ft.Text("LISTA DE FUNCIONÁRIOS", color=COR_BANANA, weight="bold")])
        for a in ativos:
            col_ativos.controls.append(ft.Row([
                ft.Icon(ft.icons.PERSON, size=16),
                ft.Text(f"{a[0].upper()} - Cargo: {a[1]}")
            ]))

        return ft.Column([col_pendentes, ft.Divider(), col_ativos], scroll=ft.ScrollMode.ALWAYS)

    def criar_aba_planilha():
        cursor = db.cursor()
        cursor.execute("SELECT user, produto, qtd, valor, data FROM lancamentos ORDER BY id DESC")
        dados = cursor.fetchall()

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Funcionário")),
                ft.DataColumn(ft.Text("Produto")),
                ft.DataColumn(ft.Text("Qtd")),
                ft.DataColumn(ft.Text("Total (R$)")),
                ft.DataColumn(ft.Text("Data")),
            ],
            rows=[]
        )

        for d in dados:
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(d[0]))),
                ft.DataCell(ft.Text(str(d[1]))),
                ft.DataCell(ft.Text(str(d[2]))),
                ft.DataCell(ft.Text(f"{d[3]:.2f}")),
                ft.DataCell(ft.Text(str(d[4])[:10])),
            ]))

        return ft.Column([
            ft.Text("PLANILHA DE MOVIMENTAÇÃO", size=18, weight="bold"),
            ft.Container(content=tabela, border_radius=10, bgcolor=COR_CARD)
        ], scroll=ft.ScrollMode.ALWAYS)

    # --- MONTAGEM DO SISTEMA ---
    def montar_sistema():
        page.controls.clear()
        
        # Cabeçalho
        header = ft.Row([
            ft.Text("SENNA CORPORATE", size=20, weight="bold", italic=True, color=COR_BANANA),
            ft.TextButton("SAIR", on_click=lambda _: page.window_destroy())
        ], alignment="center")

        if sessao["cargo"] == "pendente":
            page.add(header, ft.Container(content=ft.Text("🔒 AGUARDANDO LIBERAÇÃO", size=20), padding=50))
            return

        # Definição das Abas
        abas = [
            ft.Tab(text="VENDAS", content=criar_aba_vendas()),
        ]

        # Só o Shadow vê as abas de Equipe e Planilha
        if sessao["cargo"] == "ceo":
            abas.append(ft.Tab(text="EQUIPE", content=criar_aba_equipe()))
            abas.append(ft.Tab(text="PLANILHA", content=criar_aba_planilha()))

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=abas,
            expand=1,
        )

        page.add(header, t)
        page.update()

    # --- TELA DE LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            montar_sistema()
        else: mostrar_aviso("Acesso negado", "red")

    def cadastrar(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (ui_user.value, ui_pass.value))
            db.commit()
            mostrar_aviso("Solicitado! Fale com o Shadow.", "blue")
        except: mostrar_aviso("Usuário já existe", "red")

    ui_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    page.add(ft.Column([
        ft.Text("SENNA LOGIN", size=30, color=COR_BANANA, weight="bold"),
        ui_user, ui_pass,
        ft.ElevatedButton("ENTRAR", on_click=logar, bgcolor=COR_BANANA, color="black", width=250),
        ft.TextButton("PEDIR ACESSO", on_click=cadastrar)
    ], horizontal_alignment="center"))

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
