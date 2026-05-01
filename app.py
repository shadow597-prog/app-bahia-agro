import flet as ft
import sqlite3
import os

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("senna_agro.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, produto TEXT, qtd REAL, valor REAL)''')
    conn.commit()
    return conn

db = init_db()

def main(page: ft.Page):
    page.title = "SENNA - SISTEMA AGRO"
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variável simples para salvar o nome (evita erro de Session)
    estado = {"usuario": "Visitante"}
    
    COR_BANANA = "#EAB308"
    COR_CACAU = "#8B4513"

    container_principal = ft.Column(horizontal_alignment="center", spacing=20)

    def mostrar_aviso(texto, cor):
        aviso = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(aviso)
        aviso.open = True
        page.update()

    # --- LÓGICA DE SALVAMENTO ---
    def salvar_venda(produto, qtd_field, preco_unidade, cor):
        try:
            if not qtd_field.value:
                return
            qtd = float(qtd_field.value.replace(",", "."))
            total = qtd * preco_unidade
            
            cursor = db.cursor()
            cursor.execute("INSERT INTO lancamentos (user, produto, qtd, valor) VALUES (?, ?, ?, ?)", 
                           (estado["usuario"], produto, qtd, total))
            db.commit()
            
            qtd_field.value = ""
            mostrar_aviso(f"Registrado: {qtd} de {produto} (R$ {total:.2f})", cor)
            page.update()
        except ValueError:
            mostrar_aviso("Erro: Digite apenas números!", "red")

    # --- INTERFACE: DASHBOARD ---
    def montar_dashboard():
        container_principal.controls.clear()
        
        in_cacau = ft.TextField(label="Qtd em @", border_color=COR_CACAU, width=250)
        in_banana = ft.TextField(label="Qtd Cento/Kg", border_color=COR_BANANA, width=250)
        lista_historico = ft.Column(spacing=10)

        def atualizar_historico(e):
            cursor = db.cursor()
            cursor.execute("SELECT produto, qtd, valor FROM lancamentos ORDER BY id DESC LIMIT 5")
            vendas = cursor.fetchall()
            lista_historico.controls = [ft.Text("ÚLTIMOS LANÇAMENTOS:", weight="bold")]
            for v in vendas:
                lista_historico.controls.append(ft.Text(f"• {v[0]}: {v[1]} (R$ {v[2]:.2f})"))
            page.update()

        container_principal.controls = [
            ft.Row([
                ft.Text(f"LOGADO: {estado['usuario']}", color=COR_BANANA, weight="bold"),
                ft.Text("SENNA", size=24, weight="bold", italic=True, color=COR_BANANA)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#222222"),
            ft.Container(
                content=ft.Column([
                    ft.Text("LANÇAR PRODUÇÃO", weight="bold"),
                    in_cacau,
                    ft.ElevatedButton("SALVAR CACAU (R$ 600/@)", on_click=lambda _: salvar_venda("Cacau", in_cacau, 600, COR_CACAU)),
                    ft.Divider(height=10, color="transparent"),
                    in_banana,
                    ft.ElevatedButton("SALVAR BANANA (R$ 50/Un)", on_click=lambda _: salvar_venda("Banana", in_banana, 50, COR_BANANA)),
                ], horizontal_alignment="center"),
                padding=20, bgcolor="#121212", border_radius=15
            ),
            ft.TextButton("VER HISTÓRICO", on_click=atualizar_historico),
            lista_historico
        ]
        page.update()

    # --- INTERFACE: LOGIN ---
    def fazer_login(e):
        if campo_user.value:
            estado["usuario"] = campo_user.value # Salva na variável simples
            montar_dashboard()
        else:
            mostrar_aviso("Digite seu nome", "red")

    campo_user = ft.TextField(label="Nome do Funcionário", border_color=COR_BANANA, width=300)
    
    container_principal.controls = [
        ft.Text("SENNA AGRO", size=32, weight="bold", color=COR_BANANA),
        ft.Container(
            content=ft.Column([
                ft.Text("Acesse o sistema"),
                campo_user,
                ft.ElevatedButton("ENTRAR", on_click=fazer_login, bgcolor=COR_BANANA, color="black", width=200)
            ], horizontal_alignment="center"),
            padding=30, bgcolor="#121212", border_radius=15
        )
    ]
    
    page.add(container_principal)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
