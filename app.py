import os
import logging
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Register API routes
from api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500

# Root route for documentation
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/docs')
def api_docs():
    from flask import render_template
    return render_template('api_documentation.html')

if __name__ == '__main__':
    app.run(debug=True)
