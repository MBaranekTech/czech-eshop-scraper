# Alza Product Scraper

🛒 Python web scraper for extracting product data from Alza.cz (Czech e-commerce platform). Extract product information and export to CSV with optional HTML table visualization featuring advanced filtering.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Features

- 🕷️ **Web Scraping** - Extract product data from Alza.cz using Selenium
- 💾 **CSV Export** - Save scraped data to CSV format
- 📊 **HTML Visualization** - Convert CSV to searchable HTML tables
- 🔍 **Real-time Search** - Filter products instantly in HTML output
- 🎛️ **Advanced Filtering** - Filter by CPU, RAM, or any custom field
- 🔗 **Automatic Links** - URLs are converted to clickable hyperlinks
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 📈 **Live Counter** - See filtered results count in real-time

## 📋 Table of Contents

- [What is Selenium?](#-what-is-selenium)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Web Scraper](#1-web-scraper)
  - [CSV to HTML Converter](#2-csv-to-html-converter)
- [Example Output](#-example-output)
- [Requirements](#️-requirements)
- [Project Structure](#-project-structure)
- [Tips & Best Practices](#-tips--best-practices)
- [Configuration](#-configuration)
- [Disclaimer](#️-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)

## 🤖 What is Selenium?

**Selenium** is a powerful web automation framework that allows you to control a web browser programmatically. Unlike simple HTTP requests, Selenium opens a real browser (Chrome, Firefox, etc.) and interacts with web pages just like a human would.

### Why Use Selenium for Web Scraping?

**Traditional scraping (requests + BeautifulSoup):**
- ✅ Fast and lightweight
- ✅ Low resource usage
- ❌ Can't handle JavaScript-rendered content
- ❌ Blocked by anti-bot protections
- ❌ Can't interact with dynamic elements

**Selenium scraping:**
- ✅ Handles JavaScript-heavy websites (React, Vue, Angular)
- ✅ Can click buttons, fill forms, scroll pages
- ✅ Bypasses many anti-bot measures (appears as real user)
- ✅ Can wait for dynamic content to load
- ✅ Takes screenshots and executes JavaScript
- ❌ Slower than traditional methods
- ❌ Higher resource usage

### When to Use Selenium?

Use Selenium when the website:
- Loads products dynamically with JavaScript
- Requires scrolling to load more items
- Has complex interactions (dropdowns, filters)
- Blocks simple HTTP requests
- Uses AJAX to fetch data

**Perfect for sites like Alza.cz** which heavily rely on JavaScript for product listings!

## 🔄 How It Works

### Scraping Process

```
1. 🌐 Selenium opens Chrome browser
2. 🔍 Navigates to Alza.cz
3. ⏳ Waits for products to load (JavaScript)
4. 📦 Extracts product data (name, price, link)
5. 💾 Saves to CSV file
6. 📊 Converts CSV to HTML table
7. ✅ Done!
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Computer                            │
│                                                             │
│  ┌──────────────────┐          ┌─────────────────┐          │
│  │  Python Script   │────────▶│  Selenium        │         │
│  │  scraper.py      │          │  WebDriver      │          │
│  └──────────────────┘          └────────┬────────┘          │
│                                         │                   │
│                                         ▼                   │
│                              ┌─────────────────┐            │
│                              │  Chrome Browser │            │
│                              │  (Automated)    │            │
│                              └────────┬────────┘            │
└───────────────────────────────────────┼─────────────────────┘
                                        │ HTTPS
                                        ▼
                          ┌──────────────────────┐
                          │     Alza.cz          │
                          │  🛒 E-commerce Site  │
                          └──────────────────────┘
                                        │
                                        ▼
                          ┌──────────────────────┐
                          │   Product Data       │
                          │ • Name: Mouse XYZ    │
                          │ • Price: 299 Kč      │
                          │ • Link: alza.cz/...  │
                          └──────────────────────┘
```

### Step-by-Step Visual Guide

**Step 1: Browser Launch**
```
🚀 Starting EDGE browser...
✓ Browser opened successfully
```

**Step 2: Page Loading**
```
🌐 Navigating to Alza.cz...
⏳ Waiting for products to load...
✓ Products found: 50 items
```

**Step 3: Data Extraction**
```
📦 Extracting product data...
  [1] Logitech MX Master 3S - 2,299 Kč
  [2] Apple Magic Keyboard - 2,890 Kč
  [3] Samsung 980 PRO - 3,199 Kč
✓ Extraction complete
```

**Step 4: Export**
```
💾 Saving to products.csv...
✓ CSV saved: 50 products

📊 Converting to HTML...
✓ HTML saved: catalogue.html
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/MBaranekTech/czech-eshop-scraper
cd czech-eshop-scraper
```

2. **Browser Setup**

Selenium requires a browser driver. This project uses **EDGE** with manual driver management.



## 📖 Usage

### 1. Web Scraper

Extract product data from Alza.cz and save to CSV.

```bash
python scraper.py
```

**What it does:**
- Scrapes product names, prices, and links from Alza.cz
- Saves data to CSV file
- Handles Czech currency (Kč)
- Error handling for failed requests

**Example CSV output:**
```csv
Product Name,Price,CPU,RAM,Alza Link
Lenovo ThinkPad X1,25 999 Kč,Intel i5-1135G7,8GB,https://www.alza.cz/lenovo-x1
Dell XPS 13,35 999 Kč,Intel i7-1165G7,16GB,https://www.alza.cz/dell-xps
HP Pavilion 15,18 999 Kč,AMD Ryzen 5,8GB,https://www.alza.cz/hp-pavilion
```

---

### 2. CSV to HTML Converter

Convert your CSV export into a beautiful, searchable HTML table with advanced filtering.

```bash
python csv_to_catalogue.py
```

**Interactive prompts:**
1. Enter CSV file name (e.g., `products.csv`)
2. Enter output HTML file name (default: `catalogue.html`)
3. Enter page title (default: `Alza Product Export List`)

**Features:**
- 📊 Clean table layout with alternating row colors
- 🔍 Real-time search functionality
- 🎛️ **CPU and RAM dropdown filters** - Auto-detected from CSV
- 🔗 Automatic hyperlink detection
- 📱 Responsive design
- 🎨 Professional UI with hover effects
- 🧹 Clear filters button - Reset all filters instantly
- 📈 Live results counter - "X of Y items"
- 💡 Active filter indicator - Shows which filters are applied

## 📸 Example Output

### CSV File
```csv
Product Name,Price,CPU,RAM,Alza Link
Lenovo ThinkPad X1,25 999 Kč,Intel i5-1135G7,8GB,https://www.alza.cz/lenovo-x1
Dell XPS 13,35 999 Kč,Intel i7-1165G7,16GB,https://www.alza.cz/dell-xps
HP Pavilion 15,18 999 Kč,AMD Ryzen 5,8GB,https://www.alza.cz/hp-pavilion
ASUS ROG Strix,45 999 Kč,Intel i9-11900H,32GB,https://www.alza.cz/asus-rog
```

### HTML Table with Filters
The generated HTML includes:
- **CPU Filter Dropdown** - Select specific processor (auto-detected)
- **RAM Filter Dropdown** - Select memory size (auto-detected)
- **Search Box** - Text search across all fields
- **Clear Filters Button** - Reset all filters with one click
- **Active Filter Indicator** - Blue banner showing applied filters
- Sequential row numbering
- Detail icons for each product
- Clickable links to Alza.cz
- Live results counter (e.g., "15 of 50 items")
- Clean, professional design

### Filter Detection
The converter automatically detects filter columns:
- **CPU columns:** Looks for "CPU", "Processor", "Procesor"
- **RAM columns:** Looks for "RAM", "Memory", "Paměť"
- **Custom filters:** Easy to extend for other columns

**Preview:**
```
┌───────────────────────────────────────────────────────────────┐
│ Alza Product Export List                                      │
│ [CPU: All CPUs ▼] [RAM: All RAM ▼] [Search...] [Clear Filters]│
│ 🔍 Active filters: CPU: Intel i7 | RAM: 16GB                 │
├────┬────────┬─────────────────┬──────────┬─────────┬─────────┤
│No. │ Detail │ Product Name    │ Price    │ CPU     │ RAM     │
├────┼────────┼─────────────────┼──────────┼─────────┼─────────┤
│ 1  │   ⊙    │ Dell XPS 13     │ 35 999 Kč│ i7-1165 │ 16GB    │
└────┴────────┴─────────────────┴──────────┴─────────┴─────────┘
Showing 1 of 4 items
```

## 🛠️ Requirements

### Web Scraper
```
python >= 3.x
selenium >= 4.0.0
webdriver-manager
beautifulsoup4 (optional, for HTML parsing)
```

### CSV to HTML Converter
```
python >= 3.x
No external dependencies (uses built-in csv module)
```


**Supported browsers:**
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ⚠️ Safari (macOS only)

## 📁 Project Structure

```
alza-product-scraper/
│
├── scraper.py          # Main web scraping tool (Selenium)
├── csv_to_catalogue.py      # CSV to HTML converter
├── README.md               # This file
├── msdriver.exe # Microsoft EDGE Browser driver for Selenium


```

## 💡 Tips & Best Practices

### Web Scraping
1. **Respect robots.txt** - Always check Alza.cz's robots.txt before scraping
2. **Rate limiting** - Add delays between requests to avoid overloading the server
3. **User-Agent** - Use appropriate User-Agent headers
4. **Legal compliance** - Ensure your scraping complies with local laws and terms of service
5. **Data updates** - Product prices change frequently, scrape responsibly

### CSV Structure for Best Results
1. **Column naming** - Use clear names like "CPU", "RAM", "Price" for auto-detection
2. **Consistent formatting** - Keep data format consistent within columns
3. **URLs** - Full URLs (https://...) are auto-converted to clickable links
4. **Special characters** - UTF-8 encoding supports Czech characters (Kč, ě, š, etc.)

### HTML Filtering
- **Multiple filters** - CPU, RAM, and search work together
- **Clear button** - Quickly reset to see all items
- **Live updates** - Counter shows filtered results instantly
- **Case insensitive** - Search works regardless of letter case

## 🔧 Configuration

You can customize the scraper by modifying these variables in `scraper.py`:


## ⚠️ Disclaimer

This tool is for educational purposes only. When scraping websites:
- Respect the website's Terms of Service
- Follow robots.txt guidelines
- Don't overload servers with requests
- Use scraped data responsibly
- Check local laws regarding web scraping

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Tested on [Alza.cz](https://www.alza.cz) - Czech e-commerce platform
- Built with Python and love ❤️

## 📧 Contact

- GitHub: [@MBaranekTech](https://github.com/MBaranekTech/)
- LinkedIn: [baranekm](https://www.linkedin.com/in/baranekm-736a7532b/)

---

⭐ If you find this project useful, please consider giving it a star!

