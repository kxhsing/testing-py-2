"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import Game, connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    session['RSVP'] = True
    flash("Yay!")
    return redirect("/")


@app.route("/games")
def games():

    if session['RSVP']:
        games = Game.query.all()
        return render_template("games.html", games=games)
    else:
        return redirect('/')


@app.route('/add-game')
def add_game():

    return render_template("game_form.html")

@app.route('/add-game', methods=["POST"])
def game_submit():
    title = request.form.get("name")
    description = request.form.get("description")

    game = Game(name=title, description=description)

    db.session.add(game)
    db.session.commit()

    return redirect('/games')

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
