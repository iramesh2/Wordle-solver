from flask import Flask, request, render_template_string
import woordle_methods

app = Flask(__name__)

# This route will display the form where users can submit their guesses
@app.route('/', methods=['GET'])
def index():
    return render_template_string(open('templates/index.html').read())

# This route processes the guesses and displays the result
@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess'].lower()
    feedback = request.form['feedback'].lower()
    # Here, you need to integrate the logic to use the guess and feedback to update the solver's state
    # For demonstration, this will simply echo back the guess and feedback
    result = f"Guess: {guess}, Feedback: {feedback}"
    # You should replace this with the actual logic to update and interact with your Wordle solver
    return render_template_string(open('templates/result.html').read(), result=result)

if __name__ == '__main__':
    app.run(debug=True)
