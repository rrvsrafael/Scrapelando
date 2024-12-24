from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from .utils import validate_search_term, validate_min_score


def toggle_filter(driver):
    try:
        toggle_button = driver.find_element(By.CSS_SELECTOR, "input#filter-switch")
        if toggle_button.get_attribute("aria-checked") == "false":
            print("Clicking the toggle button to enable the filter.")
            toggle_button.click()
            time.sleep(0.5)
        else:
            print("Toggle is already enabled.")
    except Exception as e:
        print(f"Error toggling the filter button: {e}")


def scrape_pelando(search_term, min_score):
    result = []
    search_term = validate_search_term(search_term)
    min_score = validate_min_score(min_score)

    base_url = "https://www.pelando.com.br/busca/{}/promocoes".format(search_term)
    print(f"Fetching URL: {base_url}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)

    time.sleep(2)
    toggle_filter(driver=driver)

    print("Page loaded. Parsing HTML...")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    print("Checking product container structure...")
    products = soup.find_all("li", class_="sc-4af6a208-2 fLZJCR")
    print(f"Found {len(products)} products. Processing...")

    if not products:
        print("No products found on the page.")
        driver.quit()
        return

    for product in products:
        try:
            title_tag = product.find("a", class_="sc-gfMXTh uAKsV")
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            link = title_tag["href"] if title_tag else "No link"

            score_span = product.find("span", class_="sc-KDzwu hMCrdh")
            score = (
                score_span.get_text(strip=True).replace("º", "") if score_span else "0"
            )
            score = int(score)

            price_div = product.find("div", class_="sc-gUhVhA eEDhfK sc-ckafRU gvOVwL")
            price = price_div.get_text() if price_div else "No price listed"

            if score >= min_score:
                output_str = f"{title}\nScore: {score}\n{price}\n{link}\n\n"
                print(output_str)
                result.append(output_str)

        except Exception as e:
            print(f"Error processing a product: {e}")

    driver.quit()
    return result
