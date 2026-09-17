import pandas as pd

df = pd.read_csv('expenses.csv')
print(df.head())             # see your data
print(df['amount'].sum())    # total spent
print(df.groupby('category')['amount'].sum())   # total spent per category
print(df.groupby('category')['amount'].sum().sort_values(ascending=False))  # ranked

df['date'] = pd.to_datetime(df['date'])   # tell pandas this column is a real date
df['day_of_week'] = df['date'].dt.day_name()   # extract the day name
print(df)

print(df.groupby('day_of_week')['amount'].sum().sort_values(ascending=False))

def flag_high_spending(amount):
    if amount >= 3000:
        return "High"
    elif amount >= 1500:
        return "Medium"
    else:
        return "Low"

df['spending_level'] = df['amount'].apply(flag_high_spending)
print(df[['date', 'category', 'amount', 'spending_level']])
print(df['spending_level'].value_counts())

import matplotlib.pyplot as plt

category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(category_totals.index, category_totals.values, color='skyblue')
plt.title('My Spending by Category')
plt.xlabel('Category')
plt.ylabel('Amount Spent (₦)')
plt.tight_layout()
plt.savefig('spending_by_category.png')
print("Chart saved as spending_by_category.png")