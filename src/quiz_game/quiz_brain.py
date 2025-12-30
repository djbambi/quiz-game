class QuizBrain:
    def __init__(self, question_list: list, input_func=input):
        self.question_number = 0
        self.question_list = question_list
        self._input = input_func

    def next_question(self):
        current_question = self.question_list[self.question_number].text
        self._input(f"Q.1: {current_question} (True/False)?: ")
