from flask import Flask, jsonify, request
from datetime import datetime

from utils.validation import validate_data
from data.expenses import expenses_data
app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)