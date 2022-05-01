from flask import Flask, request, jsonify
from replit import db
from flask_cors import CORS

app = Flask('app')
CORS(app)

@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'
@app.route('/api/word/<id>', methods=["GET"])
def get_word(id):
  data = {}
  if id in db:
    data = db[id]
    return jsonify(isError=False, message="Success",statusCode=120,data=data),200
  else:
    return jsonify(isError=True, message="Not Found",statusCode=404,data=data),404 
    
@app.route('/api/word/', methods=["GET"])
def get_words():
  data = sorted(db.items(), key=lambda x:x[1], reverse=True)
  data = [{"word":x[0], "count":x[1]} for x in data]
  return jsonify(isError=False, message="Success",statusCode=120,words=data),201

    
@app.route('/api/word/<id>', methods=["POST"])
def post_word(id):
  if id in db:
    rec = db[id]
    rec = rec + 1
    db[id] = rec
  else:
    rec = 1
    db[id] = rec
  return jsonify(isError=False, message="Success",statusCode=120,data=rec),200



@app.route('/api/word/2132Clear', methods=["GET"])
def clear():
  db.clear()
  return jsonify(isError=False, message="Success",statusCode=120,data=""),200


app.run(host='0.0.0.0', port=8080)