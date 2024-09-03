import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

file_path = 'dados_financeiros.csv'

moedas = {
    'BRL': 'R$',
    'USD': '$',
    'EUR': '€',
    'JPY': '¥',
}

opcoes_descricao = [
    "Salário",
    "Venda",
    "Reembolso",
    "Compra",
    "Transação Bancária",
    "Outros"
]

def garantir_arquivo_csv():
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['última alteração', 'receita total', 'gastos totais', 'Descrição'])
        df.to_csv(file_path, index=False)

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

def formatar_data(data):
    return data.strftime('%d/%m/%y %H:%M')

def formatar_valor_exibicao(valor, moeda):
    if moeda == 'BRL':
        return f"{moedas[moeda]} {valor:,.2f}".replace('.', ',')
    elif moeda == 'USD':
        return f"{moedas[moeda]} {valor:,.2f}"
    # Adicione outras moedas conforme necessário
    return f"{moeda} {valor:,.2f}"

def depositar_receita(valor, descricao):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        if not data.empty:
            ultima_receita = data['receita total'].iloc[-1]
            ultimo_gasto = data['gastos totais'].iloc[-1]
        else:
            ultima_receita = 0.0
            ultimo_gasto = 0.0
    else:
        ultima_receita = 0.0
        ultimo_gasto = 0.0

    nova_receita = ultima_receita + valor
    novo_dado = pd.DataFrame({
        'última alteração': [formatar_data(pd.Timestamp.now())],
        'receita total': [nova_receita],
        'gastos totais': [ultimo_gasto],
        'Descrição': [descricao]
    })
    novo_dado.to_csv(file_path, mode='a', header=False, index=False)
    atualizar_treeview()

def pagar(valor, descricao):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        if not data.empty:
            ultima_receita = data['receita total'].iloc[-1]
            ultimo_gasto = data['gastos totais'].iloc[-1]
        else:
            ultima_receita = 0.0
            ultimo_gasto = 0.0
    else:
        ultima_receita = 0.0
        ultimo_gasto = 0.0

    novo_gasto = ultimo_gasto + valor
    nova_receita = ultima_receita - valor
    novo_dado = pd.DataFrame({
        'última alteração': [formatar_data(pd.Timestamp.now())],
        'receita total': [nova_receita],
        'gastos totais': [novo_gasto],
        'Descrição': [descricao]
    })
    novo_dado.to_csv(file_path, mode='a', header=False, index=False)
    atualizar_treeview()

def atualizar_treeview():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        try:
            data = pd.read_csv(file_path)
            if not data.empty:
                data = data.iloc[::-1]  # Inverte a ordem para mostrar a receita mais recente no topo
                tree.delete(*tree.get_children())  # Remove todas as linhas existentes
                for i, row in data.iterrows():
                    tree.insert("", "end", values=list(row))
                if tree.get_children():
                    primeiro_item = tree.get_children()[0]
                    tree.item(primeiro_item, tags=('recent',))
                    tree.tag_configure('recent', background='#d9edf7', foreground='black')
            else:
                tree.delete(*tree.get_children())  # Remove todas as linhas existentes se o DataFrame estiver vazio
        except Exception as e:
            print(f"Erro ao atualizar o Treeview: {e}")

