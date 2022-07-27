from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.y2pfd99.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    print(bucket_receive)
    count = len(list(db.bucket_List.find({},{'_id':False}))) + 1
    print(count)

    doc = {
        'index_Num': count,
        'bucket': bucket_receive,
        'done' : 0
    }

    db.bucket_List.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    index_give = request.form['index_give']

    print(index_give)
    print(db.bucket_List.find_one({'index_Num': int(index_give)}))

    db.bucket_List.update_one({'index_Num': int(index_give)}, {'$set': {'done': 1}})

    return jsonify({'msg': '달성!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    index_give = request.form['index_give']

    print(index_give)
    print(db.bucket_List.find_one({'index_Num': int(index_give)}))

    db.bucket_List.update_one({'index_Num': int(index_give)}, {'$set': {'done': 0}})

    return jsonify({'msg': '취소'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_lists = list(db.bucket_List.find({}, {'_id': False}))

    return jsonify({'bucket_receive' : all_lists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)