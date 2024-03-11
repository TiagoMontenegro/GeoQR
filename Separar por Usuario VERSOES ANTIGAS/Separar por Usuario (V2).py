import csv
import os
from tkinter import Tk, filedialog

def escolher_arquivo():
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    arquivo_origem = filedialog.askopenfilename(title="Escolha o arquivo de origem", filetypes=[("Arquivos CSV", "*.csv")])
    return arquivo_origem

# def escolher_diretorio():
#     root = Tk()
#     root.withdraw()  # Oculta a janela principal
#     diretorio_destino = filedialog.askdirectory(title="Escolha o diretório de destino")
#     return diretorio_destino


def limpar_nome(nome):
    caracteres_invalidos = r'\/:*?"<>|'
    for char in caracteres_invalidos:
        nome = nome.replace(char, '')
    return nome

#def criar_secao(arquivo_origem, diretorio_destino):
def criar_secao(arquivo_origem):
    diretorio_origem = os.path.dirname(arquivo_origem)

    with open(arquivo_origem, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    secao_atual = []
    secoes = []

    for i, linha in enumerate(linhas):
        if "INICIO" in linha:
            secao_atual = [linha]
            # Obtém a segunda parte da linha seguinte à linha de "INICIO"
            nome_secao = limpar_nome(linhas[i+1].split(",", 1)[1].split(",", 1)[0].strip().strip('"'))
        elif "FIM" in linha:
            secao_atual.append(linha)
            secoes.append((nome_secao, secao_atual))
            secao_atual = []
        elif secao_atual:
            secao_atual.append(linha)

    for nome_secao, secao in secoes:
        #nome_arquivo = f"{diretorio_destino}/{nome_secao}.csv"
        nome_arquivo = f"{diretorio_origem}/{nome_secao}.csv"
        with open(nome_arquivo, 'w', encoding='utf-8', newline='') as arquivo_secao:
            arquivo_secao.writelines(secao)

# if __name__ == "__main__":
#     arquivo_origem = escolher_arquivo()
#     if not arquivo_origem:
#         print("Nenhum arquivo selecionado. Encerrando.")
#     else:
#         diretorio_destino = escolher_diretorio()
#         if not diretorio_destino:
#             print("Nenhum diretório selecionado. Encerrando.")
#         else:
#             criar_secao(arquivo_origem, diretorio_destino)
#             print("Seções criadas com sucesso!")

if __name__ == "__main__":
    arquivo_origem = escolher_arquivo()
    if not arquivo_origem:
        print("Nenhum arquivo selecionado. Encerrando.")
    else:
        criar_secao(arquivo_origem)
        print("Seções criadas com sucesso!")


# O que esta comentado é removendo a opçao de selecionar aonde será salvo os arquivos,
# e assim salvando no local de origem do .CSV para evitar
# muitas janelas de clicar.