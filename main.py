import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

file_path = 'dados_financeiros.csv'

moedas = {
    'BRL': 'R$',
    'USD': '$',
    'EUR': '€',
}

def garantir_arquivo_csv():
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['última alteração', 'receita total', 'gastos totais'])
        df.to_csv(file_path, index=False)

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

def depositar_receita(valor):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        ultima_receita = data['receita total'].iloc[-1]
        ultimo_gasto = data['gastos totais'].iloc[-1]
    else:
        ultima_receita = 0
        ultimo_gasto = 0
    nova_receita = ultima_receita + valor
    novo_dado = pd.DataFrame({
        'última alteração': [pd.Timestamp.now()],
        'receita total': [nova_receita],
        'gastos totais': [ultimo_gasto]
    })
    novo_dado.to_csv(file_path, mode='a', header=False, index=False)
    atualizar_treeview()

def pagar(valor):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        ultima_receita = data['receita total'].iloc[-1]
        ultimo_gasto = data['gastos totais'].iloc[-1]
    else:
        ultima_receita = 0
        ultimo_gasto = 0
    novo_gasto = ultimo_gasto + valor
    nova_receita = ultima_receita - valor
    novo_dado = pd.DataFrame({
        'última alteração': [pd.Timestamp.now()],
        'receita total': [nova_receita],
        'gastos totais': [novo_gasto]
    })
    novo_dado.to_csv(file_path, mode='a', header=False, index=False)
    atualizar_treeview()

def mostrar_dados():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        print(data)

def atualizar_treeview():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        tree.delete(*tree.get_children())
        # Inverter a ordem dos dados para que a linha mais recente fique no topo
        data = data.sort_values(by='última alteração', ascending=False)
        for i, row in data.iterrows():
            tree.insert("", "end", values=list(row))
        # Adicionar cor na linha mais recente
        if tree.get_children():
            primeiro_item = tree.get_children()[0]
            tree.item(primeiro_item, tags=('recent',))
            tree.tag_configure('recent', background='#d9edf7', foreground='black')

def criar_interface():
    global tree, valor_entry, moeda_var, receita_valor_label, gastos_valor_label

    root = tk.Tk()
    root.title("Controle Financeiro")
    root.geometry("800x500")
    root.configure(bg='#f5f5f5')  # Cor de fundo do tema Breeze

    # Aplicar tema padrão "clam"
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("Treeview",
                    background="#f5f5f5",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    # Frame superior para "Receita" e "Gastos"
    top_info_frame = tk.Frame(root, bg='#f5f5f5')
    top_info_frame.pack(pady=5, fill='x')

    receita_label = tk.Label(top_info_frame, text="Receita", fg='green', bg='#f5f5f5', font=("Arial", 12, "bold"))
    receita_label.pack(side='left', padx=(10, 5))

    # Label para exibir o valor atual da receita
    receita_valor_label = tk.Label(top_info_frame, text="", fg='green', bg='#f5f5f5', font=("Arial", 12))
    receita_valor_label.pack(side='left', padx=(5, 20))

    gastos_label = tk.Label(top_info_frame, text="Gastos", fg='red', bg='#f5f5f5', font=("Arial", 12, "bold"))
    gastos_label.pack(side='left', padx=(10, 5))

    # Label para exibir o valor atual dos gastos
    gastos_valor_label = tk.Label(top_info_frame, text="", fg='red', bg='#f5f5f5', font=("Arial", 12))
    gastos_valor_label.pack(side='left', padx=(5, 10))

    # Treeview para exibir dados financeiros
    tree_frame = tk.Frame(root)
    tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=('última alteração', 'receita total', 'gastos totais'), show='headings')
    tree.heading('última alteração', text='Última Alteração')
    tree.heading('receita total', text='Receita Total')
    tree.heading('gastos totais', text='Gastos Totais')

    # Ajuste no tamanho do Treeview
    tree.column('última alteração', width=150)
    tree.column('receita total', width=150)
    tree.column('gastos totais', width=150)
    tree.pack(expand=True, fill='both')

    # Frame para a parte inferior da interface
    bottom_frame = tk.Frame(root, bg='#f5f5f5')
    bottom_frame.pack(pady=10, fill='x')

    # Campo de moeda
    tk.Label(bottom_frame, text="Moeda:", bg='#f5f5f5').pack(side='left', padx=10)
    moeda_var = tk.StringVar(value='BRL')
    moeda_combo = ttk.Combobox(bottom_frame, textvariable=moeda_var, values=list(moedas.keys()), state='readonly')
    moeda_combo.pack(side='left', padx=10)
    moeda_combo.bind('<<ComboboxSelected>>', moeda_change)  # Atualizar ao selecionar moeda

    # Campo de valor e botões
    valor_frame = tk.Frame(bottom_frame, bg='#f5f5f5')
    valor_frame.pack(side='right', padx=10)

    tk.Label(valor_frame, text="Valor:", bg='#f5f5f5').grid(row=0, column=0, padx=10)
    valor_entry = ttk.Entry(valor_frame)
    valor_entry.grid(row=0, column=1, padx=10)

    def handle_depositar():
        try:
            valor = float(valor_entry.get())
            depositar_receita(valor)
            atualizar_info_labels()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def handle_pagar():
        try:
            valor = float(valor_entry.get())
            pagar(valor)
            atualizar_info_labels()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def handle_mostrar_dados():
        mostrar_dados()
        atualizar_treeview()
        atualizar_info_labels()

    # Botões centralizados
    buttons_frame = tk.Frame(bottom_frame, bg='#f5f5f5')
    buttons_frame.pack(side='bottom', pady=5)

    ttk.Button(buttons_frame, text="Depositar Receita", command=handle_depositar).grid(row=0, column=0, padx=10, pady=5)
    ttk.Button(buttons_frame, text="Pagar", command=handle_pagar).grid(row=0, column=1, padx=10, pady=5)
    ttk.Button(buttons_frame, text="Mostrar Dados", command=handle_mostrar_dados).grid(row=0, column=2, padx=10, pady=5)

    # Atualizar a árvore e labels ao iniciar
    atualizar_treeview()
    atualizar_info_labels()

    root.mainloop()

def atualizar_info_labels():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        if not data.empty:
            receita_atual = data['receita total'].iloc[-1]
            gastos_atuais = data['gastos totais'].iloc[-1]
            receita_valor_label.config(text=f"{moedas[moeda_var.get()]} {receita_atual:.2f}")
            gastos_valor_label.config(text=f"{moedas[moeda_var.get()]} {gastos_atuais:.2f}")

def moeda_change(event):
    atualizar_info_labels()

if __name__ == "__main__":
    criar_interface()
