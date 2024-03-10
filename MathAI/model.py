# model.py
import numpy as np
from sklearn.linear_model import LinearRegression


def adjust_question_distribution(data):
    topics = ["0", "1", "2", "3", "4"]
    scores = {topic: [] for topic in topics}
    rounds = np.array(range(1, len(data) + 1))
    total_questions = 20

    if len(data) == 1:
        return distribute_questions_based_on_single_round(data[0], topics, total_questions)

    # Apply more weight to the last three rounds
    weights = np.ones(len(data))
    if len(data) > 3:
        weights[-3:] = np.linspace(2, 3, num=3)

    slopes = {}
    recent_performance = {}
    for topic in topics:
        y = np.array([entry[topic] for entry in data])
        model = LinearRegression()
        model.fit(rounds.reshape(-1, 1), y, sample_weight=weights)
        slopes[topic] = model.coef_[0]
        recent_performance[topic] = y[
            -1
        ]  # Get the most recent performance for each topic

    # Adjust the performance factors based on slopes and recent performance
    performance_factors = {}
    for topic, slope in slopes.items():
        # Adjust factor based on slope and performance
        if recent_performance[topic] < 50:
            factor = 2
        elif recent_performance[topic] >= 80:
            factor = 0.5
        else:
            factor = 1
        performance_factors[topic] = slope * factor

    # Normalize performance factors to determine the question distribution
    total_factor = sum(abs(f) for f in performance_factors.values())
    adjusted_questions = {
        topic: max(
            1, round((abs(performance_factors[topic]) / total_factor) * total_questions)
        )
        for topic in topics
    }

    # Ensure total questions sum to exactly 20, adjust if necessary
    adjust_distribution_to_total_questions(adjusted_questions, total_questions)

    return adjusted_questions

def distribute_questions_based_on_single_round(single_round_data, topics, total_questions):
    # Sort topics by performance from worst to best
    sorted_topics = sorted(single_round_data.items(), key=lambda item: item[1])
    
    # Calculate the inverse performance to prioritize lower scores with more questions
    inverse_performance_scores = {topic: (100 - performance) for topic, performance in sorted_topics}
    total_inverse_performance = sum(inverse_performance_scores.values())
    
    # Initialize distribution
    adjusted_questions = {}

    if total_inverse_performance == 0:  # Avoid division by zero if all performances are 100
        equal_distribution = total_questions // len(topics)
        adjusted_questions = {topic: equal_distribution for topic, _ in sorted_topics}
        remaining_questions = total_questions - (equal_distribution * len(topics))
        for topic in adjusted_questions.keys():
            if remaining_questions > 0:
                adjusted_questions[topic] += 1
                remaining_questions -= 1
            else:
                break
    else:
        # Distribute questions based on the inverse performance percentage
        for topic, score in inverse_performance_scores.items():
            performance_percentage = score / total_inverse_performance
            adjusted_questions[topic] = round(performance_percentage * total_questions)
        
        # Adjust the distribution to ensure the total is exactly total_questions
        adjust_distribution_to_total_questions(adjusted_questions, total_questions)
    
    return adjusted_questions

def adjust_distribution_to_total_questions(adjusted_questions, total_questions):
    question_sum = sum(adjusted_questions.values())
    while question_sum != total_questions:
        for topic in sorted(adjusted_questions, key=adjusted_questions.get):
            if question_sum < total_questions:
                adjusted_questions[topic] += 1
                question_sum += 1
            elif question_sum > total_questions and adjusted_questions[topic] > 1:
                adjusted_questions[topic] -= 1
                question_sum -= 1
            if question_sum == total_questions:
                break


# This function is just for debugging.
if __name__ == "__main__":
    sample_data = [
        {"0": 80, "1": 50, "2": 60, "3": 40, "4": 90},
        {"0": 85, "1": 55, "2": 65, "3": 45, "4": 95},
        {"0": 80, "1": 40, "2": 60, "3": 35, "4": 90},
    ]
    print(adjust_question_distribution(sample_data))
