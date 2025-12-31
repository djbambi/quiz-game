from src.quiz_game.quiz_brain import QuizBrain
from types import SimpleNamespace


def test_quiz_brain_initial_state():
    questions = ["Q1", "Q2", "Q3"]

    quiz = QuizBrain(questions)

    assert quiz.question_number == 0
    assert quiz.question_list == questions


def test_next_question_prompts_with_correct_number_and_text():
    questions = [SimpleNamespace(text="Sky is blue?")]
    captured = {}

    def fake_input(prompt: str) -> str:
        captured["prompt"] = prompt
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)

    quiz.next_question()

    assert captured["prompt"] == "Q.1: Sky is blue? (True/False)?: "


def test_next_question_increments_question_number():
    questions = [SimpleNamespace(text="Sky is blue?")]
    quiz = QuizBrain(questions, input_func=lambda _: "True")

    quiz.next_question()

    assert quiz.question_number == 1


def test_next_question_asks_second_question_on_second_call():
    questions = [
        SimpleNamespace(text="First?"),
        SimpleNamespace(text="Second?"),
    ]
    prompts = []

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)

    quiz.next_question()
    quiz.next_question()

    assert prompts[0] == "Q.1: First? (True/False)?: "
    assert prompts[1] == "Q.2: Second? (True/False)?: "
    assert quiz.question_number == 2


def test_still_has_questions_returns_true_when_questions_remain():
    questions = [SimpleNamespace(text="Q1"), SimpleNamespace(text="Q2")]
    quiz = QuizBrain(questions)

    assert quiz.still_has_questions() is True


def test_still_has_questions_false_at_exact_length():
    questions = [SimpleNamespace(text="Q1"), SimpleNamespace(text="Q2")]
    quiz = QuizBrain(questions)

    quiz.question_number = 2

    assert quiz.still_has_questions() is False
