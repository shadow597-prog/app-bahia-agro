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
    page.bgcolor = "#000000"
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"

    def alterar_status(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        montar_sistema()

    # --- GERADORES DE CONTEÚDO ---
    def view_vendas():
        in_qtd = ft.TextField(label="Qtd", border_color=COR_BANANA)
        def salvar(p, pr):
            try:
                q = float(in_qtd.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], p, q, q*pr))
                db.commit()
                in_qtd.value = ""
                page.update()
            except: pass

        return ft.Column([
            ft.Text("VENDAS", weight="bold", color=COR_BANANA),
            in_qtd,
            ft.Row([
                ft.ElevatedButton("CACAU", on_click=lambda _: salvar("Cacau", 600)),
                ft.ElevatedButton("BANANA", on_click=lambda _: salvar("Banana", 50)),
            ])
        ])

    def view_equipe():
        cursor = db.cursor()
        cursor.execute("SELECT id, login FROM usuarios WHERE cargo = 'pendente'")
        pendentes = cursor.fetchall()
        col = ft.Column([ft.Text("PEDIDOS DE ACESSO", color=COR_BANANA)])
        for p in pendentes:
            col.controls.append(ft.Row([
                ft.Text(p[1]),
                ft.TextButton("ACEITAR", on_click=lambda _, idx=p[0]: alterar_status(idx, "operador"))
            ]))
        return col

    def view_planilha():
        cursor = db.cursor()
        cursor.execute("SELECT user, produto, qtd, valor FROM lancamentos ORDER BY id DESC")
        dados = cursor.fetchall()
        tabela = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Quem")), ft.DataColumn(ft.Text("Total"))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(d[0]))), ft.DataCell(ft.Text(f"R${d[3]:.2f}"))]) for d in dados]
        )
        return ft.Column([tabela], scroll=ft.ScrollMode.ALWAYS)

    # --- MONTAGEM DO SISTEMA (ESTRUTURA COMPATÍVEL) ---
    def montar_sistema():
        page.controls.clear()
        
        # Criamos os conteúdos primeiro
        cont_vendas = view_vendas()
        cont_equipe = view_equipe()
        cont_planilha = view_planilha()

        # Escondemos todos
        cont_equipe.visible = False
        cont_planilha.visible = False

        def mudar_aba(e):
            idx = e.control.selected_index
            cont_vendas.visible = (idx == 0)
            cont_equipe.visible = (idx == 1) if sessao["cargo"] == "ceo" else False
            cont_planilha.visible = (idx == 2) if sessao["cargo"] == "ceo" else False
            page.update()

        abas = [ft.Tab(label="VENDAS")]
        if sessao["cargo"] == "ceo":
            abas.append(ft.Tab(label="EQUIPE"))
            abas.append(ft.Tab(label="PLANILHA"))

        # No Flet antigo, a Tab não tem 'content'. 
        # A gente coloca as Tabs em cima e os Columns embaixo.
        page.add(
            ft.Row([ft.Text("SENNA", color=COR_BANANA, size=20, weight="bold")]),
            ft.Tabs(tabs=abas, on_change=mudar_aba),
            cont_vendas,
            cont_equipe,
            cont_planilha
        )
        page.update()

    # --- LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            montar_sistema()

    ui_user = ft.TextField(label="Usuário")
    ui_pass = ft.TextField(label="Senha", password=True)
    page.add(ft.Column([ft.Text("LOGIN"), ui_user, ui_pass, ft.ElevatedButton("ENTRAR", on_click=logar)]))

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
