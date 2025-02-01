import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Load data
df = pd.read_csv('matches.csv')
fd = pd.read_csv('deliveries.csv')

# Merge and process data
data = pd.merge(fd, df[['id', 'venue']], left_on='match_id', right_on='id')
venue_stats = data.groupby(['venue', 'inning']).agg({
    'total_runs': 'sum',
    'player_dismissed': 'count'
}).reset_index()

first_innings_stats = venue_stats[venue_stats['inning'] == 1]
second_innings_stats = venue_stats[venue_stats['inning'] == 2]

combined_stats = pd.merge(first_innings_stats, second_innings_stats, on='venue', suffixes=('_1st', '_2nd'))

combined_stats['batting_friendly_score'] = (combined_stats['total_runs_1st'] + combined_stats['total_runs_2nd']) / 2
combined_stats['bowling_friendly_score'] = (combined_stats['player_dismissed_1st'] + combined_stats['player_dismissed_2nd']) / 2

def pitch_type(row):
    if row['batting_friendly_score'] > row['bowling_friendly_score']:
        return 'Batting Friendly'
    else:
        return 'Bowling Friendly'

combined_stats['pitch_type'] = combined_stats.apply(pitch_type, axis=1)

def get_pitch_type(venue):
    result = combined_stats[combined_stats['venue'] == venue]
    if not result.empty:
        return result.iloc[0]['pitch_type']
    else:
        return 'Stadium not found in the dataset'

# Get the unique stadium names and their maximum length
stadium_names = combined_stats['venue'].unique()
max_length_venue = max(len(venue) for venue in stadium_names)

# GUI Setup
class PitchTypeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cricket Pitch Type Analyzer")
        self.geometry("500x300")
        self.configure(bg="#1a1a1a")

        # Title Label
        title_label = tk.Label(self, text="Cricket Pitch Type Analyzer", font=("Helvetica", 18), fg="#ffffff", bg="#1a1a1a")
        title_label.pack(pady=10)

        # Dropdown Label
        dropdown_label = tk.Label(self, text="Select Stadium:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        dropdown_label.pack(pady=5)

        # Dropdown
        venue_label = tk.Label(self, text="Select Venue:", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        venue_label.pack(pady=5)
        self.venue_var = tk.StringVar()
        self.venue_dropdown = ttk.Combobox(self, textvariable=self.venue_var, state="readonly", width=50)
        self.venue_dropdown['values'] = sorted(df['venue'].unique())
        self.venue_dropdown.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self, text="", font=("Helvetica", 14), fg="#ffffff", bg="#1a1a1a")
        self.result_label.pack(pady=10)

        # Check Button
        check_button = tk.Button(self, text="Check Pitch Type", command=self.check_pitch_type, font=("Helvetica", 12), bg="#4caf50", fg="#ffffff")
        check_button.pack(pady=10)

    def check_pitch_type(self):
        venue = self.venue_var.get()
        if venue:
            pitch_type = get_pitch_type(venue)
            self.result_label.config(text=f"Pitch Type at {venue}: {pitch_type}")
        else:
            messagebox.showwarning("Input Error", "Please select a stadium.")

if __name__ == "__main__":
    app = PitchTypeApp()
    app.mainloop()
