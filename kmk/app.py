from flask import Flask, request
from flask_cors import CORS
from keras_name_generator import *

app = Flask(__name__)
CORS(app) # needed for cross-domain requests, allow everything by default
random_name = generate_word(model, temperature = 1.0, min_word_length = 4)

# 디폴트 route 
@app.route('/')
def index():
    return "Index API"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

# API route
@app.route('/random', methods=['GET'])
def random():
    output_data = generate_word(model, temperature = 1.0, min_word_length = 4)
    response = output_data
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)