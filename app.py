from datetime import datetime
from flask import Flask, request, jsonify
from models import Advertisement, db
from config import Config


app = Flask('advertisement')
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def add_to_dict(ad):
    return {
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner': ad.owner,
    }

@app.route('/api/', methods=['GET'])
def get_advertisements():
    ads = Advertisement.query.all()
    return jsonify([add_to_dict(ad) for ad in ads])

@app.route('/api/<int:id>', methods=['GET'])
def get_advertisement(id):
    ad = Advertisement.query.get_or_404(id)
    return jsonify(add_to_dict(ad))

@app.route('/api/', methods=['POST'])
def create_advertisement():
    data = request.get_json()

    new_ad = Advertisement(
        title=data['title'],
        description=data['description'],
        created_at=datetime.now(),
        owner=data['owner'],
    )

    db.session.add(new_ad)
    db.session.commit()

    return jsonify(add_to_dict(new_ad))

@app.route('/api/<int:id>', methods=['PUT'])
def update_advertisement(id):
    ad = Advertisement.query.get_or_404(id)
    data = request.get_json()

    ad.title = data['title']
    ad.description = data['description']
    ad.owner = data['owner']

    db.session.commit()
    return jsonify(add_to_dict(ad))

@app.route('/api/<int:id>', methods=['DELETE'])
def delete_advertisement(id):
    ad = Advertisement.query.get_or_404(id)
    db.session.delete(ad)
    db.session.commit()
    return jsonify({'status': 'Advertisement deleted'})


if __name__ == '__main__':
    app.run(debug=True)