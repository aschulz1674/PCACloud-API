from flask import Flask, request, jsonify
from replit import db
from flask_cors import CORS

app = Flask('app')
CORS(app)


@app.route('/')
def hello_world():
    return str(db.keys())


def normalize(s):
    'Remove redundant whitespace'
    s = s.strip()
    t = ''
    while s != t:
        t = s
        s = s.replace(' ', '').replace('\t', '').replace('r','').replace('\n', '').replace('-','').replace('~','').replace(',','').replace('.','').replace('/','').replace('`','')
    return s
  
_badlist = []

def badlist():
    if not _badlist:
        with open('badwords.txt', 'r') as f:
            while True:
                line = f.readline().strip()
                if not line: break
                _badlist.append(line)
    return _badlist

_goodlist = []
def goodlist():
    if not _goodlist:
        with open('goodwords.txt', 'r') as f:
            while True:
                line = f.readline().strip()
                if not line: break
                _goodlist.append(line)
    return _goodlist

def isBad(phrase):
  'Return true only if the phrase contains bad words'
  phrase = normalize(phrase).lower()
  for bad in badlist():
    if bad in phrase :
      for good in goodlist():
        if good in phrase:
          phrase.replace(good,'')
          if bad in phrase:
            return True
          return False
      return True
  return False



@app.route('/api/word/<id>', methods=["GET"])
def get_word(id):
    data = {}
    if id in db:
        data = db[id]
        return jsonify(isError=False,
                       message="Success",
                       statusCode=120,
                       data=data), 200
    else:
        return jsonify(isError=True,
                       message="Not Found",
                       statusCode=404,
                       data=data), 404


@app.route('/api/word/', methods=["GET"])
def get_words():
    data = sorted(db.items(), key=lambda x: x[1], reverse=True)
    data = [{"text": x[0], "weight": x[1], "tooltip": x[1]} for x in data]
    return jsonify(isError=False,
                   message="Success",
                   statusCode=120,
                   words=data), 201


@app.route('/api/word/<id>', methods=["POST"])
def post_word(id):
  if id in db:
    count = db[id]
  else:
    count = 0
  count += 1
  if isBad(id):
    data = {"bad"}
    return jsonify(isError=True, message="Invalid word", statusCode=406, data=data), 406
  db[id] = count
  data = {"count": count}
  return jsonify(isError=False, message="Success", statusCode=200, data=data), 200

404




@app.route('/api/word/clear/<id>', methods=["POST"])
def clearWord(id):
    del db[id]
    data = "Deleted:", id
    return jsonify(isError=False, message="Success", statusCode=120,data=data), 200


@app.route('/api/word/add/<id>/<id1>', methods=["POST"])
def setWord(id, id1):

    db[id] = int(id1)
    data = "Word:", id,"Count:",id1
    return jsonify(isError=False, message="Success", statusCode=120,data=data), 200


@app.route('/api/word/2132Clear', methods=["GET"])
def clear():
    db.clear()
    return jsonify(isError=False, message="Success", statusCode=120,
                   data="Cleared"), 200


app.run(host='0.0.0.0', port=8080)
