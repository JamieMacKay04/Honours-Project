import pandas as pd
import matplotlib.pyplot as plt

# Load local CSV
df = pd.read_csv('stockOrders.csv')

# Ensure correct data types
df['Week'] = df['Week'].astype(int)

# Filter last 10 weeks
latest_weeks = sorted(df['Week'].unique())[-10:]
filtered_df = df[df['Week'].isin(latest_weeks)]

# Line graph for beers
beer_names = ['Bira Moretti', 'Peroni', 'Corona']
beer_df = filtered_df[filtered_df['Item Name'].isin(beer_names)]
beer_pivot = beer_df.pivot_table(index='Week', columns='Item Name', values='Ordered Stock', aggfunc='sum')

plt.figure(figsize=(10, 5))
for beer in beer_names:
    if beer in beer_pivot.columns:
        plt.plot(beer_pivot.index, beer_pivot[beer], label=beer)

plt.title('Beer Orders Over Last 10 Weeks')
plt.xlabel('Week')
plt.ylabel('Ordered Stock')
plt.legend()
plt.grid(True)
plt.savefig('../public/img/beer_trends.png')
plt.close()

# Bar graph for weekly totals
total_order_df = filtered_df.groupby('Week')['Ordered Stock'].sum()

plt.figure(figsize=(10, 5))
total_order_df.plot(kind='bar', color='#c19a6b')
plt.title('Total Stock Ordered Per Week')
plt.xlabel('Week')
plt.ylabel('Total Items Ordered')
plt.grid(axis='y')
plt.savefig('../public/img/weekly_totals.png')
plt.close()
