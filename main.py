from flask import Flask, request, jsonify
from app import Webscraping
app = Flask(__name__)


@app.route('/ConsultaInfos', methods=['POST'])
def main():
    chave = request.json['chave']
    ws = Webscraping(chave)
    data = ws.get_data()

    return jsonify(data)





app.run(debug=True)


