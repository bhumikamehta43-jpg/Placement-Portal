
QUESTION_BANK = {
    "DSA": [
        {
            "question": "Which data structure follows LIFO?",
            "options": ["Queue", "Stack", "Tree", "Graph"],
            "answer": "Stack",
            "explanation": "Stack follows Last In, First Out."
        },
        {
            "question": "What is the average time complexity of binary search?",
            "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
            "answer": "O(log n)",
            "explanation": "Binary search halves the search space each step."
        },
        {
            "question": "Which data structure uses FIFO?",
            "options": ["Stack", "Queue", "Heap", "Graph"],
            "answer": "Queue",
            "explanation": "Queue follows First In, First Out."
        }
    ],
    "DBMS": [
        {
            "question": "Which key uniquely identifies a row?",
            "options": ["Foreign key", "Primary key", "Duplicate key", "None"],
            "answer": "Primary key",
            "explanation": "A primary key uniquely identifies each row."
        },
        {
            "question": "Which SQL command retrieves data?",
            "options": ["SELECT", "UPDATE", "DELETE", "DROP"],
            "answer": "SELECT",
            "explanation": "SELECT retrieves data from a table."
        },
        {
            "question": "Which normal form removes partial dependency?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": "2NF",
            "explanation": "Second Normal Form removes partial dependency."
        }
    ],
    "Operating Systems": [
        {
            "question": "Which is responsible for process scheduling?",
            "options": ["Compiler", "Operating system", "Browser", "Database"],
            "answer": "Operating system",
            "explanation": "The OS schedules processes for CPU execution."
        },
        {
            "question": "Which is a necessary condition for deadlock?",
            "options": ["Mutual exclusion", "Compilation", "Indexing", "Paging only"],
            "answer": "Mutual exclusion",
            "explanation": "Mutual exclusion is one of the four deadlock conditions."
        },
        {
            "question": "What does RAM provide?",
            "options": ["Permanent storage", "Temporary working memory", "Printing", "Networking only"],
            "answer": "Temporary working memory",
            "explanation": "RAM stores data temporarily while programs run."
        }
    ],
    "Computer Networks": [
        {
            "question": "Which protocol reliably delivers ordered data?",
            "options": ["UDP", "TCP", "ARP", "ICMP"],
            "answer": "TCP",
            "explanation": "TCP provides reliable, ordered delivery."
        },
        {
            "question": "What does DNS translate?",
            "options": ["Domain names to IP addresses", "Text to images", "Files to folders", "RAM to ROM"],
            "answer": "Domain names to IP addresses",
            "explanation": "DNS resolves domain names to IP addresses."
        },
        {
            "question": "Which device forwards packets between networks?",
            "options": ["Keyboard", "Router", "Monitor", "Scanner"],
            "answer": "Router",
            "explanation": "Routers forward packets between networks."
        }
    ],
    "OOP": [
        {
            "question": "Which concept bundles data and methods?",
            "options": ["Encapsulation", "Compilation", "Iteration", "Indexing"],
            "answer": "Encapsulation",
            "explanation": "Encapsulation bundles data and related methods."
        },
        {
            "question": "Which concept allows a class to inherit another class?",
            "options": ["Inheritance", "Recursion", "Sorting", "Abstraction only"],
            "answer": "Inheritance",
            "explanation": "Inheritance allows a class to reuse another class's features."
        },
        {
            "question": "Which concept means one interface can have different implementations?",
            "options": ["Polymorphism", "Normalization", "Deadlock", "Paging"],
            "answer": "Polymorphism",
            "explanation": "Polymorphism allows the same interface to behave differently."
        }
    ]
}


def evaluate_answers(subject, selected_answers):
    questions = QUESTION_BANK[subject]
    total_questions = len(questions)
    correct_answers = 0
    results = []

    for index, question in enumerate(questions):
        selected = selected_answers.get(str(index))
        correct = question["answer"]
        is_correct = selected == correct

        if is_correct:
            correct_answers += 1

        results.append({
            "question": question["question"],
            "selected": selected if selected else "Not answered",
            "correct": correct,
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })

    wrong_answers = total_questions - correct_answers
    score_percent = round(
        (correct_answers / total_questions) * 100, 2
    )

    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "score_percent": score_percent,
        "results": results
    }
