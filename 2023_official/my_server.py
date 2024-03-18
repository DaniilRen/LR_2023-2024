from flask import Flask
from flask import jsonify

coords = ((1, 2), (4, 2), (9, 3))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def return_coords():
	return jsonify({i: [*coords[i]] for i in range(len(coords))})

app.run('0.0.0.0', port=4001, debug=True)