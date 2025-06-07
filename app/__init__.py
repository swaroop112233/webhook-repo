from app.webhook.routes import webhook_bp

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(webhook_bp)
    return app
