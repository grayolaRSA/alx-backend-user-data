#!/usr/bin/env python3
"""basic Flask app"""


from flask import Flask, jsonify
from typing import Dict


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world() -> Dict:
    """flask function for home route"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
