from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_alza(search_query):
    """
    Scrape product data from alza.cz based on search query
    """
    # Path to your Edge WebDriver (assumes it's in the same folder as script)
    driver_path = "./msedgedriver.exe"  # Change to "msedgedriver" on Linux/Mac
    
    # Set up Edge WebDriver
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    
    try:
        print(f"Opening alza.cz...")
        driver.get("https://www.alza.cz")
        driver.maximize_window()
        
        # Handle cookie consent popup
        try:
            print("Checking for cookie consent popup...")
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-cookies-info-accept"))
            )
            cookie_button.click()
            print("Cookie consent accepted.")
            time.sleep(1)
        except Exception as e:
            print("No cookie popup found or already accepted.")
        
        # Wait for the search input to be present
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='searchInput']"))
        )
        
        print(f"Searching for: {search_query}")
        search_input.clear()
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        time.sleep(3)
        
        scraped_data = []
        page_number = 1
        
        while True:
            print(f"\nScraping page {page_number}...")
            
            # Wait for product listings to appear
            products = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.browsingitem"))
            )
            
            print(f"Found {len(products)} products on page {page_number}")
            print("-" * 80)
            
            for idx, product in enumerate(products, 1):  # Scrape all products on the page
                try:
                    # Extract product name
                    name_elem = product.find_element(By.CSS_SELECTOR, "a.name")
                    name = name_elem.text.strip()
                    
                    # Extract price
                    try:
                        price_elem = product.find_element(By.CSS_SELECTOR, "span.price-box__primary-price__value")
                        price = price_elem.text.strip()
                    except:
                        price = "Price not available"
                    
                    # Extract product URL
                    url = name_elem.get_attribute("href")
                    
                    # Extract description (CPU, RAM, etc.)
                    try:
                        description_elem = product.find_element(By.CSS_SELECTOR, "div.Description")
                        description = description_elem.text.strip()
                    except:
                        description = "No description available"
                    
                    # Parse CPU and RAM from description
                    cpu = "N/A"
                    ram = "N/A"
                    
                    if description != "No description available":
                        # Extract CPU (look for processor info)
                        import re
                        cpu_match = re.search(r'([^,]*(?:Intel|AMD|Apple M\d+|Ryzen|Core i\d|Celeron|Pentium)[^,]*)', description)
                        if cpu_match:
                            cpu = cpu_match.group(1).strip()
                        
                        # Extract RAM
                        ram_match = re.search(r'RAM\s+(\d+\s*GB)', description, re.IGNORECASE)
                        if ram_match:
                            ram = ram_match.group(1).strip()
                    
                    # Store data
                    product_data = {
                        "name": name,
                        "price": price,
                        "cpu": cpu,
                        "ram": ram,
                        "description": description,
                        "url": url
                    }
                    scraped_data.append(product_data)
                    
                    # Print product info
                    print(f"\n{name}")
                    print(f"Price: {price}")
                    print(f"CPU: {cpu}")
                    print(f"RAM: {ram}")
                    print(f"URL: {url}")
                    
                except Exception as e:
                    print(f"Error extracting product: {e}")
                    continue
            
            # Check if "more" button exists
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, "a.js-button-more.button-more")
                print(f"\n'More' button found. Loading next page...")
                
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                time.sleep(1)
                
                # Click the button
                more_button.click()
                
                # Wait for new products to load
                time.sleep(3)
                page_number += 1
                
            except Exception as e:
                print(f"\nNo more pages to load. Finished scraping.")
                break
        
        print("\n" + "-" * 80)
        print(f"Scraping completed! Total products scraped: {len(scraped_data)}")
        
        # Keep browser open for 5 seconds to see results
        time.sleep(5)
        
        return scraped_data
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
        
    finally:
        driver.quit()
        print("Browser closed.")

def main():
    """
    Main function to run the scraper
    """
    print("=" * 80)
    print("ALZA.CZ WEB SCRAPER")
    print("=" * 80)
    
    # Get search query from user
    search_query = input("\nEnter what you want to search on alza.cz: ").strip()
    
    if not search_query:
        print("Search query cannot be empty!")
        return
    
    # Run scraper
    results = scrape_alza(search_query)
    
    # Optional: Save results to CSV file
    if results:
        save_option = input("\nDo you want to save results to a CSV file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = f"alza_results_{search_query.replace(' ', '_')}.csv"
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Price', 'CPU', 'RAM', 'Description', 'URL'])  # Header
                for product in results:
                    writer.writerow([product['name'], product['price'], product['cpu'], product['ram'], product['description'], product['url']])
            print(f"Results saved to {filename}")

if __name__ == "__main__":
    main()