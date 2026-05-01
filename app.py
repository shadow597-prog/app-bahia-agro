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
    page.title = "SENNA AGRO"
    page.bgcolor = "#000000"
    page.padding = 20
    
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"
    COR_CARD = "#121212"

    def mostrar_aviso(msg, cor):
        snack = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def promover(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        mostrar_aviso("Permissão concedida!", "green")
        montar_sistema()

    def montar_sistema():
        page.controls.clear()

        # Cabeçalho sem ícone (usando botão de texto para evitar erro de versão)
        header = ft.Row([
            ft.Column([
                ft.Text("SISTEMA SENNA", size=10, color="#666666"),
                ft.Text(f"{sessao['user'].upper()} ({sessao['cargo'].upper()})", size=16, color=COR_BANANA, weight="bold"),
            ]),
            ft.TextButton("SAIR", on_click=lambda _: page.window_destroy())
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        if sessao["cargo"] == "pendente":
            page.add(header, ft.Divider(), ft.Container(
                content=ft.Text("🔒 ACESSO PENDENTE\nO CEO Shadow precisa liberar seu usuário.", 
                               text_align="center", size=18, color="red"),
                padding=50, alignment=ft.alignment.center
            ))
            return

        # Área de Lançamento
        in_qtd = ft.TextField(label="Quantidade", border_color=COR_BANANA, width=300)
        lista_vendas = ft.Column(spacing=5)

        def salvar(prod, preco, cor):
            if not in_qtd.value: return
            try:
                qtd = float(in_qtd.value.replace(",", "."))
                total = qtd * preco
                cursor = db.cursor()
                cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                               (sessao["user"], prod, qtd, total))
                db.commit()
                in_qtd.value = ""
                mostrar_aviso(f"Registrado: R$ {total:.2f}", cor)
                atualizar_historico()
            except: mostrar_aviso("Erro no valor", "red")

        def atualizar_historico():
            cursor = db.cursor()
            cursor.execute("SELECT user, produto, qtd, valor FROM lancamentos ORDER BY id DESC LIMIT 5")
            vendas = cursor.fetchall()
            lista_vendas.controls = [ft.Text("ÚLTIMOS LANÇAMENTOS", weight="bold", size=12, color="#666666")]
            for v in vendas:
                lista_vendas.controls.append(ft.Text(f"👤 {v[0]} | {v[1]}: {v[2]} (R$ {v[3]:.2f})", size=13))
            page.update()

        botoes = ft.Container(
            content=ft.Column([
                in_qtd,
                ft.Row([
                    ft.ElevatedButton("CACAU", on_click=lambda _: salvar("Cacau", 600, COR_CACAU), bgcolor=COR_CACAU, color="white"),
                    ft.ElevatedButton("BANANA", on_click=lambda _: salvar("Banana", 50, COR_BANANA), bgcolor=COR_BANANA, color="black"),
                ], alignment="center"),
            ], horizontal_alignment="center"),
            padding=20, bgcolor=COR_CARD, border_radius=15
        )

        area_ceo = ft.Column()
        if sessao["cargo"] == "ceo":
            cursor = db.cursor()
            cursor.execute("SELECT id, login, cargo FROM usuarios WHERE cargo = 'pendente'")
            pendentes = cursor.fetchall()
            if pendentes:
                lista_p = ft.Column([ft.Text("GESTÃO DE EQUIPE", weight="bold", color=COR_BANANA)])
                for p in pendentes:
                    lista_p.controls.append(ft.Row([
                        ft.Text(f"{p[1]}"),
                        ft.ElevatedButton("LIBERAR", on_click=lambda _, idx=p[0]: promover(idx, "operador"))
                    ], alignment="center"))
                area_ceo.controls = [ft.Container(content=lista_p, padding=15, bgcolor="#1a1a1a", border_radius=10)]

        page.add(header, ft.Divider(color="#222222"), area_ceo, ft.Text("NOVO LANÇAMENTO", weight="bold"), botoes, ft.Divider(color="#222222"), lista_vendas)
        atualizar_historico()

    # --- LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            montar_sistema()
        else: mostrar_aviso("Login inválido", "red")

    def cadastrar(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (ui_user.value, ui_pass.value))
            db.commit()
            mostrar_aviso("Solicitação enviada!", "blue")
        except: mostrar_aviso("Usuário já existe", "red")

    ui_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    page.add(ft.Column([
        ft.Text("SENNA AGRO", size=32, weight="bold", italic=True, color=COR_BANANA),
        ft.Container(content=ft.Column([
            ui_user, ui_pass,
            ft.ElevatedButton("ENTRAR", on_click=logar, bgcolor=COR_BANANA, color="black", width=250),
            ft.TextButton("CRIAR CONTA", on_click=cadastrar)
        ], horizontal_alignment="center"), padding=30, bgcolor=COR_CARD, border_radius=20)
    ], horizontal_alignment="center"))

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
