import os
from app import create_app
from app.extensions import db
from app.models.expense import Expense
from datetime import datetime

app = create_app()

with app.app_context():
    db.create_all()
    # Add some sample expenses if the database is empty
    if Expense.query.count() == 0:
        expenses = [
            Expense(title='Coffee', amount=3.50, category='Food', date=datetime.strptime('2025-01-01', '%Y-%m-%d').date()),
            Expense(title='Laptop', amount=1200, category='Electronics', date=datetime.strptime('2025-01-02', '%Y-%m-%d').date()),
            Expense(title='Groceries', amount=75.20, category='Food', date=datetime.strptime('2025-01-03', '%Y-%m-%d').date())
        ]
        db.session.add_all(expenses)
        db.session.commit()

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 8081
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)
