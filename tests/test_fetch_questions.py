from src.quiz_game.fetch_questions import extract_question_data


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
