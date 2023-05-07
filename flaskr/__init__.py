"""The main flask app."""
from flask import Flask, request, render_template
import requests


def create_app(test_config=None):

    """Create and configure the app."""
    app = Flask(__name__)

    @app.route('/')
    def index():
        """The home page."""
        return render_template('home.html')

    @app.route('/search', methods=['GET'])
    def search():
        """Search for a species."""

        # Get the search string
        search_str = request.args['search']
        print(search_str)
        url = 'https://api.gbif.org/v1/species/search'
        result = requests.get(url, params={'q': search_str})
        print(result.json())
        return render_template('home.html')


    return app


if __name__ == '__main__':
    app = create_app()
