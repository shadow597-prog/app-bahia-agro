import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS (NOVA VERSÃO PARA EVITAR CONFLITO) ---
def init_db():
    # Mudamos o nome do arquivo para forçar a criação de um novo banco limpo
    conn = sqlite3.connect("senna_final_v1.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       login TEXT UNIQUE, 
                       senha TEXT, 
                       cargo TEXT DEFAULT 'pendente')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    
    # Criar o seu acesso de mestre
    try:
        cursor.execute("INSERT INTO usuarios (login, senha, cargo) VALUES (?, ?, ?)", ("shadow", "1234", "ceo"))
    except: pass
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA AGRO"
    page.bgcolor = "#0b0b0b"
    page.padding = 20
    
    # Estado do app
    sessao = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"

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
        ir_painel(None)

    # --- TELA: PAINEL PRINCIPAL ---
    def ir_painel(e):
        page.controls.clear()
        
        conteudo = ft.Column(horizontal_alignment="center", spacing=20)
        
        # Boas vindas
        conteudo.controls.append(
            ft.Text(f"BEM-VINDO, {sessao['user'].upper()} ({sessao['cargo'].upper()})", 
                    color=COR_BANANA, weight="bold")
        )

        # Se for PENDENTE, bloqueia tudo
        if sessao["cargo"] == "pendente":
            conteudo.controls.append(
                ft.Container(
                    content=ft.Text("AGUARDANDO LIBERAÇÃO DO CEO SHADOW", color="red", size=20, text_align="center"),
                    padding=50, border=ft.border.all(1, "red"), border_radius=10
                )
            )
        
        # Se for CEO, mostra gestão
        elif sessao["cargo"] == "ceo":
            cursor = db.cursor()
            cursor.execute("SELECT id, login, cargo FROM usuarios WHERE cargo = 'pendente'")
            pendentes = cursor.fetchall()
            
            if pendentes:
                lista_gestao = ft.Column([ft.Text("USUÁRIOS AGUARDANDO:", weight="bold")])
                for p in pendentes:
                    lista_gestao.controls.append(
                        ft.Row([
                            ft.Text(p[1]),
                            ft.ElevatedButton("LIBERAR", on_click=lambda _, idx=p[0]: promover(idx, "operador"))
                        ], alignment="center")
                    )
                conteudo.controls.append(ft.Container(content=lista_gestao, padding=10, bgcolor="#1a1a1a"))

        # Botão Sair
        conteudo.controls.append(ft.TextButton("SAIR DO SISTEMA", on_click=lambda _: page.window_destroy()))
        
        page.add(conteudo)

    # --- TELA: LOGIN ---
    def logar(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", (ui_user.value, ui_pass.value))
        res = cursor.fetchone()
        if res:
            sessao["user"], sessao["cargo"] = res[0], res[1]
            ir_painel(None)
        else:
            mostrar_aviso("Usuário ou senha inválidos", "red")

    def cadastrar(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (ui_user.value, ui_pass.value))
            db.commit()
            mostrar_aviso("Cadastro solicitado!", "blue")
        except:
            mostrar_aviso("Nome já em uso", "red")

    ui_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    ui_pass = ft.TextField(label="Senha", password=True, border_color=COR_BANANA)

    page.add(
        ft.Column([
            ft.Text("SENNA LOGIN", size=30, weight="bold", color=COR_BANANA),
            ui_user,
            ui_pass,
            ft.ElevatedButton("ENTRAR", on_click=logar, bgcolor=COR_BANANA, color="black", width=200),
            ft.TextButton("SOLICITAR ACESSO", on_click=cadastrar)
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
