from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from housePriceDAO import housePriceDAO

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)


@app.route('/')
def index():
    return "Hello, world!"

# curl "http://127.0.0.1:5000/houses"
@app.route('/houses')
def getAllHouses():
    houses = housePriceDAO.getAllHouses()
    return jsonify(houses)

# curl "http://127.0.0.1:5000/houses/1"
@app.route('/houses/<int:id>')
def findByID(id):
    foundHouse = housePriceDAO.findByID(id)
    if len(foundHouse) == 0:
        return jsonify ({}) , 204
    return jsonify(foundHouse)

# curl -i -H "Content-Type:application/json" -X POST -d "{\"descr\":\"test_create\",\"beds\":10,\"baths\":4.5,\"area\":3,\"price\":5000}" http://127.0.0.1:5000/houses
@app.route('/houses', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    # other checking 
    house = {
        "descr": request.json['descr'],
        "beds": request.json['beds'],
        "baths": request.json['baths'],
        "area": request.json['area'],
        "price": request.json['price']
    }

    values = (house['descr'], house['beds'], house['baths'], house['area'], house['price'])
    newId = housePriceDAO.create(values)
    house['id'] = newId

    return jsonify(house)


# curl -i -H "Content-Type:application/json" -X PUT -d "{\"descr\":\"test_update\",\"beds\":100,\"baths\":9.5,\"area\":2,\"price\":1000}" http://127.0.0.1:5000/houses/8
@app.route('/houses/<int:id>', methods=['PUT'])
def update(id):
    foundHouse = housePriceDAO.findByID(id)

    if not foundHouse:
        abort(404)
    if not request.json:
        abort(400)

    reqJson = request.json

    if 'beds' in reqJson and type(reqJson['beds']) is not int:
        abort(400)

    if 'price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'descr' in reqJson:
        foundHouse['descr'] = reqJson['descr']
    if 'beds' in reqJson:
        foundHouse['beds'] = reqJson['beds']
    if 'baths' in reqJson:
        foundHouse['baths'] = reqJson['baths']
    if 'area' in reqJson:
        foundHouse['area'] = reqJson['area'] 
    if 'price' in reqJson:
        foundHouse['price'] = reqJson['price']   

    values = (foundHouse['descr'], foundHouse['beds'], foundHouse['baths'], foundHouse['area'], foundHouse['price'], foundHouse['id'])

    housePriceDAO.update(values)

    return jsonify(foundHouse)

# curl -X DELETE "http://127.0.0.1:5000/houses/8"
@app.route('/houses/<int:id>' , methods=['DELETE'])
def delete(id):
    housePriceDAO.delete(id)
    return jsonify({"done":True})


if __name__ == '__main__' :
    app.run(debug= True)