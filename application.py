from flask import Flask, jsonify, request, abort, session, url_for, redirect, render_template
from flask_cors import CORS
from housePriceDAO import housePriceDAO


app = Flask(__name__, static_url_path='', static_folder='.')
app.secret_key = 'myS3cr3tK3y'

CORS(app)

@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))

    return redirect(url_for('houseViewer'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        print("USERNAME: ", uname)

        upass = request.form['upass']
        print("USERPASS: ", upass)
        userCheck = housePriceDAO.checkLogin(uname, upass)
        print("TEST:",userCheck)

        if not userCheck:
            print("NOT USERCHECK")
            return render_template('login.html')

        else:
            print("YES USERCHECK")
            session['username']=uname
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/houseviewer', methods=['GET','POST'])
def houseViewer():
    return render_template('houseviewer.html')

@app.route('/mapviewer', methods=['GET','POST'])
def mapViewer():
    return render_template('mapviewer.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return render_template('login.html')


@app.route('/clear')
def clear():
    session.pop('counter', None)

    return "done"

# curl "http://127.0.0.1:5000/areas"
@app.route('/areas')
def getAllAreas():
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
    areas = housePriceDAO.getAllAreas()
    return jsonify(areas)

# curl "http://127.0.0.1:5000/houses"
@app.route('/houses')
def getAllHouses():
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
    houses = housePriceDAO.getAllHouses()
    return jsonify(houses)

# curl "http://127.0.0.1:5000/houses/1"
@app.route('/houses/<int:id>')
def findByID(id):
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
    foundHouse = housePriceDAO.findByID(id)
    if len(foundHouse) == 0:
        return jsonify ({}) , 204
    return jsonify(foundHouse)

# curl -i -H "Content-Type:application/json" -X POST -d "{\"descr\":\"test_create\",\"beds\":10,\"baths\":4.5,\"area\":3,\"price\":5000}" http://127.0.0.1:5000/houses
@app.route('/houses', methods=['POST'])
def create():
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
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
    for value in values:
        print("Value: ",value)
    newId = housePriceDAO.create(values)
    print("NewId: ", newId)
    house['id'] = newId

    return jsonify(house)


# curl -i -H "Content-Type:application/json" -X PUT -d "{\"descr\":\"test_update\",\"beds\":100,\"baths\":9.5,\"area\":2,\"price\":1000}" http://127.0.0.1:5000/houses/8
@app.route('/houses/<int:id>', methods=['PUT'])
def update(id):
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
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
    if not 'username' in session:
        abort(401)
        return redirect(url_for('login'))
    housePriceDAO.delete(id)
    return jsonify({"done":True})


if __name__ == '__main__' :
    app.run(debug= True)