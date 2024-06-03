from flask import Blueprint, request
from shared.data import update_data

bp = Blueprint('main', __name__)

@bp.route('/receive_from_2kki', methods=['POST'])
def receive_data():
    data = request.json
    location = data['data']['location']
    update_data(location)
    return {"status": "success"}

@bp.route('/status', methods=['GET'])
def status_check():
    return "Server is running", 200