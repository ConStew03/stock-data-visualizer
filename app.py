from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime
import pygal

# Import your helper functions from stock_visualizer.py
from stock_visualizer import (
    fetch_stock_data,
    filter_and_sort_data
)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Put your Alpha Vantage API key here or load it from an environment variable
ALPHA_VANTAGE_API_KEY = "5VUJVPOP7XNNNDJR"

def load_stock_symbols():
    symbols = []
    csv_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row.get('Symbol') or row.get('symbol')
                if symbol:
                    symbols.append(symbol.strip())
    except FileNotFoundError:
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    return symbols

@app.route('/', methods=['GET', 'POST'])
def index():
    symbols = load_stock_symbols()
    chart_svg = None
    
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        chart_type = request.form.get('chart_type') # '1' for Line, '2' for Bar
        time_series_choice = request.form.get('time_series') # '1', '2', or '3'
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        # Validation checks
        if not symbol:
            flash("Please select a stock symbol.")
            return redirect(url_for('index'))
            
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if end_date <= start_date:
                flash("Error: End Date must be strictly after Start Date.")
                return redirect(url_for('index'))
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('index'))
            
        # Map time series selection to Alpha Vantage parameters
        mapping = {
            "1": ("TIME_SERIES_DAILY", "Time Series (Daily)"),
            "2": ("TIME_SERIES_WEEKLY", "Weekly Time Series"),
            "3": ("TIME_SERIES_MONTHLY", "Monthly Time Series")
        }
        func_name, time_series_key = mapping.get(time_series_choice, mapping["1"])
        
        # Fetch data using your existing function
        raw_data = fetch_stock_data(symbol, func_name, ALPHA_VANTAGE_API_KEY)
        print("DEBUG RAW DATA:", raw_data)
        
        if not raw_data or time_series_key not in raw_data:
            flash("Failed to retrieve data from Alpha Vantage. Check API key or ticker limit.")
            return redirect(url_for('index'))
            
        # Filter and sort data using your existing function
        dates, open_p, high_p, low_p, close_p = filter_and_sort_data(
            raw_data, time_series_key, start_date, end_date
        )
        
        if not dates:
            flash("No data found for the selected date range.")
            return redirect(url_for('index'))
            
        # Generate Pygal chart as SVG string instead of file/browser
        chart = pygal.Line(x_label_rotation=45) if chart_type == "1" else pygal.Bar(x_label_rotation=45)
        chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
        chart.x_labels = dates

        chart.add("Open", open_p)
        chart.add("High", high_p)
        chart.add("Low", low_p)
        chart.add("Close", close_p)

        chart_svg = chart.render(is_unicode=True)

    return render_template('index.html', symbols=symbols, chart_svg=chart_svg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)