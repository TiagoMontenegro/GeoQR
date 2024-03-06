from flask import Flask, request, render_template
import os
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arquivo_origem = request.files['arquivo']
        if arquivo_origem and arquivo_origem.filename.endswith('.csv'):
            caminho_arquivo = os.path.join('uploads', arquivo_origem.filename)
            arquivo_origem.save(caminho_arquivo)
            criar_secao(caminho_arquivo)
            return 'Seções criadas com sucesso!'
        else:
            return 'Erro: Envie um arquivo CSV válido.'
    return render_template('index.html')  # Crie um arquivo HTML para o formulário de upload

def limpar_nome(nome):
    caracteres_invalidos = r'\/:*?"<>|'
    for char in caracteres_invalidos:
        nome = nome.replace(char, '')
    return nome

def obter_nome_unico(nome_arquivo):
    if not os.path.exists(nome_arquivo):    
        return nome_arquivo

    base, ext = os.path.splitext(nome_arquivo)
    contador = 1
    while os.path.exists(f"{base} ({contador}){ext}"):
        contador += 1

    return f"{base} ({contador}){ext}"

def criar_secao(arquivo_origem):
    try:
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
            nome_arquivo = obter_nome_unico(f"{diretorio_origem}/{nome_secao}.csv")
            with open(nome_arquivo, 'w', encoding='utf-8', newline='') as arquivo_secao:
                arquivo_secao.writelines(secao)
    except Exception as e:
        print(f"Erro ao criar seção: {e}")
        raise  # Propaga a exceção para identificar o problema nos logs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
