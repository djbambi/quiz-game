from src.quiz_game.question_model import Question


def test_question_stores_text_and_answer():
    q = Question("What is 2 + 2?", "4")

    assert q.text == "What is 2 + 2?"
    assert q.answer == "4"
