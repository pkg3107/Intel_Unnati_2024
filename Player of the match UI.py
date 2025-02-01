import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox, simpledialog

# Load the data
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Merge data using 'id' from matches and 'match_id' from deliveries
data = pd.merge(deliveries, matches[['id', 'player_of_match']], left_on='match_id', right_on='id')

# Filter necessary columns for analysis
match_data = data[['match_id', 'player_of_match', 'batsman', 'bowler', 'batsman_runs', 'total_runs', 'player_dismissed', 'dismissal_kind']]

# Calculate strike rate and economy rate for batsmen
batsman_stats = match_data.groupby(['match_id', 'batsman'])['batsman_runs'].agg(['sum', 'count']).reset_index()
batsman_stats['strike_rate'] = (batsman_stats['sum'] / batsman_stats['count']) * 100
batsman_stats.rename(columns={'sum': 'total_runs', 'count': 'balls_faced'}, inplace=True)

# Calculate runs conceded and economy rate for bowlers
bowler_stats = match_data.groupby(['match_id', 'bowler'])['total_runs'].agg(['sum', 'count']).reset_index()
bowler_stats['wickets'] = match_data[match_data['player_dismissed'].notnull()].groupby(['match_id', 'bowler']).size().reset_index(name='wickets')['wickets']
bowler_stats['economy_rate'] = (bowler_stats['sum'] / (bowler_stats['count'] / 6))
bowler_stats.rename(columns={'sum': 'runs_conceded', 'count': 'balls_bowled'}, inplace=True)

# Merge batsman and bowler stats, ensuring 'player_of_match' is included
player_stats = pd.merge(batsman_stats, bowler_stats, left_on=['match_id', 'batsman'], right_on=['match_id', 'bowler'], how='outer')
player_stats = pd.merge(player_stats, matches[['id', 'player_of_match']], left_on='match_id', right_on='id', how='left')  # Merge to include 'player_of_match'
player_stats = player_stats.fillna(0)

# Assign target variable
player_stats['is_player_of_match'] = player_stats.apply(lambda row: 1 if row['batsman'] == row['player_of_match'] else 0, axis=1)

# Drop unnecessary columns
player_stats = player_stats.drop(columns=['batsman', 'bowler', 'player_of_match', 'id'])  # Also drop the 'id' column

# Final dataset
X = player_stats[['strike_rate', 'economy_rate', 'wickets', 'total_runs', 'balls_faced', 'runs_conceded', 'balls_bowled']]
y = player_stats['is_player_of_match']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the model (Random Forest Classifier)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the Random Forest Classifier model: {accuracy:.2f}")

# Function to check the accuracy for a specific match
def check_match_accuracy(match_id):
    match_data = data[data['match_id'] == match_id]
    if match_data.empty:
        return f"No data available for match ID {match_id}"

    # Calculate strike rate and economy rate for the specific match
    batsman_stats = match_data.groupby(['match_id', 'batsman'])['batsman_runs'].agg(['sum', 'count']).reset_index()
    batsman_stats['strike_rate'] = (batsman_stats['sum'] / batsman_stats['count']) * 100
    batsman_stats.rename(columns={'sum': 'total_runs', 'count': 'balls_faced'}, inplace=True)

    bowler_stats = match_data.groupby(['match_id', 'bowler'])['total_runs'].agg(['sum', 'count']).reset_index()
    bowler_stats['wickets'] = match_data[match_data['player_dismissed'].notnull()].groupby(['match_id', 'bowler']).size().reset_index(name='wickets')['wickets']
    bowler_stats['economy_rate'] = (bowler_stats['sum'] / (bowler_stats['count'] / 6))
    bowler_stats.rename(columns={'sum': 'runs_conceded', 'count': 'balls_bowled'}, inplace=True)

    # Merge batsman and bowler stats for the specific match
    match_stats = pd.merge(batsman_stats, bowler_stats, left_on=['match_id', 'batsman'], right_on=['match_id', 'bowler'], how='outer').fillna(0)

    # Prepare input data for prediction
    X_match = match_stats[['strike_rate', 'economy_rate', 'wickets', 'total_runs', 'balls_faced', 'runs_conceded', 'balls_bowled']]

    # Predict using the model
    y_match_pred = model.predict(X_match)
    match_stats['predicted_is_player_of_match'] = y_match_pred

    # Actual player of the match
    actual_player_of_match = matches[matches['id'] == match_id]['player_of_match'].values[0]

    # Return result with explanation
    predicted_players = match_stats[match_stats['predicted_is_player_of_match'] == 1]['batsman'].values
    if actual_player_of_match in predicted_players:
        result = {
            'match_id': match_id,
            'actual_player': actual_player_of_match,
            'predicted_players': predicted_players.tolist()  # Convert NumPy array to list
        }
        return result
    else:
        return f"No predicted player of the match for match ID {match_id}. This could be due to insufficient data or the model's inability to confidently predict a player of the match for this particular match."

# Create the UI
class PlayerOfMatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Player of the Match Predictor")

        self.label = tk.Label(root, text="Enter Match ID:")
        self.label.pack(pady=10)

        self.match_id_entry = tk.Entry(root)
        self.match_id_entry.pack(pady=5)

        self.check_button = tk.Button(root, text="Check Accuracy", command=self.check_accuracy)
        self.check_button.pack(pady=10)

        self.result_text = tk.Text(root, height=15, width=50)
        self.result_text.pack(pady=10)

    def check_accuracy(self):
        match_id = self.match_id_entry.get()
        try:
            match_id = int(match_id)
            result = check_match_accuracy(match_id)
            self.result_text.delete(1.0, tk.END)  # Clear the text box

            if isinstance(result, dict):
                self.result_text.insert(tk.END, f"Match ID: {result['match_id']}\n")
                self.result_text.insert(tk.END, f"Actual Player of the Match: {result['actual_player']}\n")
                self.result_text.insert(tk.END, "Predicted Players of the Match:\n")
                for player in result['predicted_players']:
                    self.result_text.insert(tk.END, f"{player}\n")
            else:
                self.result_text.insert(tk.END, result)  # If result is a string (error message), print it

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid match ID.")

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerOfMatchApp(root)
    root.mainloop()
