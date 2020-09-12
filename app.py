from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return f"<h1>Welcome to our Data Service! <br> {str(datetime.datetime.today())} </h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)