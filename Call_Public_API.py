import json
import time
import requests
from requests.exceptions import RequestException

def fetch_and_save_api_data(url, output_path, retries=3, backoff_factor=1.5, timeout=5):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Success! Response written to {output_path}")
            return data
        except RequestException as e:
            print(f"Attempt {attempt}/{retries} failed: {e}")
            if attempt == retries:
                raise
            time.sleep(backoff_factor ** attempt)

# Example using a reliable mock API endpoint
try:
    fetch_and_save_api_data("https://jsonplaceholder.typicode.com/posts/1", "api_output.json")
except Exception as e:
    print(f"API pipeline terminated with error: {e}")