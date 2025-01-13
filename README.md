# Tailwind UI Scraper

A powerful and efficient scraping tool designed to extract component information and code samples from Tailwind UI's component library. This tool helps developers analyze and learn from Tailwind UI's design patterns and implementation techniques.

## ⚠️ Disclaimer

This tool is intended for educational purposes only. Please ensure you comply with Tailwind UI's terms of service and obtain proper licenses for any components you plan to use in production.

## 🚀 Features

- Automated extraction of component markup and styles
- Clean output format for easy analysis
- Support for different component categories (marketing, application UI, ecommerce)
- Configurable scraping parameters
- Rate limiting to prevent server overload
- Export options (JSON, HTML, Markdown)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (based on your browser choice)
- A valid Tailwind UI license (for accessing content)

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tailwind-ui-scraper.git

# Navigate to project directory
cd tailwind-ui-scraper

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Required Python packages (requirements.txt):

```
selenium>=4.0.0
webdriver-manager
python-dotenv
beautifulsoup4
requests
rich  # for better console output
```

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
TAILWIND_UI_EMAIL=your-email@example.com
TAILWIND_UI_PASSWORD=your-password
BROWSER_TYPE=chrome  # or firefox
HEADLESS=true  # set to false for visible browser automation
SCROLL_PAUSE_TIME=2  # pause time between scrolls in seconds
SCREENSHOT_PATH=./screenshots  # path to save component screenshots
```

### WebDriver Setup

The script uses `webdriver-manager` to automatically handle driver installation, but you can also manually set up your preferred WebDriver:

- ChromeDriver: [Download here](https://sites.google.com/chromium.org/driver/)
- GeckoDriver: [Download here](https://github.com/mozilla/geckodriver/releases)

Make sure the WebDriver is in your system PATH or specify its location in the configuration.

## 📝 Usage

```bash
# Run the scraper with default settings
python scraper.py

# Scrape specific categories
python scraper.py --category marketing

# Export to specific format
python scraper.py --export json

# Run in visible browser mode
python scraper.py --no-headless

# Specify custom screenshot directory
python scraper.py --screenshots-dir ./my-screenshots
```

### Example Selenium Code

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    if os.getenv('HEADLESS', 'true').lower() == 'true':
        options.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_component(driver, url):
    driver.get(url)

    # Wait for component to load
    wait = WebDriverWait(driver, 10)
    component = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.preview-component')
    ))

    # Extract component code
    code_block = driver.find_element(By.CSS_SELECTOR, 'pre code')
    return code_block.get_attribute('textContent')
```

## 🔍 Output Structure

The scraper generates organized output in your chosen format:

```
output/
  ├── components/
  │   ├── marketing/
  │   ├── application-ui/
  │   └── ecommerce/
  └── metadata.json
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Acknowledgments

- Tailwind UI team for their amazing component library
- Contributors and maintainers
- Open source community

## 📮 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@yourhandle](https://twitter.com/yourhandle)

## 🐛 Known Issues

- Some components may require JavaScript interaction to reveal their code
- Dynamic loading of components might need additional wait times
- Certain components might render differently in headless mode
- CAPTCHAs or authentication challenges may require manual intervention
- Rate limiting and IP blocking need careful consideration

Please report any bugs or feature requests through the issue tracker.
