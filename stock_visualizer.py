import datetime
import json
import urllib.parse
import urllib.request
import webbrowser
import pygal


def get_api_key():
    key = input("Enter your Alpha Vantage API Key: ").strip()
    while not key:
        key = input("API Key cannot be empty. Enter Alpha Vantage API Key: ").strip()
    return key


def get_stock_symbol():
    symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").strip().upper()
    while not symbol:
        symbol = input("Stock symbol cannot be empty. Enter stock symbol: ").strip().upper()
    return symbol


def get_chart_type():
    print("\nChart Types:")
    print("1. Line")
    print("2. Bar")
    choice = input("Select chart type (1 or 2): ").strip()
    while choice not in ["1", "2"]:
        choice = input("Invalid choice. Enter 1 for Line or 2 for Bar: ").strip()
    return choice


def get_time_series_function():
    print("\nTime Series Options:")
    print("1. TIME_SERIES_DAILY")
    print("2. TIME_SERIES_WEEKLY")
    print("3. TIME_SERIES_MONTHLY")
    choice = input("Select time series function (1-3): ").strip()
    
    mapping = {
        "1": ("TIME_SERIES_DAILY", "Time Series (Daily)"),
        "2": ("TIME_SERIES_WEEKLY", "Weekly Time Series"),
        "3": ("TIME_SERIES_MONTHLY", "Monthly Time Series")
    }
    while choice not in mapping:
        choice = input("Invalid choice. Select 1, 2, or 3: ").strip()
    return mapping[choice]


def get_date(prompt_text):
    while True:
        date_str = input(prompt_text).strip()
        try:
            valid_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            print("Invalid format. Please enter date as YYYY-MM-DD.")


def get_date_range():
    print("\nEnter Date Range:")
    start_date = get_date("Enter beginning date (YYYY-MM-DD): ")
    while True:
        end_date = get_date("Enter end date (YYYY-MM-DD): ")
        if end_date >= start_date:
            return start_date, end_date
        print("Error: End date cannot be before start date.")


def fetch_stock_data(symbol, function_name, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": function_name,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    print("\nFetching data from Alpha Vantage...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return None


def filter_and_sort_data(raw_data, time_series_key, start_date, end_date):
    if time_series_key not in raw_data:
        print("\nError fetching data. Response details:")
        print(json.dumps(raw_data, indent=2))
        return [], [], [], [], []

    time_series = raw_data[time_series_key]
    dates, open_prices, high_prices, low_prices, close_prices = [], [], [], [], []

    # Sort dates chronologically
    sorted_dates = sorted(time_series.keys())

    for date_str in sorted_dates:
        current_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if start_date <= current_date <= end_date:
            day_data = time_series[date_str]
            dates.append(date_str)
            open_prices.append(float(day_data["1. open"]))
            high_prices.append(float(day_data["2. high"]))
            low_prices.append(float(day_data["3. low"]))
            close_prices.append(float(day_data["4. close"]))

    return dates, open_prices, high_prices, low_prices, close_prices


def generate_chart(symbol, chart_type, dates, open_prices, high_prices, low_prices, close_prices, start_date, end_date):
    chart = pygal.Line(x_label_rotation=45) if chart_type == "1" else pygal.Bar(x_label_rotation=45)
    chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
    chart.x_labels = dates

    chart.add("Open", open_prices)
    chart.add("High", high_prices)
    chart.add("Low", low_prices)
    chart.add("Close", close_prices)

    filename = f"{symbol}_chart.html"
    chart.render_to_file(filename)
    print(f"\nChart saved to {filename}. Opening in default browser...")
    webbrowser.open(filename)


def main():
    print("=" * 50)
    print("     ALPHA VANTAGE STOCK DATA VISUALIZER     ")
    print("=" * 50)

    api_key = get_api_key()
    symbol = get_stock_symbol()
    chart_type = get_chart_type()
    func_name, time_series_key = get_time_series_function()
    start_date, end_date = get_date_range()

    raw_data = fetch_stock_data(symbol, func_name, api_key)
    if not raw_data:
        return

    dates, open_p, high_p, low_p, close_p = filter_and_sort_data(
        raw_data, time_series_key, start_date, end_date
    )

    if not dates:
        print("\nNo data found for the selected date range.")
        return

    generate_chart(symbol, chart_type, dates, open_p, high_p, low_p, close_p, start_date, end_date)


if __name__ == "__main__":
    main()