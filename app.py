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
    page.padding = 15
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"

    def mostrar_aviso(msg, cor):
        snack = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- TELAS (CONTAINERS) ---
    conteudo_principal = ft.Column(expand=True)

    def view_vendas():
        in_qtd = ft.TextField(label="Quantidade", border_color=COR_BANANA, width=250)
        def salvar(p, pr):
            if not in_qtd.value: return
            try:
                q = float(in_qtd.value.replace(",", "."))
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], p, q, q*pr))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"Venda de {p} salva!", "green")
            except: mostrar_aviso("Valor inválido", "red")

        return ft.Column([
            ft.Text("LANÇAR PRODUÇÃO", size=18, weight="bold"),
            in_qtd,
            ft.ElevatedButton("CACAU (R$ 600)", on_click=lambda _: salvar("Cacau", 600), bgcolor=COR_CACAU, color="white", width=250),
            ft.ElevatedButton("BANANA (R$ 50)", on_click=lambda _: salvar("Banana", 50), bgcolor=COR_BANANA, color="black", width=250),
        ], horizontal_alignment="center")

    def view_equipe():
        cursor = db.cursor()
        cursor.execute("SELECT id, login FROM usuarios WHERE cargo = 'pendente'")
        pendentes = cursor.fetchall()
        
        lista = ft.Column([ft.Text("APROVAR NOVOS", weight="bold", color=COR_BANANA)])
        for p in pendentes:
            def aprovar(e, idx=p[0]):
                cursor.execute("UPDATE usuarios SET cargo = 'operador' WHERE id = ?", (idx,))
                db.commit()
                navegar("equipe")

            lista.controls.append(ft.Row([
                ft.Text(p[1]),
                ft.TextButton("LIBERAR", on_click=aprovar)
            ], alignment="center"))
        return lista

    def view_planilha():
        cursor = db.cursor()
        cursor.execute("SELECT user, produto, qtd, valor FROM lancamentos ORDER BY id DESC LIMIT 20")
        dados = cursor.fetchall()
        
        tabela = ft.Column([ft.Text("ÚLTIMOS LANÇAMENTOS", weight="bold")])
        for d in dados:
            tabela.controls.append(ft.Text(f"{d[0]} -> {d[1]} ({d[2]}): R$ {d[3]:.2f}", size=12))
        return ft.Column([tabela], scroll=ft.ScrollMode.ALWAYS)

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
        
        # Menu Superior feito com botões simples (Zero erro de versão)
        menu_botoes = [
            ft.ElevatedButton("VENDAS", on_click=lambda _: navegar("vendas"), bgcolor="#1a1a1a"),
        ]
        
        if sessao["cargo"] == "ceo":
            menu_botoes.append(ft.ElevatedButton("EQUIPE", on_click=lambda _: navegar("equipe"), bgcolor="#1a1a1a"))
            menu_botoes.append(ft.ElevatedButton("PLANILHA", on_click=lambda _: navegar("planilha"), bgcolor="#1a1a1a"))

        page.add(
            ft.Row([
                ft.Text("SENNA", size=22, weight="bold", color=COR_BANANA),
                ft.TextButton("SAIR", on_click=lambda _: page.window_destroy())
            ], alignment="spaceBetween"),
            ft.Row(menu_botoes, scroll=ft.ScrollMode.ALWAYS),
            ft.Divider(color="#333333"),
            conteudo_principal
        )
        navegar("vendas")

    # --- TELA DE LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            montar_sistema()
        else: mostrar_aviso("Usuário ou senha incorretos", "red")

    ui_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    page.add(
        ft.Column([
            ft.Text("SENNA AGRO", size=32, weight="bold", color=COR_BANANA),
            ui_user, ui_pass,
            ft.ElevatedButton("ENTRAR", on_click=logar, bgcolor=COR_BANANA, color="black", width=250),
            ft.TextButton("CRIAR CONTA", on_click=lambda _: mostrar_aviso("Peça ao Shadow para cadastrar você.", "blue"))
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
