import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_amazon_price(upc):
    try:
        # Example URL structure, actual implementation will vary and require parsing the HTML
        url = f"https://www.amazon.com/s?k={upc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("span", {"class": "a-price-whole"}).get_text()
        return float(price.replace(",", "").replace("$", ""))
    except Exception as e:
        print(f"Amazon: {e}")
        return None


def get_walmart_price(upc):
    try:
        url = f"https://www.walmart.com/search/?query={upc}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("span", {"class": "price-characteristic"}).get_text()
        return float(price.replace(",", "").replace("$", ""))
    except Exception as e:
        print(f"Walmart: {e}")
        return None


def get_target_price(upc):
    try:
        url = f"https://www.target.com/s?searchTerm={upc}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("span", {"data-test": "product-price"}).get_text()
        return float(price.replace(",", "").replace("$", ""))
    except Exception as e:
        print(f"Target: {e}")
        return None


def get_homedepot_price(upc):
    try:
        url = f"https://www.homedepot.com/s/{upc}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("span", {"class": "price__dollars"}).get_text()
        return float(price.replace(",", "").replace("$", ""))
    except Exception as e:
        print(f"Home Depot: {e}")
        return None


def get_lowes_price(upc):
    try:
        url = f"https://www.lowes.com/search?searchTerm={upc}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("span", {"class": "price"}).get_text()
        return float(price.replace(",", "").replace("$", ""))
    except Exception as e:
        print(f"Lowe's: {e}")
        return None


def get_prices(upc):
    prices = {
        "Amazon": get_amazon_price(upc),
        "Walmart": get_walmart_price(upc),
        "Target": get_target_price(upc),
        "Home Depot": get_homedepot_price(upc),
        "Lowe's": get_lowes_price(upc),
    }
    return prices


def compute_statistics(prices):
    valid_prices = [price for price in prices.values() if price is not None]
    if not valid_prices:
        return None, None, None, None
    avg_price = sum(valid_prices) / len(valid_prices)
    min_price = min(valid_prices)
    max_price = max(valid_prices)
    price_spread = max_price - min_price
    return avg_price, min_price, max_price, price_spread


def display_results(prices):
    avg_price, min_price, max_price, price_spread = compute_statistics(prices)

    if avg_price is None:
        print("No prices available.")
        return

    price_data = []
    for store, price in prices.items():
        if price is not None:
            diff_avg = price - avg_price
            diff_min = price - min_price
        else:
            diff_avg = ""
            diff_min = ""
        price_data.append([store, price, diff_avg, diff_min])

    df = pd.DataFrame(
        price_data,
        columns=["Store", "Price", "Difference from Average", "Difference from Lowest"],
    )
    print(df.to_string(index=False))

    print(f"\nStatistics:")
    print(f"Average Price: ${avg_price:.2f}")
    print(f"Minimum Price: ${min_price:.2f}")
    print(f"Maximum Price: ${max_price:.2f}")
    print(f"Price Spread: ${price_spread:.2f}")


def main():
    while True:
        upc = input("Enter a UPC code (or 'exit' to quit): ")
        if upc.lower() == "exit":
            break
        prices = get_prices(upc)
        display_results(prices)


if __name__ == "__main__":
    main()
