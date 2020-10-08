import os

from app import create_app

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
<<<<<<< HEAD
    app.run()
=======
    app.run()
>>>>>>> 5a4286af0679cfdf1e5113bfd0b233c880b1826d
