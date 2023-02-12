from application import app
from dotenv import load_dotenv
import os

load_dotenv('.env')

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST')
    debug_mode = os.getenv('APP_MODE') == 'debug'
    app.run(host=host, debug=debug_mode)
