from models.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS

# Start app
app = Flask(__name__)
CORS(app)

# Custom endpoint
endpoint = '/api/v1'


# ROUTES
@app.route('/')
def index():
    return "PLEASE VISIT API ROUTE"


@app.route(endpoint+'/')
def api():
    return "Welcome to API"


@app.route(endpoint+'/bestemmingen', methods=["GET"])
def get_bestemmingen():

    data = DataRepository.read_bestemmingen()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify("error"), 404


@app.route(endpoint+'/treinen/bestemming/<bestemming_id>', methods=["GET"])
def get_bestemming(bestemming_id):
    data = DataRepository.read_treinen_met_bestemming(bestemming_id)

    if data is not None:
        return jsonify(treinen=data), 200
    else:
        return jsonify(error="failed"), 404


@app.route(endpoint+'/treinen', methods=["GET", "POST"])
def get_treinen():
    if request.method == "GET":
        data = DataRepository.read_treinen()
        if data is not None:
            return jsonify(treinen=data), 200
        else:
            return jsonify("error"), 404

    elif request.method == "POST":
        gegevens = DataRepository.json_or_formdata(request)
        if gegevens["vertraging"] is None:
            gegevens["vertraging"] = 0

        data = DataRepository.create_trein(
            gegevens["vertrek"],
            gegevens["bestemmingID"],
            gegevens["spoor"],
            gegevens["vertraging"],
            gegevens["afgeschaft"]
        )

        if data is not None:
            # 201 Bij POST
            return jsonify(trein_id=data), 201
        else:
            return jsonify("error"), 404


@app.route(endpoint+'/treinen/<trein_id>', methods=["GET", "PUT", "DELETE"])
def get_trein(trein_id):
    if request.method == "GET":
        data = DataRepository.read_trein(trein_id)
        if data is not None:
            return jsonify(trein=data), 200
        else:
            return jsonify("error"), 404

    elif request.method == "PUT":
        gegevens = DataRepository.json_or_formdata(request)
        data = DataRepository.update_trein(
            trein_id,
            gegevens["vertrek"],
            gegevens["bestemmingID"],
            gegevens["spoor"],
            gegevens["vertraging"],
            gegevens["afgeschaft"]
        )

        if data is not None:
            if data > 0:
                return jsonify(treinID=trein_id), 200
            else:
                return jsonify(message="Geen aanpassingen doorgevoerd"), 303
        else:
            return jsonify(message="Error"), 404

    elif request.method == "DELETE":
        data = DataRepository.delete_trein(trein_id)
        if data is not None:
            return jsonify(gelukt=data), 200
        else:
            return jsonify("error"), 404


# Start app
if __name__ == '__main__':
    app.run(debug=True)
