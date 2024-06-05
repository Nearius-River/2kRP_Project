from flask import Blueprint, request
from shared.data import update_data

bp = Blueprint('main', __name__)

@bp.route('/receive_from_2kki', methods=['POST'])
def receive_data():
    data = request.json
    location = data['location']
    badgeImageUrl = data['badgeImageUrl']
    playersOnline = data['playersOnline']
    playersOnMap = data['playersOnMap']
    update_data(location, badgeImageUrl, playersOnline, playersOnMap)
    return {"status": "success"}

@bp.route('/status', methods=['GET'])
def status_check():
    return "Server is running", 200