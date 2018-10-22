import os
from app import create_app


config_name='development'
app=create_app(config_name)

@app.route('/')
def landing_page():
    
    return "Welcome to Bolton Store Manager"


if __name__== '__main__':
    app.run()

