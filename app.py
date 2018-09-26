from flask import Flask, jsonify, request, Response
from test import validBookObject
import json

app = Flask(__name__)
print(__name__) #it will print __main__
print(app)

#java contains method similar
#if "blah" not in somestring:
#https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method?rq=1
books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 938394839
    },
    {
        'name': 'The cat in The Hat',
        'price': 6.99,
        'isbn': 938394835
    }
]

#GET METHODS
#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books':books})

#searching by ISBN
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    print(type(isbn))
    for book in books:
        if book["isbn"] == isbn:
            return_value= {
                'name':book["name"],
                'price':book["price"]
            }
    return jsonify(return_value)
    #pass placeholder

#POST METHODS
@app.route('/books', methods=['POST'])
def add_book():
    #request_data = json from request
    request_data = request.get_json()
    #checking if request_data that we post, the json object is valid
    if(validBookObject(request_data)):
        #create a new json type object with name,price and isbn
        new_book = {
            "name": request_data['name'],
            "price": request_data["price"],
            "isbn": request_data['isbn']
        }
        #and insert it to index 0
        books.insert(0, new_book)
        #if insert is succesfull and is a validobject then return true, else return false
        #code 201 is for POST type
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBook = {
            "error": "Invalid obj",
            "helpString": "Data passed wrong"
        }
        response = Response(json.dumps(invalidBook), 400, mimetype='application/json');
        return response




# PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i=0;
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i+=1
    response = Response("", status=204)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if ("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

app.run(port=5000)
