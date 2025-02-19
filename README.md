# Sustainability Reports Web Scraper

## Overview
This is a Flask-based web scraper designed to collect sustainability reports (PDFs) from [sustainability-reports.com](https://www.sustainability-reports.com/). The scraper allows users to select a sector and automatically download available PDF reports related to that sector.

## Features
- Web-based interface using Flask
- Selenium-powered scraping for dynamic content
- BeautifulSoup for parsing HTML
- Automatic downloading of sustainability PDFs
- Organized storage by sector

## Prerequisites
Ensure you have the following installed on your system:

- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Flask
- Selenium
- BeautifulSoup
- Requests

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/sustainability-pdf-scraper.git
   cd sustainability-pdf-scraper
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Download and install ChromeDriver:
   - Check your Chrome version: `chrome://settings/help`
   - Download the corresponding ChromeDriver from [here](https://sites.google.com/chromium.org/driver/)
   - Place it in a directory included in your system `PATH`.

## Usage
1. Run the Flask app:
   ```sh
   python app.py
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
3. Select a sector from the dropdown list and start scraping.
4. The downloaded PDFs will be saved in the `sustainability_pdfs` directory, organized by sector.

## Folder Structure
```
├── sustainability_pdfs/      # Folder where downloaded PDFs are stored
│   ├── Agriculture/
│   ├── Energy/
│   ├── Retail/
│   ├── ...
├── templates/
│   ├── index.html            # HTML template for the web UI
├── app.py                    # Flask web scraper application
├── requirements.txt          # Required dependencies
├── README.md                 # Documentation
```

## Notes
- The script runs Chrome in headless mode to improve performance.
- Some websites may block automated scraping; consider adding headers or using proxies if needed.
- Increase `time.sleep()` if pages take longer to load.

## License
This project is licensed under the MIT License. Feel free to modify and distribute.

## Author
[Sabry Aboud](https://github.com/satorukage)

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

