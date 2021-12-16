import os
from flask import Flask
from bot.api.route.home import home_api
from bot.api.handler.main import main

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
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
    main()
    
    app.run(host='0.0.0.0', port=port, debug=True)