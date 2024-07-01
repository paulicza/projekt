from app import db
from app.models import Restaurant, User
from werkzeug.security import generate_password_hash

db.create_all()

# Przykładowe sale weselne
restaurants = [
    {
        'name': 'Sala Weselna Krakowianka',
        'location': 'Kraków, ul. Krakowska 1',
        'menu': 'Menu 1: Rosół, Kotlet schabowy, Deser. Menu 2: Zupa pomidorowa, Ryba, Deser.',
        'capacity': 100
    },
    {
        'name': 'Restauracja Wesele',
        'location': 'Kraków, ul. Rynek 2',
        'menu': 'Menu 1: Barszcz, Pierogi, Deser. Menu 2: Zupa grzybowa, Gulasz, Deser.',
        'capacity': 150
    },
    {
        'name': 'Dom Weselny Krakus',
        'location': 'Kraków, ul. Wawelska 3',
        'menu': 'Menu 1: Żurek, Kurczak, Deser. Menu 2: Zupa ogórkowa, Wieprzowina, Deser.',
        'capacity': 200
    }
]

for r in restaurants:
    restaurant = Restaurant(name=r['name'], location=r['location'], menu=r['menu'], capacity=r['capacity'])
    db.session.add(restaurant)

# Przykładowy użytkownik
user = User(username='admin', email='admin@example.com', password=generate_password_hash('password'))
db.session.add(user)

db.session.commit()
