
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "number_guessing_secret_key"


# Initialize a new game
def new_game():
    session["secret_number"] = random.randint(1, 100)
    session["attempts"] = 0
    session["message"] = "Enter your first guess!"
    session["game_over"] = False
    session["won"] = False
    session["guess_history"] = []


# Home page
@app.route("/")
def home():

    # Initialize missing session variables
    if "secret_number" not in session:
        new_game()

    if "guess_history" not in session:
        session["guess_history"] = []

    if "attempts" not in session:
        session["attempts"] = 0

    if "message" not in session:
        session["message"] = "Enter your first guess!"

    if "game_over" not in session:
        session["game_over"] = False

    if "won" not in session:
        session["won"] = False

    return render_template(
        "index.html",
        attempts=session["attempts"],
        message=session["message"],
        game_over=session["game_over"],
        won=session["won"],
        guess_history=session["guess_history"]
    )


# Check user guess
@app.route("/guess", methods=["POST"])
def guess():

    if "secret_number" not in session:
        new_game()

    if session["game_over"]:
        return redirect(url_for("home"))

    user_input = request.form.get("guess", "").strip()

    try:
        user_guess = int(user_input)

        if user_guess < 1 or user_guess > 100:
            session["message"] = "Enter a number between 1 and 100!"

        else:
            session["attempts"] += 1

            secret_number = session["secret_number"]

            if user_guess < secret_number:
                result = "Too Low"
                session["message"] = "Too Low! Try a higher number."

            elif user_guess > secret_number:
                result = "Too High"
                session["message"] = "Too High! Try a lower number."

            else:
                result = "Correct"
                session["message"] = (
                    f"Congratulations! You guessed {secret_number} correctly!"
                )
                session["game_over"] = True
                session["won"] = True

            history = session["guess_history"]
            history.append({
                "number": user_guess,
                "result": result
            })
            session["guess_history"] = history

    except ValueError:
        session["message"] = "Invalid input! Please enter a valid number."

    return redirect(url_for("home"))


# Restart game
@app.route("/restart")
def restart():
    new_game()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
