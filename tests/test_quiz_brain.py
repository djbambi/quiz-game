"""
tests/test_quiz_brain.py

Pytest test suite for QuizBrain.

Assumptions:
- Your class lives in a module you can import, e.g. `quiz_brain.py` or `rp_poetry/quiz_brain.py`.
- Update the import line below to match your project structure.
"""

from types import SimpleNamespace
from src.quiz_game.quiz_brain import QuizBrain

import pytest


# -----------------------------
# Helpers
# -----------------------------
def make_questions(*pairs):
    """
    Create lightweight question objects with `.text` and `.answer`.
    Example: make_questions(("Q1", "True"), ("Q2", "False"))
    """
    return [SimpleNamespace(text=text, answer=answer) for text, answer in pairs]


# -----------------------------
# __init__
# -----------------------------
def test_init_sets_defaults_and_stores_dependencies():
    questions = make_questions(("Q1", "True"))

    def fake_input(_):
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)

    assert quiz.question_number == 0
    assert quiz.score == 0
    assert quiz.question_list is questions
    assert quiz._input is fake_input


# -----------------------------
# still_has_questions
# -----------------------------
def test_still_has_questions_true_when_questions_remain():
    quiz = QuizBrain(make_questions(("Q1", "True"), ("Q2", "False")))
    assert quiz.still_has_questions() is True


def test_still_has_questions_false_when_no_questions_remain():
    quiz = QuizBrain(make_questions(("Q1", "True")))
    quiz.question_number = 1  # simulate having asked the only question
    assert quiz.still_has_questions() is False


def test_still_has_questions_true_when_question_number_less_than_length():
    quiz = QuizBrain(make_questions(("Q1", "True"), ("Q2", "False")))
    quiz.question_number = 1
    assert quiz.still_has_questions() is True


# -----------------------------
# next_question
# -----------------------------
def test_next_question_increments_question_number_and_prompts_correctly():
    questions = make_questions(("Sky is blue?", "True"))
    captured = {}

    def fake_input(prompt: str) -> str:
        captured["prompt"] = prompt
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)

    # prevent printing / scoring logic from interfering with this test
    called = {}

    def fake_check_answer(user_answer, correct_answer):
        called["user_answer"] = user_answer
        called["correct_answer"] = correct_answer

    quiz.check_answer = fake_check_answer

    quiz.next_question()

    assert quiz.question_number == 1
    assert captured["prompt"] == "Q.1: Sky is blue? (True/False)?: "
    assert called == {"user_answer": "True", "correct_answer": "True"}


def test_next_question_asks_second_question_on_second_call():
    questions = make_questions(("First?", "True"), ("Second?", "False"))
    prompts = []

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return "True"

    quiz = QuizBrain(questions, input_func=fake_input)

    # stub answer checking to isolate this test from print behavior
    quiz.check_answer = lambda *_: None

    quiz.next_question()
    quiz.next_question()

    assert prompts[0] == "Q.1: First? (True/False)?: "
    assert prompts[1] == "Q.2: Second? (True/False)?: "
    assert quiz.question_number == 2


def test_next_question_raises_index_error_when_out_of_questions():
    questions = make_questions(("Only one", "True"))
    quiz = QuizBrain(questions, input_func=lambda _: "True")
    quiz.check_answer = lambda *_: None

    quiz.next_question()  # consumes the only question

    with pytest.raises(IndexError):
        quiz.next_question()


# -----------------------------
# check_answer
# -----------------------------
def test_check_answer_correct_increments_score_and_prints_feedback(capsys):
    quiz = QuizBrain(make_questions(("Q1", "True")))
    quiz.question_number = 1  # matches typical call path from next_question()

    quiz.check_answer("true", "True")

    assert quiz.score == 1

    out = capsys.readouterr().out
    assert "You got it right!" in out
    assert "The correct answer was: True." in out
    assert "Your current score is: 1/1" in out


def test_check_answer_wrong_does_not_increment_score_and_prints_feedback(capsys):
    quiz = QuizBrain(make_questions(("Q1", "True")))
    quiz.question_number = 1  # matches typical call path from next_question()

    quiz.check_answer("False", "True")

    assert quiz.score == 0

    out = capsys.readouterr().out
    assert "That's wrong." in out
    assert "The correct answer was: True." in out
    assert "Your current score is: 0/1" in out


def test_check_answer_is_case_insensitive_for_correctness(capsys):
    quiz = QuizBrain(make_questions(("Q1", "True")))
    quiz.question_number = 1

    quiz.check_answer("TRUE", "true")

    assert quiz.score == 1
    out = capsys.readouterr().out
    assert "You got it right!" in out


def test_check_answer_prints_blank_line_separator(capsys):
    quiz = QuizBrain(make_questions(("Q1", "True")))
    quiz.question_number = 1

    quiz.check_answer("True", "True")

    out = capsys.readouterr().out
    # The method prints an extra newline string at the end: print("\n")
    # So we just assert there is at least one blank line present.
    assert "\n\n" in out
