from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/test')
def api_test():
    return {"status": "working", "message": "API is ready"}

if __name__ == '__main__':
    port = 5000
    print("=" * 50)
    print("🌤️ WEATHER DASHBOARD STARTING")
    print("=" * 50)
    print(f"📍 Port: {port}")
    print(f"🔗 Local URL: http://127.0.0.1:{port}")
    print(f"🌐 Public URL: https://{os.environ.get('CODESPACE_NAME', 'localhost')}-{port}.app.github.dev")
    print("=" * 50)
    
    # Try to import and register API routes
    try:
        from app.api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        print("✅ API routes registered")
    except Exception as e:
        print(f"⚠️ API routes not available: {e}")
    
    app.run(host='0.0.0.0', port=port, debug=True)