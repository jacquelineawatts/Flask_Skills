from flask import Flask, render_template, flash, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = '\x90\xc0|\xb7\xbd\xd4\xd2\xf1"\x94\x18\xb9\xed\x84\xb8\x9e\x18\x7f\xf6\x83rkb\xd1'


@app.route("/")
def index_page():
    """Show an index page."""

    return render_template("index.html")


@app.route("/application-form")
def application_form():
    """Show the application form """

    # Checks for presence of application progress in session keys
    application_progress = session.get('application_input', [])

    # Saves positions as unicode to enable comparison of session values in application form
    positions = [unicode(position) for position in ['Software Engineer', 'QA Engineer', 'Product Manager']]

    return render_template("application-form.html", application_progress=application_progress, positions=positions)


@app.route('/application', methods=["POST"])
def application_confirmation():
    """Show to confirm application form submission or redirect if incomplete."""

    # Gets form submission values from /application-form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    salary = request.form.get('salary')
    position = request.form.get('position')

    # Saves all inputs into session key to access in the case of incomplete form submission
    session['application_input'] = [first_name, last_name, salary, position]

    # Handles form submissions when all fields completed
    if first_name and last_name and salary and position:
        flash("""Thank you for submitting an application for {}, {} {}. You've
                indicated a minimum salary requirement of ${}. We look forward to
                being in touch shortly!""".format(position, first_name, last_name, salary))
        return render_template("application-response.html")

    # Handles incomplete form submissions by redirecting back to form
    else:
        flash("""Your application seems to be incomplete! Please enter all form fields.""")
        return redirect('/application-form')

# -------------------------------- RUN APPLICATION -----------------------------

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
