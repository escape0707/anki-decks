from collections import Counter
from typing import List


def extract_expressions(expression_field: str) -> List[str]:
    expression_counter = Counter[str]()
    word_start = 0
    word_end = expression_field.find("（")
    while True:
        if word_end == -1:
            word_end = len(expression_field)
        expression = expression_field[word_start:word_end]
        expression_counter[expression] += 1
        word_start = expression_field.find("（", word_end)
        if word_start == -1:
            break
        word_start += 1
        word_end = expression_field.find("）", word_start)

    expression_collection = []
    for expression, cnt in expression_counter.items():
        if cnt == 1:
            expression_collection.append(expression)
        else:
            expression_collection.extend(f"{expression}_{i}" for i in range(1, cnt + 1))
    return expression_collection
