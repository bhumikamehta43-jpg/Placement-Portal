
from modules.mock_test import QUESTION_BANK, evaluate_answers


def test_question_bank_has_questions():
    assert QUESTION_BANK

    for subject, questions in QUESTION_BANK.items():
        assert questions, f"{subject} has no questions"

        for question in questions:
            assert "question" in question
            assert "options" in question
            assert "answer" in question
            assert question["answer"] in question["options"]


def test_all_correct_answers():
    subject = next(iter(QUESTION_BANK))
    questions = QUESTION_BANK[subject]

    answers = {
        str(index): question["answer"]
        for index, question in enumerate(questions)
    }

    result = evaluate_answers(subject, answers)

    assert result["correct_answers"] == len(questions)
    assert result["wrong_answers"] == 0
    assert result["score_percent"] == 100.0


def test_all_wrong_answers():
    subject = next(iter(QUESTION_BANK))
    questions = QUESTION_BANK[subject]

    answers = {
        str(index): "__definitely_wrong_answer__"
        for index, question in enumerate(questions)
    }

    result = evaluate_answers(subject, answers)

    assert result["correct_answers"] == 0
    assert result["wrong_answers"] == len(questions)
    assert result["score_percent"] == 0.0


def test_unanswered_questions():
    subject = next(iter(QUESTION_BANK))

    result = evaluate_answers(subject, {})

    assert result["correct_answers"] == 0
    assert result["wrong_answers"] == len(QUESTION_BANK[subject])
    assert result["score_percent"] == 0.0
