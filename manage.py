from app import app, db
from app.logconfig import logger
if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        print("Database tables created successfully.")
        logger.info("Database tables created successfully.")

        # Run the Flask application
        app.run(debug=True)

    except Exception as e:
        print(f"An error occurred while creating database tables: {str(e)}")
        logger.error(f"An error occurred while creating database tables: {str(e)}")
