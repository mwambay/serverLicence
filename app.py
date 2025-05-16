from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # très important pour permettre à l'app Android d'accéder

# Variable de contrôle globale
APP_ACTIVE = True

@app.route('/app-status', methods=['GET'])
def app_status():
    """
    Endpoint pour que l'app mobile vérifie si elle doit continuer ou se bloquer
    """
    if APP_ACTIVE:
        return jsonify({
            'status': 'active',
            'message': 'L\'application peut continuer à fonctionner.'
        }), 200
    else:
        return jsonify({
            'status': 'blocked',
            'message': 'L\'application est désactivée. Veuillez contacter l\'administrateur.'
        }), 403

@app.route('/set-status', methods=['POST'])
def set_status():
    """
    Endpoint pour changer l’état de l’app via une requête POST
    Exemple de body JSON : { "active": false }
    """
    global APP_ACTIVE
    data = request.get_json()

    if not data or 'active' not in data:
        return jsonify({'error': 'Champ "active" manquant (true ou false).'}), 400

    if not isinstance(data['active'], bool):
        return jsonify({'error': '"active" doit être un booléen (true ou false).'}), 400

    APP_ACTIVE = data['active']

    return jsonify({
        'success': True,
        'status': 'active' if APP_ACTIVE else 'blocked',
        'message': f"L'état de l'application a été mis à jour à {'actif' if APP_ACTIVE else 'bloqué'}."
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
