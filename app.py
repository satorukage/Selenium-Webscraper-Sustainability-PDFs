from flask import Flask, render_template, request, redirect, url_for, flash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Import Options for headless mode
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for flash messaging

# Dictionary of sectors with their corresponding URLs
sectors = {
    "Agriculture": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=agri",
    "Building and Construction": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=bouw",
    "Business Services": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=zakelijke-dienstverlening",
    "Energy": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=energie",
    "Financials": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=financials",
    "Food and Beverage": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=voeding-en-dranken",
    "ICT": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=ict",
    "Manufacturing": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=productiebedrijven",
    "Packaging": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=packaging",
    "Retail": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=retail",
    "Telecom": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=telecom",
    "Transport": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=telecom",
    "Waste (collection/treatment)": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=afval-inzamelingverwerking",
}

@app.route('/')
def index():
    """Renders the home page with a dropdown for sector selection."""
    return render_template('index.html', sectors=sectors)

@app.route('/scrape', methods=['POST'])
def scrape():
    """Scrapes the selected sector and downloads PDFs."""
    selected_sector = request.form.get('sector')

    if selected_sector in sectors:
        url = sectors[selected_sector]
        # Create a main folder called "sustainability_pdfs"
        main_folder = "sustainability_pdfs"
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        # Set up Selenium options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Required for running in some environments like Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Initialize the web driver in headless mode
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open the URL for the sector
            driver.get(url)

            # Wait for the page to fully load (adjust the sleep time if necessary)
            time.sleep(5)

            # Fetch the page source after it has loaded
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Create a folder for the sector within "sustainability_pdfs"
            sector_folder = os.path.join(main_folder, selected_sector.replace(" ", "_"))
            if not os.path.exists(sector_folder):
                os.makedirs(sector_folder)

            # Find all <a> tags with an href attribute (PDF links)
            pdf_links = soup.find_all('a', href=True)

            # Filter links that contain '.pdf' (even with query params)
            pdf_links = [link['href'] for link in pdf_links if '.pdf' in link['href']]

            # Loop through the filtered PDF links and download each one
            if pdf_links:
                for pdf_url in pdf_links:
                    if not pdf_url.startswith("http"):
                        pdf_url = url + pdf_url

                    pdf_name = pdf_url.split("/")[-1].split("?")[0]  # Extract filename before query params

                    # Download the PDF
                    pdf_response = requests.get(pdf_url)

                    # Save the PDF to the sector folder
                    with open(os.path.join(sector_folder, pdf_name), 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)

            driver.quit()
            flash(f"Scraping for {selected_sector} completed successfully!", "success")
        
        except Exception as e:
            driver.quit()
            flash(f"Error: {str(e)}", "danger")
    
    else:
        flash(f"Invalid sector selected.", "danger")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
