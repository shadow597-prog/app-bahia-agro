import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DE ESTILO GLOBAL ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def iniciar_banco():
    conn = sqlite3.connect('fazenda_v3.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS producao 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, cultura TEXT, variedade TEXT, 
                       processo TEXT, quantidade REAL, unidade TEXT, data TEXT)''')
    conn.commit()
    conn.close()

class AppGestaoRural(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela
        self.title("BAHIA AGRO v4.0")
        self.geometry("1200x900")
        
        # Cores Premium
        self.COR_CACAU = "#8B4513"  # SaddleBrown mais sóbrio
        self.COR_BANANA = "#EAB308" # Amarelo ouro moderno
        self.COR_FUNDO_CARD = "#1e293b" # Slate escuro
        self.senha_admin = "1234"
        self.admin_ativo = False

        # Container Principal com padding
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Cabeçalho Estilizado
        self.header = ctk.CTkLabel(self.main_container, text="SISTEMA GESTÃO DE SAFRA", 
                                  font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"))
        self.header.pack(pady=(0, 20))

        # Abas com design arredondado
        self.abas_principais = ctk.CTkTabview(self.main_container, 
                                             segmented_button_fg_color="#334155",
                                             segmented_button_selected_color="#3b82f6",
                                             corner_radius=15)
        self.abas_principais.pack(fill="both", expand=True)
        
        self.abas_principais.add("📊 Planilhas")
        self.abas_principais.add("➕ Novo Lançamento")
        self.abas_principais.add("📖 Conhecimento")

        self.setup_planilhas()
        self.setup_lancamento()
        self.setup_conhecimento()
        self.carregar_dados()

    def setup_planilhas(self):
        tab_pai = self.abas_principais.tab("📊 Planilhas")
        
        # Estilização da Tabela (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#0f172a", 
                        foreground="#f8fafc", 
                        rowheight=38, 
                        fieldbackground="#0f172a", 
                        font=("Segoe UI", 10),
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background="#334155", 
                        foreground="white", 
                        font=("Segoe UI", 11, "bold"),
                        relief="flat")
        style.map("Treeview", background=[('selected', '#3b82f6')])

        # Sub-abas de planilha com botões menores
        self.sub_plan = ctk.CTkTabview(tab_pai, fg_color="transparent", height=600)
        self.sub_plan.pack(fill="both", expand=True, padx=10)
        self.sub_plan.add("Cacau")
        self.sub_plan.add("Banana")

        # --- SEÇÃO CACAU ---
        p_c = self.sub_plan.tab("Cacau")
        self.card_c = self.criar_card_resumo(p_c, "Resumo Produção Cacau", self.COR_CACAU)
        self.lbl_total_cacau = ctk.CTkLabel(self.card_c, text="0.0 @", font=("Arial", 24, "bold"), text_color="white")
        self.lbl_total_cacau.pack(pady=10)
        
        self.tab_cacau = self.criar_tabela_ui(p_c)
        self.btn_del_c = ctk.CTkButton(p_c, text="Deletar Registro", fg_color="#475569", state="disabled", 
                                      corner_radius=8, command=lambda: self.deletar(self.tab_cacau))
        self.btn_del_c.pack(pady=10)

        # --- SEÇÃO BANANA ---
        p_b = self.sub_plan.tab("Banana")
        self.card_b = self.criar_card_resumo(p_b, "Resumo Produção Banana", self.COR_BANANA)
        self.lbl_total_banana = ctk.CTkLabel(self.card_b, text="0 itens", font=("Arial", 24, "bold"), text_color="black")
        self.lbl_total_banana.pack(pady=10)

        self.tab_banana = self.criar_tabela_ui(p_b)
        self.btn_del_b = ctk.CTkButton(p_b, text="Deletar Registro", fg_color="#475569", state="disabled", 
                                      corner_radius=8, command=lambda: self.deletar(self.tab_banana))
        self.btn_del_b.pack(pady=10)

        # Botão Admin Flutuante/Discreto
        self.btn_lock = ctk.CTkButton(tab_pai, text="MODO ADMIN", fg_color="#1e293b", border_width=1, 
                                     border_color="#3b82f6", height=40, command=self.trava_seguranca)
        self.btn_lock.pack(pady=5)

    def criar_card_resumo(self, master, titulo, cor):
        card = ctk.CTkFrame(master, fg_color=cor, corner_radius=12, height=100)
        card.pack(fill="x", padx=30, pady=15)
        ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 12, "bold"), text_color="white" if cor != self.COR_BANANA else "black").pack(pady=(10,0))
        return card

    def criar_tabela_ui(self, master):
        frame = ctk.CTkFrame(master, fg_color="#0f172a", corner_radius=10, border_width=1, border_color="#334155")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        cols = ("ID", "Variedade", "Processo/Tipo", "Qtd", "Unidade", "Data")
        tabela = ttk.Treeview(frame, columns=cols, show="headings")
        
        # Zebrado customizado
        tabela.tag_configure('odd', background='#1e293b')
        tabela.tag_configure('even', background='#0f172a')

        for col in cols:
            tabela.heading(col, text=col)
            tabela.column(col, anchor="center", width=110)
        tabela.column("ID", width=50)

        tabela.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        return tabela

    def setup_lancamento(self):
        tab = self.abas_principais.tab("➕ Novo Lançamento")
        
        # Grid para os dois setores de lançamento lado a lado
        frame_grid = ctk.CTkFrame(tab, fg_color="transparent")
        frame_grid.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- COLUNA CACAU ---
        f_c = ctk.CTkFrame(frame_grid, fg_color=self.COR_FUNDO_CARD, corner_radius=15, border_width=1, border_color=self.COR_CACAU)
        f_c.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        ctk.CTkLabel(f_c, text="LANÇAR CACAU", font=("Segoe UI", 18, "bold"), text_color=self.COR_CACAU).pack(pady=20)
        
        self.var_c = self.criar_input(f_c, "Variedade", ["PS-1319", "CCN-51", "Comum", "Parazinho"])
        self.proc_c = self.criar_input(f_c, "Processo", ["Secado ao Sol", "Torrado (Nibs)", "Fermentado", "In Natura"])
        self.qtd_c = ctk.CTkEntry(f_c, placeholder_text="Quantidade em @", height=45, corner_radius=8)
        self.qtd_c.pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(f_c, text="GRAVAR CACAU", fg_color=self.COR_CACAU, height=50, corner_radius=8, command=lambda: self.salvar("Cacau")).pack(pady=30, padx=40, fill="x")

        # --- COLUNA BANANA ---
        f_b = ctk.CTkFrame(frame_grid, fg_color=self.COR_FUNDO_CARD, corner_radius=15, border_width=1, border_color=self.COR_BANANA)
        f_b.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        ctk.CTkLabel(f_b, text="LANÇAR BANANA", font=("Segoe UI", 18, "bold"), text_color=self.COR_BANANA).pack(pady=20)
        
        self.var_b = self.criar_input(f_b, "Variedade", ["Prata", "Nanica", "Terra", "Maçã"])
        self.tipo_b = self.criar_input(f_b, "Tipo", ["De Primeira", "De Segunda", "Madura", "Verde"])
        self.uni_b = ctk.CTkSegmentedButton(f_b, values=["Kg", "Cento", "Caixa"], selected_color=self.COR_BANANA, selected_hover_color="#ca8a04")
        self.uni_b.set("Cento")
        self.uni_b.pack(pady=10)
        self.qtd_b = ctk.CTkEntry(f_b, placeholder_text="Quantidade", height=45, corner_radius=8)
        self.qtd_b.pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(f_b, text="GRAVAR BANANA", fg_color=self.COR_BANANA, text_color="black", height=50, corner_radius=8, command=lambda: self.salvar("Banana")).pack(pady=30, padx=40, fill="x")

    def criar_input(self, master, label, valores):
        combo = ctk.CTkComboBox(master, values=valores, height=45, corner_radius=8, fg_color="#334155")
        combo.set(label)
        combo.pack(pady=10, padx=40, fill="x")
        return combo

    def setup_conhecimento(self):
        tab = self.abas_principais.tab("📖 Conhecimento")
        info = ctk.CTkTextbox(tab, font=("Consolas", 14), corner_radius=15, border_width=1, border_color="#334155", fg_color="#0f172a")
        info.pack(padx=30, pady=30, fill="both", expand=True)
        
        guia = """
    >>> GUIA DE VARIEDADES - GESTÃO AGRO BAHIA <<<

    [ CACAU ]
    ----------------------------------------------------------
    * PS-1319: Alta produtividade e amêndoas pesadas. Resistente.
    * CCN-51:  O 'trator' do cacau. Alta manteiga, exige fermentação fria.
    * COMUM:   Sabor chocolate intenso. Cultivado na sombra (Cabruca).
    * PARAZINHO: Variedade fina, amêndoas de alto sabor aromático.

    [ BANANA ]
    ----------------------------------------------------------
    * PRATA:   Melhor durabilidade pós-colheita. Equilíbrio doce/ácido.
    * NANICA:  Porte baixo, muito doce. Ótima para indústria de doces.
    * TERRA:   Grande, para cozinhar/fritar. Alto valor de mercado.
    * MAÇÃ:    Sabor premium, aroma de maçã. Rara e valorizada.
    """
        info.insert("0.0", guia)
        info.configure(state="disabled")

    def salvar(self, cultura):
        try:
            conn = sqlite3.connect('fazenda_v3.db')
            cursor = conn.cursor()
            data = datetime.now().strftime("%d/%m/%Y")
            if cultura == "Cacau":
                v, p, q, u = self.var_c.get(), self.proc_c.get(), float(self.qtd_c.get()), "@"
                self.qtd_c.delete(0, 'end')
            else:
                v, p, q, u = self.var_b.get(), self.tipo_b.get(), float(self.qtd_b.get()), self.uni_b.get()
                self.qtd_b.delete(0, 'end')
            
            cursor.execute("INSERT INTO producao (cultura, variedade, processo, quantidade, unidade, data) VALUES (?,?,?,?,?,?)",
                           (cultura, v, p, q, u, data))
            conn.commit()
            conn.close()
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Dados salvos no banco!")
        except:
            messagebox.showerror("Erro", "Verifique se a quantidade é um número.")

    def carregar_dados(self):
        for i in self.tab_cacau.get_children(): self.tab_cacau.delete(i)
        for i in self.tab_banana.get_children(): self.tab_banana.delete(i)
        
        conn = sqlite3.connect('fazenda_v3.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producao")
        rows = cursor.fetchall()
        tc, tb, cc, cb = 0, 0, 0, 0
        
        for r in rows:
            d = (r[0], r[2], r[3], r[4], r[5], r[6])
            if r[1] == "Cacau":
                tag = 'even' if cc % 2 == 0 else 'odd'
                self.tab_cacau.insert("", "end", values=d, tags=(tag,))
                tc += r[4]; cc += 1
            else:
                tag = 'even' if cb % 2 == 0 else 'odd'
                self.tab_banana.insert("", "end", values=d, tags=(tag,))
                tb += r[4]; cb += 1
        
        conn.close()
        self.lbl_total_cacau.configure(text=f"{tc:.1f} Arrobas (@)")
        self.lbl_total_banana.configure(text=f"{tb:.1f} Un/Kg")

    def trava_seguranca(self):
        if not self.admin_ativo:
            if simpledialog.askstring("Acesso", "Senha Admin:", show="*") == self.senha_admin:
                self.admin_ativo = True
                self.btn_lock.configure(text="Sair Admin", fg_color="#ef4444")
                self.btn_del_c.configure(state="normal", fg_color="#dc2626")
                self.btn_del_b.configure(state="normal", fg_color="#dc2626")
        else:
            self.admin_ativo = False
            self.btn_lock.configure(text="MODO ADMIN", fg_color="#1e293b")
            self.btn_del_c.configure(state="disabled", fg_color="#475569")
            self.btn_del_b.configure(state="disabled", fg_color="#475569")

    def deletar(self, tabela):
        sel = tabela.selection()
        if sel:
            id_db = tabela.item(sel)['values'][0]
            conn = sqlite3.connect('fazenda_v3.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producao WHERE id=?", (id_db,))
            conn.commit(); conn.close(); self.carregar_dados()

if __name__ == "__main__":
    iniciar_banco()
    app = AppGestaoRural()
    app.mainloop()