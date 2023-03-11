import tkinter as tk
import csv
import random
import sys

class Quiz:
    def __init__(self, master, filename):
        self.master = master
        self.filename = filename
        self.questions = []
        self.current_question = 0
        self.score = 0

        # Load questions from CSV file
        self.load_questions()

        # Shuffle questions and options
        random.shuffle(self.questions)
        for question in self.questions:
            random.shuffle(question["options"])

        # Create widgets
        self.question_label = tk.Label(master, text="", font=("Helvetica", 16), wraplength=500, pady=20)
        self.question_label.pack()

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(master, text="", font=("Helvetica", 14), pady=10, width=40, command=lambda i=i: self.select_option(i))
            button.pack(pady=10)
            self.option_buttons.append(button)

        self.score_label = tk.Label(master, text="", font=("Helvetica", 14), pady=20)
        self.score_label.pack()

        self.next_button = tk.Button(master, text="Next", font=("Helvetica", 14), pady=10, width=40, command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=20)

        # Ask first question
        self.ask_question()

    def load_questions(self):
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question = {"text": row["question"], "answer": row["answer"], "options": [row["answer"], row["decoy1"], row["decoy2"], row["decoy3"]]}
                self.questions.append(question)

    def ask_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=question["text"])

        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=option)

        for button in self.option_buttons:
            button.config(state=tk.NORMAL)

        self.next_button.config(state=tk.DISABLED)

    def select_option(self, index):
        selected_option = self.questions[self.current_question]["options"][index]
        correct_option = self.questions[self.current_question]["answer"]

        if selected_option == correct_option:
            self.score += 1

        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1

        if self.current_question == len(self.questions):
            self.show_score()
        else:
            self.ask_question()

    def show_score(self):
        self.question_label.config(text="Quiz finished!")
        self.next_button.config(text="Exit", command=self.master.destroy)
        self.score_label.config(text="Your score: {}/{}".format(self.score, len(self.questions)), pady=20)

# Check if input file was provided
if len(sys.argv) < 2:
    print("Usage: python quiz.py input_file.csv")
    sys.exit(1)

# Get input file name from command line argument
filename = sys.argv[1]

# Create main window
root = tk.Tk()
root.title("Quiz")
root.geometry("600x500")
root.configure(bg="#F5F5F5")

# Create quiz object
quiz = Quiz(root, filename)

# Start GUI event loop
root.mainloop()

