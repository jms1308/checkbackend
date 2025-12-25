from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='testuser').first():
        user = User(username='testuser', email='test@test.com', role='Admin')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        print("User created")
    else:
        print("User already exists")
