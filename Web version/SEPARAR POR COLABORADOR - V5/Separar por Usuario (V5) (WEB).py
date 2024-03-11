from flask import (
    Flask,
    request,
    render_template,
    redirect,
    flash,
    send_file,
    send_from_directory,
)
import os
import csv
import zipfile

app = Flask(__name__)
app.secret_key = "empat@2019"

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Função para criar o diretório "uploads" se não existir
def criar_diretorio_uploads():
    diretorio_uploads = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "uploads"
    )
    if not os.path.exists(diretorio_uploads):
        os.makedirs(diretorio_uploads)


# Função para limpar caracteres inválidos do nome do arquivo
def limpar_nome(nome):
    caracteres_invalidos = r'\/:*?"<>|'
    for char in caracteres_invalidos:
        nome = nome.replace(char, "")
    return nome


# Função para obter um nome de arquivo único
def obter_nome_unico(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return nome_arquivo

    base, ext = os.path.splitext(nome_arquivo)
    contador = 1
    while os.path.exists(f"{base} ({contador}){ext}"):
        contador += 1

    return f"{base} ({contador}){ext}"


# Função para criar seções
def criar_secao(arquivo_origem):
    try:
        diretorio_origem = os.path.dirname(arquivo_origem)

        with open(arquivo_origem, "r", encoding="utf-8") as file:
            linhas = file.readlines()

        secao_atual = []
        secoes = []

        for i, linha in enumerate(linhas):
            if "INICIO" in linha:
                secao_atual = [linha]
                # Obtém a segunda parte da linha seguinte à linha de "INICIO"
                nome_secao = limpar_nome(
                    linhas[i + 1].split(",", 1)[1].split(",", 1)[0].strip().strip('"')
                )
            elif "FIM" in linha:
                secao_atual.append(linha)
                secoes.append((nome_secao, secao_atual))
                secao_atual = []
            elif secao_atual:
                secao_atual.append(linha)

        for nome_secao, secao in secoes:
            nome_arquivo = obter_nome_unico(f"{diretorio_origem}/{nome_secao}.csv")
            with open(nome_arquivo, "w", encoding="utf-8", newline="") as arquivo_secao:
                arquivo_secao.writelines(secao)
    except Exception as e:
        print(f"Erro ao criar seção: {e}")
        raise


# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        arquivo_origem = request.files["arquivo"]
        if arquivo_origem and arquivo_origem.filename.endswith(".csv"):
            criar_diretorio_uploads()  # Verifica e cria o diretório "uploads" se necessário
            caminho_arquivo = os.path.join("uploads", arquivo_origem.filename)
            arquivo_origem.save(caminho_arquivo)
            criar_secao(caminho_arquivo)

            flash(
                "Arquivos divididos criados com sucesso! Clique em Download para baixá-los."
            )

            return redirect("/")
        else:
            flash("Erro: Envie um arquivo CSV válido.")
            return redirect("/")
    return render_template("index.html")


# Rota para download
@app.route("/download")
def download():
    try:
        # Caminho absoluto para o arquivo ZIP
        zip_path = os.path.abspath(os.path.join("uploads", "arquivos_divididos.zip"))

        # Compactar os arquivos divididos em um arquivo ZIP
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for arquivo in os.listdir("uploads"):
                if arquivo.endswith(".csv"):
                    zipf.write(
                        os.path.join("uploads", arquivo), os.path.basename(arquivo)
                    )

        # Enviar o arquivo ZIP como resposta
        response = send_file(zip_path, as_attachment=True)

        # Excluir os arquivos divididos após o download
        for arquivo in os.listdir("uploads"):
            if arquivo.endswith(".csv"):
                os.remove(os.path.join("uploads", arquivo))

        return response
    except Exception as e:
        print(f"Erro ao criar arquivo ZIP: {e}")
        return "Erro ao gerar o download", 500


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


# Iniciar o aplicativo Flask
if __name__ == "__main__":
    # app.run(host="172.17.0.135", port=9080)
    app.run(host="0.0.0.0", port=3000)
