"""The main flask app."""
from flask import Flask, request, render_template


def create_app(test_config=None):

    """Create and configure the app."""
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/search', methods=['GET'])
    def search():
        """Search for a species."""
        print('a')

    return app


if __name__ == '__main__':
    app = create_app()
