import os
import os, json, base64

from os import environ, path
from dotenv import load_dotenv

from flask import Flask
from bot.api.route.home import home_api
from bot.api.handler import main
from bot.api.handler import main

from database import Database
def create_app():
    app = Flask(__name__)
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))
    # register blueprints
    app.register_blueprint(home_api, url_prefix='/api')
    return app
    
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()
    database = Database(os.getenv('G_KEY')) # os.getenv only works when the main function is invoked.
    main()
    
    app.run(host='0.0.0.0', port=port, debug=True)