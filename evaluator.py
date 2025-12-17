def evaluate(predicted: str, actual: str):
    return {
        "correct": predicted == actual,
        "predicted": predicted,
        "actual": actual
    }
