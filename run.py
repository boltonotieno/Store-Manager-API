import os
from application.app import create_app

app=create_app('FLASK_ENV')

if __name__ == '__main__':
    app.run()

