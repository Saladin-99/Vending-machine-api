from app import app, db

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        print("Database tables created successfully.")

        # Run the Flask application
        app.run(debug=True)

    except Exception as e:
        print(f"An error occurred while creating database tables: {str(e)}")
