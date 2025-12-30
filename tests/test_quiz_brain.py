from src.quiz_game.quiz_brain import QuizBrain


def test_quiz_brain_initial_state():
    questions = ["Q1", "Q2", "Q3"]

    quiz = QuizBrain(questions)

    assert quiz.question_number == 0
    assert quiz.question_list == questions
