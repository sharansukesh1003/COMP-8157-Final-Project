import redis
import requests

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(page_name):
    """
    Cache a Wikipedia page and set its expiration.
    """
    # Check if the page is already cached
    cached_content = r.get(page_name)
    
    if cached_content:
        print(f"Cache hit for: {page_name}")
        return cached_content.decode('utf-8')  # Return cached content
    
    print(f"Cache miss for: {page_name}. Fetching from Wikipedia...")
    
    # Fetch content from Wikipedia
    response = requests.get(f"https://en.wikipedia.org/wiki/{page_name}")
    
    if response.status_code == 200:
        # Cache the content
        r.set(page_name, response.text, ex=7200)  # Cache for 2 hours
        return response.text
    else:
        print(f"Failed to retrieve {page_name}. Status code: {response.status_code}")
        return None

def invalidate_cache(page_name):
    """
    Invalidate a cached Wikipedia page.
    """
    r.delete(page_name)
    print(f"Cache invalidated for: {page_name}")

def set_eviction_policy():
    """
    Set Redis eviction policy to LRU.
    """
    r.config_set('maxmemory-policy', 'allkeys-lru')
    print("Eviction policy set to LRU.")


# Sample usage

# if __name__ == "__main__":
#     # Set eviction policy
#     set_eviction_policy()

#     # Cache specific pages
#     pages_to_cache = [
#         "Halloween",
#         "Thanksgiving",
#         "Christmas",
#         "New Year's Day",
#         "Diwali"
#     ]

#     for page in pages_to_cache:
#         cached_content = cache_page(page)
#         if cached_content:
#             print(f"Successfully cached content for: {page}")

#     # Invalidate a specific page (example: after the event)
#     invalidate_cache("Halloween")
