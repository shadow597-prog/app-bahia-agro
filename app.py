import flet as ft
import sqlite3
import os

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("safra_senna.db", check_same_thread=False)
    cursor = conn.cursor()
    # Cria a tabela de safras se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS safras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            quantidade TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

def main(page: ft.Page):
    page.title = "SENNA - GESTÃO AGRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    COR_CACAU = "#8B4513"
    COR_BANANA = "#EAB308"
    COR_CARD = "#121212"

    texto_feedback = ft.Text("", size=16, weight="bold")

    # --- FUNÇÕES ---
    def salvar_no_banco(produto, valor):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO safras (produto, quantidade) VALUES (?, ?)", (produto, valor))
        conn.commit()

    def confirmar_cacau(e):
        if campo_cacau.value:
            salvar_no_banco("Cacau", campo_cacau.value)
            texto_feedback.value = f"✅ SENNA: {campo_cacau.value}@ de Cacau Salvas!"
            texto_feedback.color = COR_CACAU
            campo_cacau.value = ""
            page.update()

    def confirmar_banana(e):
        if campo_banana.value:
            salvar_no_banco("Banana", campo_banana.value)
            texto_feedback.value = f"✅ SENNA: {campo_banana.value} de Banana Salvas!"
            texto_feedback.color = COR_BANANA
            campo_banana.value = ""
            page.update()

    # --- INTERFACE ---
    header = ft.Row([
        ft.Text("BAHIA AGRO", size=18, color="#666666"),
        ft.Text("SENNA", size=26, weight="bold", italic=True, color=COR_BANANA)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    campo_cacau = ft.TextField(label="Qtd em @", border_color=COR_CACAU, width=250)
    campo_banana = ft.TextField(label="Qtd Banana", border_color=COR_BANANA, width=250)

    page.add(
        header,
        ft.Divider(color="#222222"),
        ft.Container(
            content=ft.Column([
                ft.Text("LANÇAMENTO DE SAFRA", weight="bold", size=20),
                campo_cacau,
                ft.ElevatedButton("SALVAR CACAU", bgcolor=COR_CACAU, color="white", on_click=confirmar_cacau),
                ft.Divider(height=20, color="transparent"),
                campo_banana,
                ft.ElevatedButton("SALVAR BANANA", bgcolor=COR_BANANA, color="black", on_click=confirmar_banana),
                ft.Container(content=texto_feedback, padding=10)
            ], horizontal_alignment="center"),
            padding=30, bgcolor=COR_CARD, border_radius=20
        )
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
