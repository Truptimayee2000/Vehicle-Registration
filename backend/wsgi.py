from vehicle_data_api import app
from dbconfig import db
from load_data import load_initial_data


with app.app_context():
    db.create_all()  
    load_initial_data()
    print("Tables created successfully!")

if __name__ == "__main__":
    app.run(debug=True)
