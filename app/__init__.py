from flask import Flask

def create_app(config=None):

    app = Flask(__name__)

    app.config.update({
        'DEBUG': True,
        'JSON_SORT_KEYS': False,
    })

    if config:
        app.config.update(config)


    return app
