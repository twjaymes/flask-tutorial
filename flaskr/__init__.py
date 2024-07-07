import os

from flask import Flask
import requests
from flask import Flask, jsonify, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    # API URL to fetch the summary data
    API_URL = 'https://api.congress.gov/v3/bill/117/hr/4980/summaries?api_key=q82Mbm5luDtmT0yMuxLP4eaGqqEpu0h7jWPMiBC1'

    @app.route('/')
    def index():
        # Render the base.html template
        return render_template('base.html')

    @app.route('/fetch_summary')
    def fetch_summary():
        # Make the API request to fetch the summary data
        response = requests.get(API_URL)
    
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            data = response.json()
            try:
                # Extract the summary text from the JSON response
                summary = data['summaries'][0]['text']
            except (KeyError, IndexError):
                # Handle cases where the expected data is not found in the response
                summary = "No summary available."
        else:
            # Handle cases where the API request fails
            summary = "Error fetching data."

        # Return the summary as a JSON response
        return jsonify({'summary': summary})

    @app.route('/routes')
    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, str(rule)))
            output.append(line)
        return "<br>".join(sorted(output))

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app