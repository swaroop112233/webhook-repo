# Import the webhook blueprint from your routes file
from app.webhook.routes import webhook_bp

# Factory function to create and configure the Flask app
def create_app():
    from flask import Flask
    
    # Create a Flask app instance
    app = Flask(__name__)
    
    # Register the webhook blueprint to handle routes
    app.register_blueprint(webhook_bp)
    
    # Return the configured Flask app
    return app
