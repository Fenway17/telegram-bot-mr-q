import os
from flask import Flask
from bot.api.route.home import home_api
# from bot.api.handler.main import bot_handler

def create_app():
    app = Flask(__name__)

    app.config['BOT_KEY'] = os.getenv('BOT_KEY')
    app.config.from_pyfile('config.py')
    # register home blueprint
    app.register_blueprint(home_api, url_prefix='/api')
    # app.register_blueprint(bot_handler)
    return app
    
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port, debug=True)
