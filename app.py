from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv('expenses.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()

    total_spent = df['amount'].sum()
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    day_totals = df.groupby('day_of_week')['amount'].sum().sort_values(ascending=False)

    top_category = category_totals.index[0]
    top_day = day_totals.index[0]

    def classify(amount):
        if amount >= 3000:
            return "High"
        elif amount >= 1500:
            return "Medium"
        else:
            return "Low"

    df['spending_level'] = df['amount'].apply(classify)
    transactions = df[['date', 'category', 'description', 'amount', 'spending_level']].to_dict('records')

    plt.figure(figsize=(8, 5))
    plt.bar(category_totals.index, category_totals.values, color='skyblue')
    plt.title('My Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent (₦)')
    plt.tight_layout()
    plt.savefig('static/spending_by_category.png')
    plt.close()

    return render_template(
        'index.html',
        total_spent=total_spent,
        category_totals=category_totals.to_dict(),
        day_totals=day_totals.to_dict(),
        top_category=top_category,
        top_day=top_day,
        transactions=transactions
    )

if __name__ == '__main__':
    app.run(debug=True)