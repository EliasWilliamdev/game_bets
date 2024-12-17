from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Dados do jogo
numeros_validos = list(range(1, 100))
apostas = []
ultimo_numero_sorteado = None

@app.route("/")
def index():
    return render_template("index.html", apostas=apostas, numero_sorteado=ultimo_numero_sorteado)

@app.route("/fazer_aposta", methods=["POST"])
def fazer_aposta():
    nome = request.form["nome"]
    numero = int(request.form["numero"])
    valor = float(request.form["valor"])

    if numero not in numeros_validos:
        return "Número inválido. Escolha entre 1 e 99.", 400
    if valor <= 0:
        return "O valor da aposta deve ser maior que zero.", 400

    apostas.append({"nome": nome, "numero": numero, "valor": valor})
    return redirect(url_for("index"))

@app.route("/sortear", methods=["POST"])
def sortear():
    global ultimo_numero_sorteado
    if not apostas:
        return "Nenhuma aposta registrada. Não é possível realizar o sorteio.", 400

    ultimo_numero_sorteado = random.choice(numeros_validos)
    return redirect(url_for("resultado"))

@app.route("/resultado")
def resultado():
    if ultimo_numero_sorteado is None:
        return redirect(url_for("index"))

    ganhadores = [
        aposta for aposta in apostas if aposta["numero"] == ultimo_numero_sorteado
    ]
    return render_template(
        "resultado.html",
        numero_sorteado=ultimo_numero_sorteado,
        ganhadores=ganhadores,
        apostas=apostas,
    )

@app.route("/limpar", methods=["POST"])
def limpar():
    global apostas, ultimo_numero_sorteado
    apostas.clear()
    ultimo_numero_sorteado = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
