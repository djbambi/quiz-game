def extract_question_data(payload: dict) -> list[dict]:
    response_code = payload["response_code"]
    if response_code != 0:
        raise ValueError(f"Unexpected response_code: {response_code}")

    results = payload["results"]
    return [
        {"text": item["question"], "answer": item["correct_answer"]} for item in results
    ]
