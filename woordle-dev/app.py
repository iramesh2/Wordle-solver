from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from flask import send_from_directory
import woordle_methods

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize 'history' in session if it doesn't exist
    if 'history' not in session:
        session['history'] = []

    if 'possible_words' not in session or 'best_guess' not in session:
        # On first access or new game, initialize with all possible answers
        session['possible_words'] = woordle_methods.read_in_file("possible_answers.txt")
        session['best_guess'] = woordle_methods.calculate_best_guess(session['possible_words'])
        session['win'] = False  # Ensure the win flag is reset at the start of a new game

    win_condition_met = False  # Local flag to determine if the win screen should be shown

    if request.method == 'POST':
        guess = request.form['guess'].lower()
        feedback = request.form['feedback'].lower()
        # Check for win condition
        if feedback == "ggggg":
            win_condition_met = True
            session['win'] = True  # Set win flag in session for persistence if needed
        else:
            session['win'] = False  # Reset win flag in session
            # Continue game logic only if not won
            session['history'].append({'guess': guess, 'feedback': feedback})
            session['possible_words'] = woordle_methods.filter_words(session['possible_words'], guess, feedback)
            session['best_guess'] = woordle_methods.calculate_best_guess(session['possible_words'])

    if win_condition_met:
        message = "Congratulations! You've guessed the word correctly!"
    elif not session['possible_words']:
        message = "No possible words left. Start a new game."
        # Clear the session for a new game
        session.pop('possible_words', None)
        session.pop('best_guess', None)
        session['win'] = False  # Ensure the win flag is reset
        session['history'] = []  # Reset history for a new game
    else:
        message = session['best_guess']

    session.modified = True  # Notify Flask that the session has changed
    
    # Pass the win condition and message to the template
    return render_template('index.html', best_guess=message, win=session.get('win', False), history=len(session.get('history', [])))

@app.route('/undo', methods=['GET'])
def undo():
    if session.get('history'):
        # Remove the last action
        session['history'].pop()
        # Reset possible words and recalculate based on updated history
        session['possible_words'] = woordle_methods.read_in_file("possible_answers.txt")
        for action in session['history']:
            session['possible_words'] = woordle_methods.filter_words(session['possible_words'], action['guess'], action['feedback'])
        session['best_guess'] = woordle_methods.calculate_best_guess(session['possible_words'])
        session['win'] = False  # Reset win condition since we're undoing
    return redirect(url_for('index'))

@app.route('/restart', methods=['GET'])
def restart():
    # Clear the session variables related to the game
    session.pop('possible_words', None)
    session.pop('best_guess', None)

    
    return redirect(url_for('index'))

@app.route('/logo.png')
def logo():
    return send_from_directory(app.root_path, 'logo.png')

if __name__ == '__main__':
    app.run(debug=True)

