from typing import List


def count_unique_group_questions(group_questions: str) -> int:
    bag_of_questions = set()
    for question in group_questions:
        bag_of_questions.add(question)
    return len(bag_of_questions)


def count_common_group_questions(user_questions: List[str]) -> int:
    bags_of_user_questions = []
    for questions in user_questions:
        bag_of_questions = set()
        for question in questions:
            bag_of_questions.add(question)
        bags_of_user_questions.append(bag_of_questions)
    return len(set.intersection(*bags_of_user_questions))


with open('input_6.txt', 'r') as f:
    data = "".join(f.readlines())
    entries = data.split('\n\n')
    all_unique_questions = 0
    all_common_questions = 0
    for entry in entries:
        all_unique_questions += count_unique_group_questions(entry.strip().replace("\n", ""))
        all_common_questions += count_common_group_questions(entry.strip().split("\n"))
    print("Unique group questions = {}".format(all_unique_questions))
    print("Common group questions = {}".format(all_common_questions))
