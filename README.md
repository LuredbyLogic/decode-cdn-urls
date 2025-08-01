Of course. Here is a `README.md` file for the Python script, formatted in Markdown for GitHub.

---

# CDN Image URL Decoder

A simple, command-line Python script to decode CDN-processed image URLs and retrieve the original source URL.

## Table of Contents
- [Description](#description)
- [How It Works](#how-it-works)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Description

Web services and blogs often use Content Delivery Networks (CDNs) like Substack's, Cloudflare, or AWS CloudFront to serve images. These CDNs automatically optimize images by resizing, compressing, and converting them to modern formats like WebP or AVIF.

While this is great for website performance, it can be frustrating if you need to download the original, high-quality PNG or JPEG file. The URL you get from your browser's "Copy Image Address" option often points to the processed, lower-quality version.

This script automates the process of inspecting these complex CDN URLs to find and extract the original, unmodified image link.

## How It Works

The script works by identifying common patterns used by CDNs to mask the original image URL:

1.  **URL Decoding:** It first performs a full URL-decode on the input string. CDNs often URL-encode the source image URL and append it to their processing endpoint.
2.  **Regex Matching:** It uses a regular expression to look for patterns that look like a complete URL (`http://...` or `https://...`) ending in a common image extension (`.png`, `.jpg`, `.jpeg`, etc.).
3.  **Path Analysis:** As a fallback, it analyzes the URL path for domain-like segments, attempting to reconstruct the original URL even if the `http://` prefix was stripped before encoding.

## Features

-   Decodes standard URL-encoded characters.
-   Finds embedded source URLs within a larger CDN link.
-   Handles multiple common image formats (PNG, JPEG, GIF, WebP, etc.).
-   Pure Python solution with no external libraries required.
-   Simple and straightforward command-line interface.

## Requirements

-   Python 3.10 or newer.

The script uses only standard Python libraries (`sys`, `re`, `urllib.parse`), so no `pip install` is needed.

## Installation

There is no formal installation process. Simply download the `decode_url.py` script to your local machine.

```bash
git clone https://github.com/your-username/cdn-url-decoder.git
cd cdn-url-decoder
```
Or, just save the code from the `decode_url.py` file directly.

## Usage

Run the script from your terminal or command prompt, passing the CDN URL as the only argument.

**Important:** Always wrap the URL in double quotes (`"`) to prevent your shell from misinterpreting special characters like `&`, `$`, or `?`.

### Syntax
```bash
python decode_url.py "<your_cdn_image_url>"
```

### On Windows
```powershell
# In PowerShell or CMD
cd path\to\script
python decode_url.py "https://your.cdn/url/..."
```

### On macOS / Linux
```bash
# In Terminal
cd path/to/script
python3 decode_url.py "https://your.cdn/url/..."
```

## Example

Here is an example using a common Substack CDN URL that converts a PNG to WebP.

### Command
```bash
python decode_url.py "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61394ea3-f9a1-49a4-a159-3fa52d79fc2d_1024x1024.png"
```

### Expected Output
```
Found potential original URL:
https://substack-post-media.s3.amazonaws.com/public/images/61394ea3-f9a1-49a4-a159-3fa52d79fc2d_1024x1024.png
```
You can now use this output link to download the original PNG file.

## Limitations

This script is based on heuristics and common CDN patterns. It may not work for all CDNs, especially if:
-   The CDN uses a proprietary or heavily obfuscated method to hide the source URL.
-   The original URL is not included in the public-facing link at all (e.g., it's referenced by an internal database ID).

If the script fails, it will print the fully decoded URL, which you can inspect manually to see if you can find the source link.

## Contributing

Contributions are welcome! If you have an idea for an improvement or find a CDN URL that this script can't handle, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
