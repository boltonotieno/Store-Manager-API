import os
from application.app import create_app

config_name=os.getenv('FLASK_ENV')
app=create_app(config_name)
app.config['SECRET_KEY'] = 'the-secret-secret'

if __name__== '__main__':
    app.run()

