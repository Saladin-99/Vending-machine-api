class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/vending_machine'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key' #for auth