from application import create_app
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = create_app()

if __name__ == "__main__":
    host = os.getenv('FLASK_HOST')
    debug_mode = os.getenv('APP_MODE') == 'debug'
    app.run(host='0.0.0.0', debug=True)
