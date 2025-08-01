import sys
import re
from urllib.parse import unquote, urlparse, parse_qs

def find_original_image_url(cdn_url):
    """
    Attempts to find the original image URL from a CDN-processed URL using a multi-step, robust approach.

    Args:
        cdn_url: The URL of the image from the CDN.

    Returns:
        The likely original image URL, or None if it cannot be found.
    """
    # --- Strategy 1: Look for the URL in query parameters ---
    # Handles URLs like: ...?url=https%3A%2F%2Fexample.com%2Fimage.png
    try:
        parsed_url = urlparse(cdn_url)
        query_params = parse_qs(parsed_url.query)
        for key, values in query_params.items():
            for value in values:
                # Check if the query parameter value is itself a URL
                if value.lower().startswith(('http://', 'https://')) or value.lower().startswith('http%3a'):
                    return unquote(value)
    except Exception:
        pass # Ignore parsing errors and move to the next strategy

    # --- Strategy 2: Look for embedded URLs in the path ---
    # This is the fix for the reported issue.
    decoded_url = unquote(cdn_url)
    
    # Find all occurrences of 'http://' or 'https://'
    # re.finditer provides the start index of each match
    matches = list(re.finditer(r'https?://', decoded_url))

    if len(matches) > 1:
        # If we found more than one 'http(s)://', the last one is the embedded original URL
        last_match_start_index = matches[-1].start()
        potential_url = decoded_url[last_match_start_index:]
        
        # A final sanity check to ensure it looks like an image URL
        if re.search(r'\.(?:png|jpe?g|gif|bmp|tiff|webp|svg)', potential_url, re.IGNORECASE):
            return potential_url

    # --- Fallback Strategy 3: Original regex, but only as a last resort ---
    # This might still catch some edge cases, but it's less reliable.
    potential_urls = re.findall(r'(https?://\S+\.(?:png|jpe?g|gif|bmp|tiff|webp|svg))', decoded_url, re.IGNORECASE)
    if potential_urls:
        # To avoid the original error, we ensure the found URL is not the same as the decoded input URL
        # unless it is a direct link to an image.
        if potential_urls[-1] != decoded_url or cdn_url.endswith(('.png', '.jpg', '.jpeg')):
            return potential_urls[-1]

    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode_url.py \"<url>\"")
        print("\nNote: Always wrap the URL in double quotes to handle special characters.")
        sys.exit(1)

    input_url = sys.argv[1]
    original_url = find_original_image_url(input_url)

    if original_url:
        print("Found potential original URL:")
        print(original_url)
    else:
        print("Could not automatically determine the original URL.")
        print("Here is the fully decoded URL for manual inspection:")
        print(unquote(input_url))