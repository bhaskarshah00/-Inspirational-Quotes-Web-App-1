# QuoteWave 🌊

A beautiful and resilient web application that delivers daily inspiration through random quotes, quote of the day, and aesthetic background images. Powered by a robust Flask backend with smart retries, caching, and offline fallback capabilities.

![QuoteWave Screenshot]QuoteWave Screenshot.png) 


## ✨ Features

- **📜 Smart Quote Fetching**: Retrieves quotes from multiple APIs (ZenQuotes, Quotable) with automatic fallback if one fails.
- **🌅 Beautiful Images**: Proxies and displays high-quality background images from various sources without CORS issues.
- **💪 Offline Resilience**: Serves cached quotes and placeholder images even when external APIs are down or you're offline.
- **🎨 Elegant UI**: Clean, modern glass-morphism design with light/dark mode toggle.
- **🔧 User Control**: Choose preferred sources for quotes and images.
- **📤 Share & Export**: Copy quotes, tweet them directly, or download the quote card as a PNG image.
- **⚡ Fast & Lightweight**: Built with Flask and vanilla JS, ensuring quick load times.

## 🚀 Live Demo

[Check out the live application here!](https://your-render-heroku-link-here.herokuapp.com/) 
*[Replace with your actual deployment link]*

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Bootstrap 5, Custom CSS
- **Image Processing**: html2canvas (for PNG export)
- **Deployment**: Ready for Render, Heroku, or any WSGI-compatible host

## 📦 Installation & Local Setup

Follow these steps to run QuoteWave locally on your machine.

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/quotewave.git
    cd quotewave
    ```

2.  **Create a virtual environment and activate it**
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    python app.py
    ```
    The app will be available at `http://127.0.0.1:5000`.

## 🎯 How to Use

1.  **Get a Random Quote**: Click the "🎲 Random" button.
2.  **Get Today's Quote**: Click the "☀️ Today" button.
3.  **Change Background**: Click the "🖼️ New Image" button.
4.  **Select Sources**: Use the dropdown menus to choose your preferred quote and image sources.
5.  **Share Quotes**: Use the "Copy" or "Tweet" buttons to share your favorite quotes.
6.  **Download**: Click "Download as PNG" to save the quote card as an image.
7.  **Toggle Theme**: Switch between light and dark mode using the moon button in the navbar.

## 🔌 API Endpoints

QuoteWave provides a simple API:

- `GET /api/random` - Fetches a random quote. Query Param: `?source=zenquotes|quotable|auto`
- `GET /api/today` - Fetches the quote of the day. Query Param: `?source=zenquotes_today|quotable|auto`
- `GET /api/image` - Proxies an image from the configured sources. Query Param: `?source=zenquotes_image|picsum|auto`
- `GET /health` - Health check endpoint.
- `GET /api/debug` - Returns debug information about current cache and sources.

## 🌐 Deployment

### Deploy to Render (Recommended)
1.  Fork this repository.
2.  Create a new Web Service on Render and connect your GitHub account.
3.  Select your forked repository.
4.  Use the following build settings:
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app`
5.  Click "Create Web Service". Your app will be deployed automatically.

### Deploy to Heroku
Use the provided Procfile. Run the following commands:
```bash
heroku create your-app-name
git push heroku main
heroku open
