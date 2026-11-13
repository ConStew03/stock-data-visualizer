# Stock Data Visualizer (Project 3a)

A Flask web app that charts stock prices from the [Alpha Vantage](https://www.alphavantage.co/) API. Pick a stock, a chart type, a time series and a date range, press Submit, and the chart appears under the form. The app runs inside a Docker container.

## How to run it

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and open it.
2. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key). A free key allows about 25 lookups a day.
3. In this folder, make a copy of `.env.example`, name the copy `.env`, and replace `paste_your_key_here` with your key. Git ignores `.env`, so your key stays on your computer.
4. Open a terminal in this folder and run:

   ```bash
   docker compose up -d --build
   ```

5. Open http://localhost:5005 in your browser.

To stop the app:

```bash
docker compose down
```

Notes:

- The app uses port 5005 because Macs use port 5000 for AirPlay.
- Code changes show up without rebuilding: the folder is shared with the container, and Flask reloads itself in debug mode.
- If you change `.env`, run `docker compose up -d` again so the container gets the new key.

## Credits

Osteen Katambwa wrote the Project 3 command-line version of this app and the first version of this Flask app.
