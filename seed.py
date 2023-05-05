from models import db, User, NYTList, Book, UserBooks, UserLists
from app import app
import json

# to run this, just $ python seed.py

# Add a few fake users

with app.app_context():
    db.drop_all()
    db.create_all()

u1 = User(email="sadman@sadman.com", username="sadman22", password="$2b$12$p690WxW7ttjoXYjJ5SaZK.LnQrEgaGgawy8rjwWo1Sba97s1BgbtS",
          image_url="https://images.unsplash.com/photo-1500099817043-86d46000d58f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80", bio="Why is coding so hard? I mean wow.")

u2 = User(email="carrie@sohappy.com", username="carrie", password="$2b$12$M1ir6.Awr2dz97m7PzVaLeCngb4fW.yDVJcI8OUtdP7ePR604CUhK",
          image_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80", bio="I enjoy chickens who drink strong cocktails.")

u3 = User(email="markymark@mark.com", username="markymark", password="$2b$12$hFXVuN4OJ5pcZAN1BtOkpu99swi4QNXMj48hcfvU42r5AIHxeoIpq",
          image_url="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1160&q=80", bio="Sometimes I just want to go read a book.")

# https://images.unsplash.com/photo-1500099817043-86d46000d58f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80

# https://images.unsplash.com/photo-1457140072488-87e5ffde2d77?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80

with app.app_context():
    db.session.add_all([u1, u2, u3])
    db.session.commit()

# Add NYT lists in bulk

list_file = open('generator/lists-names.json')
data = json.load(list_file)
lists = data['results']

keys_to_keep = ['list_name', 'list_name_encoded',
                'oldest_published_date', 'newest_published_date']
new_lists = [{key: value for key, value in dictionary.items() if key in keys_to_keep}
             for dictionary in lists]

with app.app_context():
    db.session.bulk_insert_mappings(NYTList, new_lists)
    db.session.commit()

# Now add Books

books = [
    {
        "isbns_combined": "07352190959780735219090",
        "title": "WHERE THE CRAWDADS SING",
        "author": "Delia Owens",
        "description": "In a quiet town on the North Carolina coast in 1969, a young woman who survived alone in the marsh becomes a murder suspect.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9780735219090.jpg"
    },
    {
        "isbns_combined": "05255362999780525536291",
        "title": "THE VANISHING HALF",
        "author": "Brit Bennett",
        "description": "The lives of twin sisters who run away from a Southern Black community at age 16 diverge as one returns and the other takes on a different racial identity but their fates intertwine.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9780525536291.jpg"
    },
    {
        "isbns_combined": "19821829119781982182915",
        "title": "PERIL",
        "author": "Bob Woodward and Robert Costa",
        "description": "The Washington Post journalists detail the dangers and challenges during the transition to the Biden presidency.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9781982182915.jpg"
    },
    {
        "isbns_combined": "006308001X9780063080010",
        "title": "UNCONTROLLED SPREAD",
        "author": "Scott Gottlieb",
        "description": "The former F.D.A. commissioner assesses America’s Covid-19 response and prescribes ways to prepare for other pandemics.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9780063080010.jpg"
    },
    {
        "isbns_combined": "07611690839780761169086",
        "title": "ATLAS OBSCURA",
        "author": "Joshua Foer, Dylan Thuras and Ella Morton",
        "description": "A dense (nearly 500 pages) richly documented ultimate explorer's guide to more than 700 hidden marvels, events and curiosities around the world.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9780761169086.jpg"
    },
    {
        "isbns_combined": "030746489X9780307464897",
        "title": "COOKING FOR JEFFREY",
        "author": "Ina Garten",
        "description": "A collection of recipes for dishes the Barefoot Contessa makes for her husband.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9780307464897.jpg"
    },
    {
        "isbns_combined": "16233635869781623363581",
        "title": "THUG KITCHEN",
        "author": "the staff of Thug Kitchen",
        "description": "More than 100 vegan recipes, including cornmeal waffles with strawberry syrup, from the creators of the popular, irreverent website.",
        "image_url": "https://storage.googleapis.com/du-prd/books/images/9781623363581.jpg"
    }
]

with app.app_context():
    db.session.bulk_insert_mappings(Book, books)
    db.session.commit()

# Now assign books and lists to users

book_assignments = [
    {
        "user_id": 1,
        "book_id": 1
    },
    {
        "user_id": 1,
        "book_id": 2
    },
    {
        "user_id": 1,
        "book_id": 3
    },
    {
        "user_id": 1,
        "book_id": 4
    },
    {
        "user_id": 1,
        "book_id": 5
    },
    {
        "user_id": 2,
        "book_id": 2
    },
    {
        "user_id": 2,
        "book_id": 3
    },
    {
        "user_id": 2,
        "book_id": 4
    },
    {
        "user_id": 2,
        "book_id": 5
    },
    {
        "user_id": 2,
        "book_id": 6
    },
    {
        "user_id": 3,
        "book_id": 3
    },
    {
        "user_id": 3,
        "book_id": 4
    },
    {
        "user_id": 3,
        "book_id": 5
    },
    {
        "user_id": 3,
        "book_id": 6
    },
    {
        "user_id": 3,
        "book_id": 7
    }
]

list_assignments = [
    {
        "user_id": 1,
        "list_id": 1
    },
    {
        "user_id": 1,
        "list_id": 3
    },
    {
        "user_id": 1,
        "list_id": 5
    },
    {
        "user_id": 1,
        "list_id": 7
    },
    {
        "user_id": 1,
        "list_id": 9
    },
    {
        "user_id": 2,
        "list_id": 2
    },
    {
        "user_id": 2,
        "list_id": 4
    },
    {
        "user_id": 2,
        "list_id": 6
    },
    {
        "user_id": 2,
        "list_id": 12
    },
    {
        "user_id": 2,
        "list_id": 22
    },
    {
        "user_id": 3,
        "list_id": 15
    },
    {
        "user_id": 3,
        "list_id": 19
    },
    {
        "user_id": 3,
        "list_id": 30
    },
    {
        "user_id": 3,
        "list_id": 40
    },
    {
        "user_id": 3,
        "list_id": 43
    }
]

with app.app_context():
    db.session.bulk_insert_mappings(UserBooks, book_assignments)
    db.session.bulk_insert_mappings(UserLists, list_assignments)
    db.session.commit()