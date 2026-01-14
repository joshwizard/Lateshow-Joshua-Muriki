from flask import request, jsonify
from config import app, db
from models import Episode, Guest, Appearance

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict(only=('id', 'date', 'number')) for e in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict(only=('id', 'date', 'number', 'appearances.id', 'appearances.rating', 'appearances.guest_id', 'appearances.episode_id', 'appearances.guest.id', 'appearances.guest.name', 'appearances.guest.occupation')))

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict(only=('id', 'name', 'occupation')) for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        appearance = Appearance(
            rating=data.get('rating'),
            episode_id=data.get('episode_id'),
            guest_id=data.get('guest_id')
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict(only=('id', 'rating', 'guest_id', 'episode_id', 'episode.id', 'episode.date', 'episode.number', 'guest.id', 'guest.name', 'guest.occupation'))), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True)
