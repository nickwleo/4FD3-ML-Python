import random
import pandas as pd

# Number of data samples and topics
num_samples = 1000
num_topics = 10

def adjust_recommendations(recommendations):
    total_questions = sum(recommendations.values())
    while total_questions != 20:
        for topic, count in recommendations.items():
            if total_questions > 20 and count > 2:
                recommendations[topic] -= 1
                total_questions -= 1
            elif total_questions < 20:
                recommendations[topic] += 1
                total_questions += 1
            if total_questions == 20:
                break
    return recommendations

data = []
for _ in range(num_samples):
    # Simulate random performance for each topic (0 to 100%)
    performance = {f"topic_{i}": random.uniform(0, 100) for i in range(num_topics)}

    # Generating recommendations based on performance
    recommendations = {}
    for topic, score in performance.items():
        if score < 40:
            recommendations[topic] = 4  # More questions if performance is low
        elif score < 70:
            recommendations[topic] = 3  # Moderate number of questions
        else:
            recommendations[topic] = 1  # Fewer questions if performance is high

    # Adjust recommendations to sum up to 20 questions
    recommendations = adjust_recommendations(recommendations)

    data.append({**performance, **recommendations})

# Convert to DataFrame for easier manipulation and visualization
df = pd.DataFrame(data)

# Save the generated data to 'generated_data.csv'
df.to_csv('generated_data.csv', index=False)  # index=False to exclude the index column

# Displaying the first few rows of the dataset
print(df.head())
