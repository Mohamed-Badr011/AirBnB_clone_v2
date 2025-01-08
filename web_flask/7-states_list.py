#!/usr/bin/python3
"""
Starts a Flask web application that interacts with the storage engine to display
a list of states in an HTML page.

Routes:
    /states_list: Displays a list of all states in alphabetical order.
"""

from flask import Flask, render_template
from models import *
from models import storage

# Initialize the Flask application
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Displays an HTML page with the list of states.

    The states are retrieved from the storage engine, sorted in alphabetical order
    by their name, and passed to the '7-states_list.html' template.

    Returns:
        str: Rendered HTML page with the list of states.
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Teardown function to close the storage.

    This function is executed after each request to ensure that the storage
    session is properly closed.

    Args:
        exception (Exception): The exception raised during the request (if any).
    """
    storage.close()


if __name__ == '__main__':
    """
    Main entry point for the application.

    The Flask app runs on host 0.0.0.0 and port 5000, making it accessible
    locally and on the network.
    """
    app.run(host='0.0.0.0', port='5000')

