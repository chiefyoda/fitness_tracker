import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class FitnessIndicator: 
    def __init__(self, file_location):
        self.file_location = file_location
        self.data = pd.read_csv(self.file_location)

    def calculate_normalize_score(self, score, min_score, max_score):
        normalized_score = int(max(((score - min_score) / (max_score - min_score)), 0) * 100)
        return normalized_score

    def calculate_average_scores(self, *args):
        return round(sum(args) / len(args), 0)

    def process_data(self):
        results = []

        for _, row in self.data.iterrows():
            pull_up_norm = self.calculate_normalize_score(row['pull_up'], 1, 14)
            fivekm_time_norm = self.calculate_normalize_score(row['fivekm_time'], 32.0, 22.5)
            bench_press_norm = self.calculate_normalize_score(row['bench_press'], 47, 98)
            squat_norm = self.calculate_normalize_score(row['squat'], 60, 130)
            overhead_press_norm = self.calculate_normalize_score(row['overhead_press'], 30, 64)

            overall_score = self.calculate_average_scores(
                 pull_up_norm, fivekm_time_norm,
                 bench_press_norm, squat_norm, overhead_press_norm
            )

            results.append({
                'date': row['date'],
                'overall_score': overall_score,
                'pull_up_norm': pull_up_norm,
                'fivekm_time_norm': fivekm_time_norm,
                'bench_press_norm': bench_press_norm,
                'squat_norm': squat_norm,
                'overhead_press_norm': overhead_press_norm,
            })

        return results

    def plot_results(self, results_df):
        data = results_df
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        print(data)
        sns.lineplot(
            data=data[['pull_up_norm',
                       'fivekm_time_norm',
                       'bench_press_norm',
                       'squat_norm',
                       'overhead_press_norm'
                       ]],
                       )

        sns.lineplot(data=data['overall_score'], color='black', linewidth=3, label='Overall Score')

        plt.title('Normalized Fitness Scores Over Time')
        plt.xlabel('Date')
        plt.ylabel('Normalized Score')

        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('plots/fitness_score.png')
        plt.close()

    def run(self):
        results = self.process_data()
        results_df = pd.DataFrame.from_dict(results)
        print(results_df['overall_score'])
        self.plot_results(results_df)


file_location = 'input_pbs.csv'
fitness_indicator = FitnessIndicator(file_location)
fitness_indicator.run()
