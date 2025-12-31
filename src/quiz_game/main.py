from question_model import Question
from quiz_brain import QuizBrain

# from data import question_data
from fetch_questions import fetch_questions, extract_question_data

fetched_questions = fetch_questions()

question_bank = []
question_data = extract_question_data(fetched_questions)

for question in question_data:
    new_question = Question(question["text"], question["answer"])
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the Quiz!")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