def criar_interface():
    global tree, valor_entry, descricao_combobox, moeda_var, receita_valor_label, gastos_valor_label

    root = tk.Tk()
    root.title("Controle Financeiro")
    root.geometry("800x500")
    root.configure(bg='#f5f5f5')

    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("Treeview",
                    background="#f5f5f5",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    top_info_frame = tk.Frame(root, bg='#f5f5f5')
    top_info_frame.pack(pady=5, fill='x')

    receita_label = tk.Label(top_info_frame, text="Receita", fg='green', bg='#f5f5f5', font=("Arial", 12, "bold"))
    receita_label.pack(side='left', padx=(10, 5))

    receita_valor_label = tk.Label(top_info_frame, text="", fg='green', bg='#f5f5f5', font=("Arial", 12))
    receita_valor_label.pack(side='left', padx=(5, 20))

    gastos_label = tk.Label(top_info_frame, text="Gastos", fg='red', bg='#f5f5f5', font=("Arial", 12, "bold"))
    gastos_label.pack(side='left', padx=(10, 5))

    gastos_valor_label = tk.Label(top_info_frame, text="", fg='red', bg='#f5f5f5', font=("Arial", 12))
    gastos_valor_label.pack(side='left', padx=(5, 10))

    tree_frame = tk.Frame(root)
    tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=('última alteração', 'receita total', 'gastos totais', 'Descrição'),
                        show='headings')
    tree.heading('última alteração', text='Última Alteração')
    tree.heading('receita total', text='Receita Total')
    tree.heading('gastos totais', text='Gastos Totais')
    tree.heading('Descrição', text='Descrição')

    tree.column('última alteração', width=150)
    tree.column('receita total', width=100)
    tree.column('gastos totais', width=100)
    tree.column('Descrição', width=300)
    tree.pack(expand=True, fill='both')

    bottom_frame = tk.Frame(root, bg='#f5f5f5')
    bottom_frame.pack(pady=10, fill='x')

    tk.Label(bottom_frame, text="Moeda:", bg='#f5f5f5').pack(side='left', padx=10)
    moeda_var = tk.StringVar(value='BRL')
    moeda_combo = ttk.Combobox(bottom_frame, textvariable=moeda_var, values=list(moedas.keys()), state='readonly')
    moeda_combo.pack(side='left', padx=10)
    moeda_combo.bind('<<ComboboxSelected>>', moeda_change)

    valor_frame = tk.Frame(bottom_frame, bg='#f5f5f5')
    valor_frame.pack(side='right', padx=10)

    tk.Label(valor_frame, text="Valor:", bg='#f5f5f5').grid(row=0, column=0, padx=10)
    valor_entry = ttk.Entry(valor_frame)
    valor_entry.grid(row=0, column=1, padx=10)

    tk.Label(valor_frame, text="Descrição:", bg='#f5f5f5').grid(row=1, column=0, padx=10)
    descricao_combobox = ttk.Combobox(valor_frame, values=opcoes_descricao, state='normal')
    descricao_combobox.grid(row=1, column=1, padx=10)

    def handle_depositar():
        try:
            valor = valor_entry.get().strip()
            valor = valor.replace('.', '').replace(',', '.')  # Remove separadores de milhar e ajusta o decimal
            valor = float(valor)
            descricao = descricao_combobox.get()
            if descricao:
                depositar_receita(valor, descricao)
                atualizar_info_labels()
            else:
                messagebox.showerror("Erro", "Por favor, selecione uma descrição.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def handle_pagar():
        try:
            valor = valor_entry.get().strip()
            valor = valor.replace('.', '').replace(',', '.')  # Remove separadores de milhar e ajusta o decimal
            valor = float(valor)
            descricao = descricao_combobox.get()
            if descricao:
                pagar(valor, descricao)
                atualizar_info_labels()
            else:
                messagebox.showerror("Erro", "Por favor, selecione uma descrição.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    ttk.Button(bottom_frame, text="Depositar Receita", command=handle_depositar).pack(side='left', padx=10)
    ttk.Button(bottom_frame, text="Pagar", command=handle_pagar).pack(side='left', padx=10)

    atualizar_info_labels()
    atualizar_treeview()

    root.mainloop()

def atualizar_info_labels():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        if not data.empty:
            receita_atual = data['receita total'].iloc[-1]
            gastos_atuais = data['gastos totais'].iloc[-1]

            receita_valor_label.config(text=formatar_valor_exibicao(receita_atual, moeda_var.get()))
            gastos_valor_label.config(text=formatar_valor_exibicao(gastos_atuais, moeda_var.get()))

def moeda_change(event):
    atualizar_info_labels()
    atualizar_treeview()

criar_interface()
