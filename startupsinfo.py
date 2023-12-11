from googlesearch import search
import plotly.express as px


class StartupInfo:
    def __init__(self, df):
        self.df = df

    def get_founder(self, startup_name):
        query = f"founder of {startup_name}"
        search_url = 'https://www.google.com/search?&q=' + '+'.join(query.split())
        search_results = []
        search_results.append(search_url)
        # Loop through search results and print the founder name (if found)
        for result in search_results:
            if "founder" in result.lower():
                return result
        return "Founder name not found"



    def get_vertical(self, startup_name):
        vertical = self.df[self.df['startup'] == startup_name]['vertical'].values
        if len(vertical) == 0:
            return 'Not Known'
        else:
            return vertical[0]

    def get_subvertical(self, startup_name):
        subvertical = self.df[self.df['startup'] == startup_name]['subvertical'].values
        if len(subvertical) == 0:
            return 'Not Known'
        else:
            return subvertical[0]

    def get_location(self, startup_name):
        location = self.df[self.df['startup'] == startup_name]['location'].values
        if len(location) == 0:
            return 'Not Known'
        else:
            return location[0]

    def plot_startup_funding(self, startup_name):
        # Filter data for selected startup
        startup_df = self.df[self.df['startup'] == startup_name]

        # Create scatter plot with hover information
        fig13 = px.scatter(startup_df, x='date', y='investor', size='amount', color='investment_type',
                         hover_data={'date': '|%B %d, %Y', 'investor': True, 'investment_type': True, 'amount': ':.2f',
                                     'location': True})

        # Update figure layout
        fig13.update_layout(title=f'Funding details for {startup_name}',
                          xaxis_title='Date', yaxis_title='Investor', legend_title='Investment Type')
        fig13.update_traces(marker=dict(size=25))

        # Return the plot
        return fig13

    def find_similar_startups(self, startup_name, num_similar=6):
        # Get the vertical of the selected startup
        vertical = self.df[self.df['startup'] == startup_name]['vertical'].values[0]

        # Filter the dataset by the same vertical
        vertical_df = self.df[self.df['vertical'] == vertical]

        # Sort the startups by funding amount
        sorted_df = vertical_df.sort_values(by=["amount","subvertical"], ascending=False)
        sorted_df = sorted_df.drop_duplicates(subset='startup',keep='first')

        # Remove the selected startup from the list of similar startups
        similar_startups = sorted_df[sorted_df['startup'] != startup_name]['startup'][:num_similar]
        # Convert the similar startups to a formatted string
        similar_startups_str = ', '.join(list(similar_startups))

        return similar_startups_str
