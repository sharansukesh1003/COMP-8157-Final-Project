import re
import redis
import requests

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def add_cache(page_name):
    """
    Cache a Wikipedia page and set its expiration.
    """
    # Check if the page is already cached
    cached_content = r.get(page_name)
    
    page_name_processed = re.sub(r'^\d+_|_en$', '', page_name)

    if cached_content:
        print(f"Cache hit for: {page_name_processed}")
        return cached_content.decode('utf-8')  # Return cached content
    
    print(f"Cache miss for: {page_name_processed}. Fetching from Wikipedia...")
    
    # Fetch content from Wikipedia
    response = requests.get(f"https://en.wikipedia.org/wiki/{page_name_processed}")
    
    if response.status_code == 200:
        # Cache the content
        print(f"Caching content for: {page_name_processed}")
        return response.text
    else:
        print(f"Failed to retrieve {page_name}. Status code: {response.status_code}")

def remove_cache(page_name):
    """
    Invalidate a cached Wikipedia page.
    """
    r.delete(page_name)
    print(f"Cache invalidated for: {page_name}")

if __name__ == "__main__":
    # Example usage
    add_cache("2016_in_film_en")