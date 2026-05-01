import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS (Com suporte a Cargos) ---
def init_db():
    conn = sqlite3.connect("senna_corporation.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabela de Usuários com coluna 'cargo' e 'status'
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       login TEXT UNIQUE, 
                       senha TEXT, 
                       cargo TEXT DEFAULT 'pendente')''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    
    # Criar o CEO Shadow automaticamente se não existir
    try:
        cursor.execute("INSERT INTO usuarios (login, senha, cargo) VALUES (?, ?, ?)", ("shadow", "1234", "ceo"))
    except: pass
    
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - CORPORATE SYSTEM"
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"user": None, "cargo": None}
    COR_BANANA = "#EAB308"
    COR_CARD = "#121212"

    container_principal = ft.Column(horizontal_alignment="center", spacing=20)

    def mostrar_aviso(texto, cor):
        aviso = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(aviso)
        aviso.open = True
        page.update()

    # --- LÓGICA DE GESTÃO DE CARGOS ---
    def promover_usuario(id_user, novo_cargo):
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET cargo = ? WHERE id = ?", (novo_cargo, id_user))
        db.commit()
        mostrar_aviso(f"Usuário atualizado para {novo_cargo}!", "green")
        montar_dashboard() # Atualiza a tela

    # --- INTERFACE: DASHBOARD ---
    def montar_dashboard():
        container_principal.controls.clear()
        
        # Cabeçalho Hierárquico
        cabecalho = ft.Row([
            ft.Column([
                ft.Text(f"USUÁRIO: {estado['user'].upper()}", size=12, color="#666666"),
                ft.Text(f"CARGO: {estado['cargo'].upper()}", size=14, color=COR_BANANA, weight="bold"),
            ]),
            ft.Text("SENNA", size=28, weight="bold", italic=True, color=COR_BANANA)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # BLOQUEIO PARA PENDENTES
        if estado["cargo"] == "pendente":
            container_principal.controls = [
                cabecalho,
                ft.Container(
                    content=ft.Text("⚠️ ACESSO BLOQUEADO\nAguarde o CEO Shadow promover seu acesso.", 
                                   text_align="center", size=18, color="red"),
                    padding=50, bgcolor=COR_CARD, border_radius=20
                ),
                ft.ElevatedButton("SAIR / RECARREGAR", on_click=lambda _: page.update())
            ]
            page.update()
            return

        # SEÇÃO EXCLUSIVA DO CEO: GESTÃO DE EQUIPE
        sessao_ceo = ft.Column()
        if estado["cargo"] == "ceo":
            cursor = db.cursor()
            cursor.execute("SELECT id, login, cargo FROM usuarios WHERE cargo = 'pendente' OR cargo = 'operador'")
            equipe = cursor.fetchall()
            
            lista_promocao = ft.Column([ft.Text("--- GESTÃO DE EQUIPE (CEO ONLY) ---", weight="bold")])
            for p in equipe:
                lista_promocao.controls.append(
                    ft.Row([
                        ft.Text(f"{p[1]} ({p[2]})"),
                        ft.TextButton("PROMOVER OPERADOR", on_click=lambda _, idx=p[0]: promover_usuario(idx, "operador")),
                        ft.TextButton("PROMOVER GERENTE", on_click=lambda _, idx=p[0]: promover_usuario(idx, "gerente"), font_color="blue"),
                    ], alignment="center")
                )
            sessao_ceo.controls = [ft.Container(content=lista_promocao, padding=20, bgcolor="#1a1a1a", border_radius=10)]

        # ÁREA DE LANÇAMENTOS (Disponível para Operadores, Gerentes e CEO)
        area_vendas = ft.Container(
            content=ft.Column([
                ft.Text("LANÇAR PRODUÇÃO", weight="bold"),
                ft.TextField(label="Quantidade", border_color=COR_BANANA, width=250),
                ft.ElevatedButton("CONFIRMAR REGISTRO", bgcolor=COR_BANANA, color="black")
            ], horizontal_alignment="center"),
            padding=20, bgcolor=COR_CARD, border_radius=15
        )

        container_principal.controls = [cabecalho, ft.Divider(color="#222222"), sessao_ceo, area_vendas]
        page.update()

    # --- TELAS INICIAIS (LOGIN E CADASTRO) ---
    def validar_login(e):
        cursor = db.cursor()
        cursor.execute("SELECT login, cargo FROM usuarios WHERE login = ? AND senha = ?", 
                       (campo_user.value, campo_pass.value))
        res = cursor.fetchone()
        if res:
            estado["user"], estado["cargo"] = res[0], res[1]
            montar_dashboard()
        else:
            mostrar_aviso("Dados incorretos!", "red")

    def registrar(e):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (campo_user.value, campo_pass.value))
            db.commit()
            mostrar_aviso("Cadastrado! Peça ao CEO para te liberar.", "blue")
        except: mostrar_aviso("Usuário já existe!", "red")

    campo_user = ft.TextField(label="Usuário", border_color=COR_BANANA)
    campo_pass = ft.TextField(label="Senha", password=True, can_reveal_password=True, border_color=COR_BANANA)
    
    tela_inicial = ft.Column([
        ft.Text("SENNA AGRO", size=35, weight="bold", color=COR_BANANA, italic=True),
        ft.Container(
            content=ft.Column([
                campo_user, campo_pass,
                ft.ElevatedButton("ENTRAR", on_click=validar_login, bgcolor=COR_BANANA, color="black", width=250),
                ft.TextButton("SOLICITAR ACESSO (CADASTRO)", on_click=registrar)
            ], horizontal_alignment="center"),
            padding=30, bgcolor=COR_CARD, border_radius=20
        )
    ], horizontal_alignment="center")

    container_principal.controls = [tela_inicial]
    page.add(container_principal)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
