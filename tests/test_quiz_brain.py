from src.quiz_game.quiz_brain import QuizBrain
from types import SimpleNamespace


def test_quiz_brain_initial_state():
    questions = ["Q1", "Q2", "Q3"]

    quiz = QuizBrain(questions)

    assert quiz.question_number == 0
    assert quiz.question_list == questions


def test_next_question_prompts_correctly():
    questions = [SimpleNamespace(text="Sky is blue?")]
    captured = {}

    def fake_input(prompt):
        captured["prompt"] = prompt
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)
    quiz.next_question()

    assert captured["prompt"] == "Q.1: Sky is blue? (True/False)?: "
