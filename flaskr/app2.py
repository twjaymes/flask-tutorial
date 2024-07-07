from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

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

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)