# wordle_methods.py

def read_in_file(file_name):
    """Read words from a file and return them as a list."""
    words_list = []
    try:
        with open(file_name, "r") as file:
            for word in file:
                words_list.append(word.strip()) 
    except FileNotFoundError:
        print("File not found.")
    return words_list

def filter_words(words, guess, feedback):
    """Filter words based on the guess and the feedback."""
    filtered_words = []
    
    for word in words:
        # Create a copy of the word as a list for mutable operations
        temp_word_list = list(word)
        
        # First pass: Process 'green' feedback
        for i in range(len(guess)):
            if feedback[i] == 'g':
                if guess[i] != word[i]:
                    break
                else:
                    # Remove the matched letter to avoid re-matching in 'yellow' processing
                    temp_word_list[i] = None
        else:
            # Second pass: Process 'yellow' and 'black' feedback
            for i in range(len(guess)):
                if feedback[i] == 'y':
                    if guess[i] not in temp_word_list or guess[i] == word[i]:
                        break
                    else:
                        # Remove the first occurrence of this letter from the temp word list to handle repeats
                        temp_word_list[temp_word_list.index(guess[i])] = None
                elif feedback[i] == 'b':
                    if guess[i] in temp_word_list:
                        break
            else:
                # If both loops complete without breaking, it's a match
                filtered_words.append(word)

    return filtered_words




# Logic used to calculate the best guess.
def calculate_letter_frequencies(words):
    """Calculate the frequency of each letter in the list of words."""
    letter_frequencies = {}
    for word in words:
        for letter in word:
            if letter in letter_frequencies:
                letter_frequencies[letter] += 1
            else:
                letter_frequencies[letter] = 1
    return letter_frequencies

def calculate_positional_letter_frequencies(words):
    """Calculate the frequency of each letter in each position in the list of words."""
    letter_frequencies = [{} for _ in range(5)]
    for word in words:
        for position, letter in enumerate(word):
            if letter in letter_frequencies[position]:
                letter_frequencies[position][letter] += 1
            else:
                letter_frequencies[position][letter] = 1
    return letter_frequencies

def calculate_best_guess(possible_words):
    """Calculate the best guess based on positional letter frequencies."""
    positional_frequencies = calculate_positional_letter_frequencies(possible_words)
    best_guess = None
    best_score = -1
    
    for word in possible_words:
        score = sum(positional_frequencies[i].get(letter, 0) for i, letter in enumerate(word))
        if score > best_score:
            best_score = score
            best_guess = word
    
    return best_guess

# Modify the solver function to use calculate_best_guess
def solver():
    possible_words = read_in_file("possible_answers.txt")
    
    for attempt in range(6):
        if not possible_words:
            print("No possible words left. Exiting.")
            return
        
        # Use the calculate_best_guess function to select the next guess
        print("Best Guess: " + calculate_best_guess(possible_words))
        guess = input("Enter the word: ").strip().lower()
        feedback = input("Enter feedback (g for green, y for yellow, b for black): ").strip().lower()
        

        # Checks if the user wants to quit the game.
        if guess == 'q' or feedback == 'q': 
            print("Quitting the game. Goodbye!")
            return
        
        # Update possible words based on the feedback
        possible_words = filter_words(possible_words, guess, feedback)
        
        if feedback == "ggggg":
            print("Congratulations! You've guessed correctly!")
            return
        else:
            print(f"Possible words left: {len(possible_words)}")
            print("Possible words:", possible_words)
    
    print("Game over. Try again!")
