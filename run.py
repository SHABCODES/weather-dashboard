from flask import Flask, jsonify
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Weather Dashboard API', 
            'status': 'Running!'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG)
