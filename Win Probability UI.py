import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# Load data
deliveries_df = pd.read_csv('deliveries.csv')
matches_df = pd.read_csv('matches.csv')

df = matches_df[['id', 'venue', 'team1', 'team2', 'winner']]

first_innings_scores = deliveries_df[deliveries_df['inning'] == 1].groupby('match_id')['total_runs'].sum().reset_index()
first_innings_scores.rename(columns={'total_runs': 'first_innings_score'}, inplace=True)

df = pd.merge(df, first_innings_scores, left_on='id', right_on='match_id', how='left')

df['match_outcome'] = df.apply(lambda row: 1 if row['winner'] == row['team1'] else 0, axis=1)
df = df.dropna(subset=['match_outcome'])
df = df[['venue', 'team1', 'team2', 'first_innings_score', 'match_outcome']]

label_encoder_venue = LabelEncoder()
df['venue_encoded'] = label_encoder_venue.fit_transform(df['venue'])

label_encoder_team = LabelEncoder()
df['team1_encoded'] = label_encoder_team.fit_transform(df['team1'])
df['team2_encoded'] = label_encoder_team.fit_transform(df['team2'])

X = df[['venue_encoded', 'team1_encoded', 'team2_encoded', 'first_innings_score']]
y = df['match_outcome']

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_rf = grid_search.best_estimator_

def predict_win_probability(first_innings_score, venue, team1, team2):
    venue_encoded = label_encoder_venue.transform([venue])[0]
    team1_encoded = label_encoder_team.transform([team1])[0]
    team2_encoded = label_encoder_team.transform([team2])[0]

    input_data = np.array([[venue_encoded, team1_encoded, team2_encoded, first_innings_score]])
    win_probability = best_rf.predict_proba(input_data)[:, 1][0]
    return win_probability

# GUI Setup
class WinProbabilityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cricket Win Probability Predictor")
        self.geometry("600x400")
        self.configure(bg="#1a1a1a")

        # Title Label
        title_label = tk.Label(self, text="Cricket Win Probability Predictor", font=("Helvetica", 18), fg="#ffffff", bg="#1a1a1a")
        title_label.pack(pady=10)

        # Venue Dropdown
        venue_label = tk.Label(self, text="Select Venue:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        venue_label.pack(pady=5)
        self.venue_var = tk.StringVar()
        self.venue_dropdown = ttk.Combobox(self, textvariable=self.venue_var, state="readonly", width=50)
        self.venue_dropdown['values'] = sorted(df['venue'].unique())
        self.venue_dropdown.pack(pady=10)

        # Team 1 Dropdown
        team1_label = tk.Label(self, text="Select Team 1:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        team1_label.pack(pady=5)
        self.team1_var = tk.StringVar()
        self.team1_dropdown = ttk.Combobox(self, textvariable=self.team1_var, state="readonly", width=50)
        self.team1_dropdown['values'] = sorted(df['team1'].unique())
        self.team1_dropdown.pack(pady=10)

        # Team 2 Dropdown
        team2_label = tk.Label(self, text="Select Team 2:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        team2_label.pack(pady=5)
        self.team2_var = tk.StringVar()
        self.team2_dropdown = ttk.Combobox(self, textvariable=self.team2_var, state="readonly", width=50)
        self.team2_dropdown['values'] = sorted(df['team2'].unique())
        self.team2_dropdown.pack(pady=10)

        # First Innings Score Entry
        first_innings_score_label = tk.Label(self, text="Enter First Innings Score:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        first_innings_score_label.pack(pady=5)
        self.first_innings_score_var = tk.StringVar()
        self.first_innings_score_entry = tk.Entry(self, textvariable=self.first_innings_score_var, font=("Helvetica", 12), width=10)
        self.first_innings_score_entry.pack(pady=10)

        # Predict Button
        predict_button = tk.Button(self, text="Predict Win Probability", command=self.predict_win_probability, font=("Helvetica", 12), bg="#4caf50", fg="#ffffff")
        predict_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self, text="", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        self.result_label.pack(pady=10)

    def predict_win_probability(self):
        venue = self.venue_var.get()
        team1 = self.team1_var.get()
        team2 = self.team2_var.get()
        try:
            first_innings_score = int(self.first_innings_score_var.get())
            win_probability = predict_win_probability(first_innings_score, venue, team1, team2)
            self.result_label.config(text=f"Win Probability for {team1}: {win_probability:.2f}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid first innings score.")

if __name__ == "__main__":
    app = WinProbabilityApp()
    app.mainloop()
