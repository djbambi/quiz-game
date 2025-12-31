import requests


BASE_URL = "https://opentdb.com/api.php"


def fetch_questions(
    amount: int = 10,
    category: int | None = None,
    question_type: str = "boolean",
    timeout: int = 10,
) -> dict:
    params = {
        "amount": amount,
        "type": question_type,
    }

    if category is not None:
        params["category"] = category

    response = requests.get(BASE_URL, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def extract_question_data(payload: dict) -> list[dict]:
    response_code = payload["response_code"]
    if response_code != 0:
        raise ValueError(f"Unexpected response_code: {response_code}")

    results = payload["results"]
    return [
        {"text": item["question"], "answer": item["correct_answer"]} for item in results
    ]
