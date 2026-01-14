from config import app, db
from models import Episode, Guest, Appearance
import csv

with app.app_context():
    db.drop_all()
    db.create_all()
    
    try:
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                episode = Episode.query.filter_by(number=int(row['Show'])).first()
                if not episode:
                    episode = Episode(date=row['Date'], number=int(row['Show']))
                    db.session.add(episode)
                
                guest = Guest.query.filter_by(name=row['Raw_Guest_List']).first()
                if not guest:
                    guest = Guest(name=row['Raw_Guest_List'], occupation=row.get('GoogleKnowlege_Occupation', 'Unknown'))
                    db.session.add(guest)
                
                db.session.commit()
                
                appearance = Appearance(rating=int(row.get('IMDB_Rating', 3)), episode_id=episode.id, guest_id=guest.id)
                db.session.add(appearance)
            
            db.session.commit()
            
    except FileNotFoundError:
        print("CSV file not found. Creating sample data...")
        e1 = Episode(date="1/11/99", number=1)
        e2 = Episode(date="1/12/99", number=2)
        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        g3 = Guest(name="Tracey Ullman", occupation="television actress")
        
        db.session.add_all([e1, e2, g1, g2, g3])
        db.session.commit()
        
        a1 = Appearance(rating=4, episode_id=e1.id, guest_id=g1.id)
        a2 = Appearance(rating=5, episode_id=e2.id, guest_id=g3.id)
        
        db.session.add_all([a1, a2])
        db.session.commit()
    
    print("Database seeded!")
