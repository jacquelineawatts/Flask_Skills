from flask import Flask, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def index_page():
    """Show an index page."""

    return render_template("index.html")


@app.route("/application-form")
def application_form():
    """Show the application form """

    return render_template("application-form.html")


@app.route('/application', methods=["POST"])
def application_confirmation():
    """Show to confirm application form submission"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    salary = request.form.get('salary')
    position = request.form.get('position')

    is_complete = True

    if first_name and last_name and salary and position:
        flash("""Thank you for submitting an application for {}, {} {}. You've
                indicated a minimum salary requirement of ${}. We look forward to
                being in touch shortly!""".format(position, first_name, last_name, salary))

    else:
        is_complete = False
        flash("""Your application seems to be incomplete! Please enter all form fields.""")

    return render_template("application-response.html", is_complete=is_complete)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
