from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text="Score:", fg='white', bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(bg='white', height=250, width=300)
        self.question_text = self.canvas.create_text(150, 125, text='some text',width=280, font=('Arial', 15, 'italic'))
        self.canvas.grid(row=1,column=0, columnspan=2)

        self.true_img = PhotoImage(file='images/true.png')
        self.false_img = PhotoImage(file='images/false.png')

        self.true_btn = Button(image=self.true_img, highlightthickness=0, command=self.correct_answer)
        self.true_btn.grid(row=2, column=0, padx=20, pady=20)

        self.false_btn = Button(image=self.false_img, highlightthickness=0, command=self.incorrect_answer)
        self.false_btn.grid(row=2, column=1, padx=20, pady=20)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg='white')
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.true_btn.config(state='disabled')
            self.false_btn.config(state='disabled')
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")

    def correct_answer(self):
        is_right = self.quiz.check_answer('True')
        self.give_feedback(is_right)

    def incorrect_answer(self):
        is_right = self.quiz.check_answer('False')
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')
        self.window.after(1000,self.get_next_question)










