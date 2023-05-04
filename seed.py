from models import User, NYTList, db
from app import app
import json

# to run this, just $ python seed.py

# Add a few fake users

with app.app_context():
    db.drop_all()
    db.create_all()

u1 = User(email="sadman@sadman.com", username = "sadman22", password = "$2b$12$p690WxW7ttjoXYjJ5SaZK.LnQrEgaGgawy8rjwWo1Sba97s1BgbtS", image_url="https://images.unsplash.com/photo-1457140072488-87e5ffde2d77?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80", bio="I am happy to be here. Yes, I am")

u2 = User(email="carrie@sohappy.com", username="carrie", password="$2b$12$M1ir6.Awr2dz97m7PzVaLeCngb4fW.yDVJcI8OUtdP7ePR604CUhK", image_url = "", bio = "Reading is just so much darn fun.")

u3 = User(email="markymark@mark.com", username="markymark", password="$2b$12$hFXVuN4OJ5pcZAN1BtOkpu99swi4QNXMj48hcfvU42r5AIHxeoIpq", image_url = "", bio = "Sometimes I just want to go read a book.")

with app.app_context():
    db.session.add_all([u1, u2, u3])
    db.session.commit()

# Add NYT lists in bulk

list_file = open('generator/lists-names.json')
data = json.load(list_file)
lists = data['results']

keys_to_keep = ['list_name', 'list_name_encoded', 'oldest_published_date', 'newest_published_date']
new_lists = [{key: value for key, value in dictionary.items() if key in keys_to_keep} for dictionary in lists]

with app.app_context():
    db.session.bulk_insert_mappings(NYTList, new_lists)
    db.session.commit()

# Now add Books


