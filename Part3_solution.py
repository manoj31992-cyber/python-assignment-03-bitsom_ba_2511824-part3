"""
Product Explorer & Error-Resilient Logger
Complete solution for all 4 tasks.
"""

import requests
from datetime import datetime

# ─────────────────────────────────────────────
# HELPER: Logger
# ─────────────────────────────────────────────

def log_error(location, error_type, message):
    """Append a timestamped error entry to error_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {location}: {error_type} — {message}\n"
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)


# ═══════════════════════════════════════════════════════════════
# TASK 1 — File Read & Write Basics
# ═══════════════════════════════════════════════════════════════

def task1():
    print("\n" + "="*60)
    print("TASK 1 — File Read & Write")
    print("="*60)

    # ── Part A: Write ──────────────────────────────────────────
    notes = [
        "Topic 1: Variables store data. Python is dynamically typed.",
        "Topic 2: Lists are ordered and mutable.",
        "Topic 3: Dictionaries store key-value pairs.",
        "Topic 4: Loops automate repetitive tasks.",
        "Topic 5: Exception handling prevents crashes.",
    ]

    with open("python_notes.txt", "w", encoding="utf-8") as f:
        for line in notes:
            f.write(line + "\n")
    print("File written successfully.")

    # Append two extra lines
    extra_lines = [
        "Topic 6: Functions help organise and reuse code.",
        "Topic 7: Modules let you split code across multiple files.",
    ]
    with open("python_notes.txt", "a", encoding="utf-8") as f:
        for line in extra_lines:
            f.write(line + "\n")
    print("Lines appended.")

    # ── Part B: Read ───────────────────────────────────────────
    with open("python_notes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("\nFile contents:")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.rstrip()}")

    print(f"\nTotal lines: {len(lines)}")

    keyword = input("\nEnter a keyword to search: ").strip()
    matches = [l.rstrip() for l in lines if keyword.lower() in l.lower()]
    if matches:
        print(f"Lines containing '{keyword}':")
        for m in matches:
            print(" ", m)
    else:
        print(f"No lines found containing '{keyword}'.")


# ═══════════════════════════════════════════════════════════════
# TASK 2 — API Integration
# ═══════════════════════════════════════════════════════════════

BASE_URL = "https://dummyjson.com/products"


def fetch_products(limit=20):
    """Step 1: Fetch products and print a formatted table."""
    url = f"{BASE_URL}?limit={limit}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        products = data.get("products", [])

        # Print formatted table
        header = f"{'ID':<4} | {'Title':<30} | {'Category':<13} | {'Price':>8} | {'Rating':>6}"
        print(header)
        print("-" * len(header))
        for p in products:
            print(f"{p['id']:<4} | {p['title']:<30} | {p['category']:<13} | ${p['price']:>7.2f} | {p['rating']:>6.2f}")

        return products

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_products", "ConnectionError", "Could not reach the server")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_products", "Timeout", "Request exceeded 5 seconds")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_products", "Exception", str(e))
        return []


def filter_and_sort(products):
    """Step 2: Filter rating >= 4.5, sort by price descending."""
    filtered = [p for p in products if p["rating"] >= 4.5]
    filtered.sort(key=lambda p: p["price"], reverse=True)

    print("\n--- Products with rating >= 4.5 (sorted by price desc) ---")
    for p in filtered:
        print(f"  {p['title']:<30} ${p['price']:>8.2f}  ★{p['rating']}")
    return filtered


def fetch_laptops():
    """Step 3: Fetch all laptops and print name + price."""
    url = f"{BASE_URL}/category/laptops"
    try:
        response = requests.get(url, timeout=5)
        laptops = response.json().get("products", [])

        print("\n--- Laptops ---")
        for p in laptops:
            print(f"  {p['title']:<35} ${p['price']:.2f}")

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_laptops", "ConnectionError", "Could not reach the server")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_laptops", "Timeout", "Request exceeded 5 seconds")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_laptops", "Exception", str(e))


def post_custom_product():
    """Step 4: POST a simulated new product."""
    url = f"{BASE_URL}/add"
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API",
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        print("\n--- POST Response ---")
        print(response.json())

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("post_custom_product", "ConnectionError", "Could not reach the server")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("post_custom_product", "Timeout", "Request exceeded 5 seconds")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("post_custom_product", "Exception", str(e))


def task2():
    print("\n" + "="*60)
    print("TASK 2 — API Integration")
    print("="*60)

    products = fetch_products(limit=20)
    if products:
        filter_and_sort(products)
    fetch_laptops()
    post_custom_product()


# ═══════════════════════════════════════════════════════════════
# TASK 3 — Exception Handling
# ═══════════════════════════════════════════════════════════════

# ── Part A: Guarded Calculator ─────────────────────────────────

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


# ── Part B: Guarded File Reader ────────────────────────────────

def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")


# ── Part D: Input Validation Loop ─────────────────────────────

def product_lookup_loop():
    """Repeatedly ask user for a product ID and fetch it."""
    while True:
        user_input = input("\nEnter a product ID to look up (1–100), or 'quit' to exit: ").strip()

        if user_input.lower() == "quit":
            print("Exiting product lookup.")
            break

        # Validate: must be an integer in 1–100
        try:
            product_id = int(user_input)
            if not (1 <= product_id <= 100):
                raise ValueError
        except ValueError:
            print("⚠ Invalid input. Please enter an integer between 1 and 100.")
            continue

        # Make the API call only with valid input
        url = f"{BASE_URL}/{product_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                print("Product not found.")
                log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
            elif response.status_code == 200:
                p = response.json()
                print(f"  Title: {p['title']}")
                print(f"  Price: ${p['price']:.2f}")
            else:
                print(f"Unexpected status code: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("Connection failed. Please check your internet.")
            log_error("lookup_product", "ConnectionError", "Could not reach the server")
        except requests.exceptions.Timeout:
            print("Request timed out. Try again later.")
            log_error("lookup_product", "Timeout", "Request exceeded 5 seconds")
        except Exception as e:
            print(f"Unexpected error: {e}")
            log_error("lookup_product", "Exception", str(e))


def task3():
    print("\n" + "="*60)
    print("TASK 3 — Exception Handling")
    print("="*60)

    # Part A
    print("\n-- Part A: safe_divide --")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    # Part B
    print("\n-- Part B: read_file_safe --")
    content = read_file_safe("python_notes.txt")
    if content:
        print(content[:80], "...")   # print a snippet
    read_file_safe("ghost_file.txt")

    # Part C is embedded in Task 2 API calls (all wrapped in try-except).

    # Part D
    print("\n-- Part D: Product Lookup Loop --")
    product_lookup_loop()


# ═══════════════════════════════════════════════════════════════
# TASK 4 — Logging to File
# ═══════════════════════════════════════════════════════════════

def task4():
    print("\n" + "="*60)
    print("TASK 4 — Logging")
    print("="*60)

    # Intentionally trigger a ConnectionError with an unreachable URL
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except requests.exceptions.ConnectionError:
        print("(Expected) Connection failed for unreachable URL.")
        log_error("fetch_products", "ConnectionError", "No connection could be made")
    except Exception as e:
        log_error("fetch_products", "Exception", str(e))

    # Intentionally trigger an HTTP 404 by requesting a non-existent product
    bad_id = 999
    try:
        response = requests.get(f"{BASE_URL}/{bad_id}", timeout=5)
        if response.status_code != 200:
            print(f"(Expected) Product {bad_id} not found — status {response.status_code}.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {bad_id}")
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("lookup_product", "ConnectionError", "Could not reach the server")
    except Exception as e:
        log_error("lookup_product", "Exception", str(e))

    # Print the full log file
    print("\n--- Contents of error_log.txt ---")
    with open("error_log.txt", "r", encoding="utf-8") as f:
        print(f.read())


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
