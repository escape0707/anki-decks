from typing import List


def extract_expressions(expression_field: str) -> List[str]:
    expression_collection = []
    word_start = 0
    word_end = expression_field.find("（")
    while True:
        if word_end == -1:
            word_end = len(expression_field)
        expression_collection.append(expression_field[word_start:word_end])
        word_start = expression_field.find("（", word_end)
        if word_start == -1:
            break
        word_start += 1
        word_end = expression_field.find("）", word_start)
    return expression_collection
