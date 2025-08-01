import sys
import re
from urllib.parse import unquote, urlparse

def find_original_image_url(cdn_url):
    """
    Attempts to find the original image URL from a CDN-processed URL.

    Args:
        cdn_url: The URL of the image from the CDN.

    Returns:
        The likely original image URL, or None if it cannot be found.
    """
    # First, decode the entire URL to handle any nested encoding
    decoded_url = unquote(cdn_url)

    # Regex to find potential image URLs within the decoded URL
    # This looks for http/https starting strings ending with a common image extension
    potential_urls = re.findall(r'(https?://\S+\.(?:png|jpe?g|gif|bmp|tiff|webp))', decoded_url, re.IGNORECASE)

    if potential_urls:
        # Return the last found URL, as it's often the original source
        return potential_urls[-1]

    # Fallback for URLs where the protocol is not part of the encoded string
    # (e.g., Cloudflare-style URLs)
    parsed_url = urlparse(decoded_url)
    path_parts = parsed_url.path.split('/')
    for part in reversed(path_parts):
        # Heuristic to check if a part looks like a domain name
        if '.' in part and not part.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
             # Check the part of the url that comes after what we suspect is the domain
            try:
                # Find the index of the potential domain and reconstruct the rest of the URL
                start_index = decoded_url.rfind(part)
                # Check if the found part is indeed part of the path or the netloc
                if start_index > decoded_url.find(parsed_url.netloc):
                    reconstructed_url = "https://" + decoded_url[start_index:]
                    # A simple check to see if it looks like a valid URL
                    if re.match(r'^https?://\S+\.\S+', reconstructed_url):
                        return reconstructed_url
            except ValueError:
                continue


    return None

if __name__ == "__main__":
    # Ensure a URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python decode_url.py <url>")
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