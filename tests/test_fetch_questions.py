from src.quiz_game.fetch_questions import extract_question_data
import pytest


def test_extract_question_data_returns_expected_list():
    payload = {
        "response_code": 0,
        "results": [
            {
                "question": "It is automatically considered entrapment in the United States if the police sell you illegal substances without revealing themselves.",
                "correct_answer": "False",
            },
            {
                "question": "An eggplant is a vegetable.",
                "correct_answer": "False",
            },
        ],
    }

    expected = [
        {
            "text": "It is automatically considered entrapment in the United States if the police sell you illegal substances without revealing themselves.",
            "answer": "False",
        },
        {"text": "An eggplant is a vegetable.", "answer": "False"},
    ]

    assert extract_question_data(payload) == expected

def test_extract_question_data_empty_results_returns_empty_list():
    payload = {"response_code": 0, "results": []}
    assert extract_question_data(payload) == []


def test_extract_question_data_raises_when_response_code_not_zero():
    payload = {"response_code": 1, "results": []}
    with pytest.raises(ValueError):
        extract_question_data(payload)