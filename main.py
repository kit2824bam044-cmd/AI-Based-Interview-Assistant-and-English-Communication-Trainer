import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data.csv")

# Average
avg_scores = data[['Technical', 'Communication', 'Confidence']].mean()
avg_scores.plot(kind='bar')
plt.savefig("output.png")

# Recommendation
def give_recommendation(row):
    if row['Technical'] < 6:
        return "Improve Technical Skills"
    elif row['Communication'] < 6:
        return "Improve Communication"
    elif row['Confidence'] < 6:
        return "Work on Confidence"
    else:
        return "Good Performance"

data['Recommendation'] = data.apply(give_recommendation, axis=1)

print(data)

# 👉 THIS LINE ADD HERE
data.to_csv("output_with_recommendation.csv", index=False)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Input (features)
X = data[['Technical', 'Communication', 'Confidence']]

# Output (target)
y = data['Result']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model create
model = DecisionTreeClassifier()

# Train model
model.fit(X_train, y_train)

# Accuracy check
accuracy = model.score(X_test, y_test)
print("\nModel Accuracy:", accuracy)
# New candidate prediction
new_data = [[6, 7, 6]]  # Technical, Communication, Confidence

prediction = model.predict(new_data)
print("\nNew Candidate Result:", prediction[0])