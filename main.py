import pandas as pd
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

file_path = 'dados_financeiros.csv'
log_path = 'log.txt'

def log_message(message):
    with open(log_path, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {message}\n")

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

def criar_arquivo_csv():
    colunas = ['última alteração', 'receita total', 'gastos totais']
    df = pd.DataFrame(columns=colunas)
    df.to_csv(file_path, index=False)
    log_message(f"Arquivo '{file_path}' criado com as colunas {colunas}.")
    print(f"Arquivo '{file_path}' criado com as colunas {colunas}.")

def garantir_arquivo_csv():
    if not os.path.exists(file_path):
        criar_arquivo_csv()

def depositar_receita(valor):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        try:
            data = pd.read_csv(file_path)
            if data.empty:
                data = pd.DataFrame({
                    'última alteração': [datetime.now().strftime('%d/%m/%y %H:%M')],
                    'receita total': [valor],
                    'gastos totais': [0]
                })
            else:
                receita_total_atual = data['receita total'].iloc[-1]
                nova_receita_total = receita_total_atual + valor
                data = pd.DataFrame({
                    'última alteração': [datetime.now().strftime('%d/%m/%y %H:%M')],
                    'receita total': [nova_receita_total],
                    'gastos totais': [data['gastos totais'].iloc[-1]]
                }, index=[0])
            data.to_csv(file_path, index=False)
            atualizar_treeview()
            log_message(f"Receita de {valor} adicionada. Receita total atualizada com sucesso!")
            messagebox.showinfo("Sucesso", f"Receita de {valor} adicionada. Receita total atualizada com sucesso!")
        except pd.errors.EmptyDataError:
            log_message("Erro: O arquivo CSV está vazio ou não contém dados válidos.")
            messagebox.showerror("Erro", "O arquivo CSV está vazio ou não contém dados válidos.")
        except Exception as e:
            log_message(f"Erro ao ler o arquivo CSV: {e}")
            messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
    else:
        messagebox.showwarning("Aviso", "O arquivo CSV está vazio.")

def pagar(valor):
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        try:
            data = pd.read_csv(file_path)
            if data.empty:
                log_message("Erro: O arquivo CSV está vazio ou não contém dados válidos.")
                messagebox.showerror("Erro", "O arquivo CSV está vazio ou não contém dados válidos.")
                return
            receita_total_atual = data['receita total'].iloc[-1]
            gastos_totais_atual = data['gastos totais'].iloc[-1]
            if valor > receita_total_atual:
                log_message("Erro: Valor de pagamento maior do que a receita total disponível.")
                messagebox.showerror("Erro", "Valor de pagamento maior do que a receita total disponível.")
                return
            nova_receita_total = receita_total_atual - valor
            novos_gastos_totais = gastos_totais_atual + valor
            data = pd.DataFrame({
                'última alteração': [datetime.now().strftime('%d/%m/%y %H:%M')],
                'receita total': [nova_receita_total],
                'gastos totais': [novos_gastos_totais]
            }, index=[0])
            data.to_csv(file_path, index=False)
            atualizar_treeview()
            log_message(f"Gasto de {valor} registrado. Receita total e gastos totais atualizados com sucesso!")
            messagebox.showinfo("Sucesso", f"Gasto de {valor} registrado. Receita total e gastos totais atualizados com sucesso!")
        except pd.errors.EmptyDataError:
            log_message("Erro: O arquivo CSV está vazio ou não contém dados válidos.")
            messagebox.showerror("Erro", "O arquivo CSV está vazio ou não contém dados válidos.")
        except Exception as e:
            log_message(f"Erro ao ler o arquivo CSV: {e}")
            messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
    else:
        messagebox.showwarning("Aviso", "O arquivo CSV está vazio.")

def mostrar_dados():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        try:
            data = pd.read_csv(file_path)
            if data.empty:
                log_message("Erro: O arquivo CSV está vazio ou não contém dados válidos.")
                messagebox.showerror("Erro", "O arquivo CSV está vazio ou não contém dados válidos.")
                return
            ultima_alteracao = data['última alteração'].iloc[-1]
            receita_total = data['receita total'].iloc[-1]
            gastos_totais = data['gastos totais'].iloc[-1]
            log_message(f"Dados exibidos - Última alteração: {ultima_alteracao}, Receita total: {receita_total}, Gastos totais: {gastos_totais}")
            messagebox.showinfo("Dados Financeiros",
                                f"Última alteração: {ultima_alteracao}\n"
                                f"Receita total atual: {receita_total}\n"
                                f"Gastos totais: {gastos_totais}")
        except pd.errors.EmptyDataError:
            log_message("Erro: O arquivo CSV está vazio ou não contém dados válidos.")
            messagebox.showerror("Erro", "O arquivo CSV está vazio ou não contém dados válidos.")
        except Exception as e:
            log_message(f"Erro ao ler o arquivo CSV: {e}")
            messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
    else:
        messagebox.showwarning("Aviso", "O arquivo CSV está vazio.")

def atualizar_treeview():
    garantir_arquivo_csv()
    if not is_file_empty(file_path):
        data = pd.read_csv(file_path)
        if data.empty:
            return

        # Limpar o Treeview antes de atualizar
        for item in tree.get_children():
            tree.delete(item)

        for index, row in data.iterrows():
            tree.insert('', 'end', values=(row['última alteração'], row['receita total'], row['gastos totais']))

def criar_interface():
    global tree, valor_entry

    root = tk.Tk()
    root.title("Controle Financeiro")

    # Treeview para exibir dados financeiros
    tree = ttk.Treeview(root, columns=('última alteração', 'receita total', 'gastos totais'), show='headings')
    tree.heading('última alteração', text='Última Alteração')
    tree.heading('receita total', text='Receita Total')
    tree.heading('gastos totais', text='Gastos Totais')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Frame para botões
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Label(button_frame, text="Valor:").grid(row=0, column=0, padx=10)
    valor_entry = tk.Entry(button_frame)
    valor_entry.grid(row=0, column=1, padx=10)

    def handle_depositar():
        try:
            valor = float(valor_entry.get())
            depositar_receita(valor)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def handle_pagar():
        try:
            valor = float(valor_entry.get())
            pagar(valor)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def handle_mostrar_dados():
        mostrar_dados()
        atualizar_treeview()

    tk.Button(button_frame, text="Depositar Receita", command=handle_depositar).grid(row=1, column=0, padx=10, pady=5)
    tk.Button(button_frame, text="Pagar", command=handle_pagar).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(button_frame, text="Mostrar Dados", command=handle_mostrar_dados).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Atualizar a árvore ao iniciar
    atualizar_treeview()

    root.mainloop()

criar_interface()
