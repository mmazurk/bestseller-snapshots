from models import User, db
from app import app

# to run this, just $ python seed.py

db.drop_all()
db.create_all()

u1 = User(email="sadman@sadpeople.com", username = "sadman22", password = "$2b$12$pbJzlgvsVorrdrzghyq1SOf2C18pEhU7JzyF9BKKzKbDat.Y4omjm", image_url="", bio="I am not happy as a clam.")

db.session.add(u1)
db.session.commit()

