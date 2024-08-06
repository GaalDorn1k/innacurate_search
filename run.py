import os

from config_manager import get_config
from client import Client
from flask import Flask, Response, request, jsonify


app = Flask(__name__)


@app.route('/api/search', methods=['GET'])
def search() -> Response:
    query = request.args.get('query')
    response = service.search(query)
    return jsonify(response)


@app.route('/api/open', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f_path = os.path.join('temp', f.filename)
        f.save(f_path)
        service.open_doc(f_path)
        os.remove(f_path)
        return 'file uploaded successfully'


if __name__ == '__main__':
    config = get_config()
    service = Client(config.embedder, config.search_treshold)
    app.run(port=config.port)
