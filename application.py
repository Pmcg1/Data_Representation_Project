from flask import Flask, jsonify, request, abort, session, url_for, redirect
from flask_cors import CORS
from housePriceDAO import housePriceDAO

app = Flask(__name__, static_url_path='', static_folder='.')
app.secret_key = 'myS3cr3tK3y'

CORS(app)

@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))

    return 'welcome ' + session['username'] +\
        '<br><a href="'+url_for('logout')+'">logout</a>'

@app.route('/login')
def login():
    return '<h1> login</h1> '+\
        '<button>' +\
            '<a href="'+url_for('process_login')+'">' +\
                'login' +\
            '</a>' +\
        '</button>'

@app.route('/processLogin')
def process_login():
    session['username']="Guest User"
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

'''
@app.route('/')
def index():
    count=0
    count+=1

    if not 'counter' in session:
        session['counter'] = 0
        print["new session"]

    sessionCount=session['counter']
    sessionCount+=1
    session['counter']=sessionCount

    pageContent = "<h1>counts</h1>" +\
        "session Count ="+str(sessionCount) +\
        "<br/>this Count ="+str(count)

    return pageContent
'''

@app.route('/clear')
def clear():
    session.pop('counter', None)

    return "done"

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
    newId = housePriceDAO.create(values)
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