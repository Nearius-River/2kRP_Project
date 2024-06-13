from flask import Blueprint, request, jsonify
from shared.data import update_data

bp = Blueprint('main', __name__)

@bp.route('/receive_from_2kki', methods=['POST'])
def receive_data():
    """
    Receive data from linker extension and update the data store appropriately.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        gameType = data.get('gameType')
        location = data.get('location')
        badge_image_url = data.get('badgeImageUrl')
        players_online = data.get('playersOnline')
        players_on_map = data.get('playersOnMap')
        wiki_page_url = data.get('wikiPageUrl')

        update_data(gameType, location, badge_image_url, players_online, players_on_map, wiki_page_url)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/status', methods=['GET'])
def status_check():
    """
    Verify server status.
    """
    return "Server is running", 200