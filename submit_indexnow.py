#!/usr/bin/env python3
"""
Bing IndexNow Submission Script
Site: https://pdf.softcoverbooks.co.za/
API Key: fee097ac8b8c4f9ab8b43be1b0eda384
Key File: https://pdf.softcoverbooks.co.za/fee097ac8b8c4f9ab8b43be1b0eda384.txt

Standalone backend/admin utility to submit updated URLs directly to IndexNow
(Bing, Yandex, Naver, Seznam, and other participating search engines).
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

HOST = "pdf.softcoverbooks.co.za"
API_KEY = "fee097ac8b8c4f9ab8b43be1b0eda384"
KEY_LOCATION = f"https://{HOST}/{API_KEY}.txt"
DEFAULT_ENDPOINT = "https://api.indexnow.org/IndexNow"
DEFAULT_URL = f"https://{HOST}/"

# HTTP response code meanings per IndexNow protocol specification
HTTP_CODE_DESCRIPTIONS = {
    200: "200 OK - URL(s) submitted successfully.",
    202: "202 Accepted - URL(s) received; IndexNow key validation pending.",
    400: "400 Bad Request - Invalid request format.",
    403: "403 Forbidden - Key not valid or key file verification failed.",
    422: "422 Unprocessable Entity - URLs do not belong to the host or key does not match.",
    429: "429 Too Many Requests - Submissions are being throttled.",
}


def get_sitemap_urls(sitemap_path: str) -> list[str]:
    """Extract URLs from local sitemap XML."""
    if not os.path.exists(sitemap_path):
        return []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        urls = []
        for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url_text = elem.text.strip() if elem.text else ""
            if url_text and url_text not in urls:
                urls.append(url_text)
        return urls
    except Exception as e:
        print(f"Warning: Failed to parse sitemap at {sitemap_path}: {e}", file=sys.stderr)
        return []


def submit_to_indexnow(urls: list[str], endpoint: str = DEFAULT_ENDPOINT) -> bool:
    """Submit a list of URLs to the IndexNow API via HTTP POST."""
    if not urls:
        print("No URLs specified for submission.")
        return False

    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }

    data = json.dumps(payload, indent=2).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "IndexNow-Client/1.0 (pdf.softcoverbooks.co.za)",
            "Accept": "application/json, text/plain, */*",
        },
        method="POST",
    )

    print("=" * 60)
    print("INDEXNOW URL SUBMISSION")
    print("=" * 60)
    print(f"Endpoint:     {endpoint}")
    print(f"Host:         {HOST}")
    print(f"Key:          {API_KEY}")
    print(f"Key Location: {KEY_LOCATION}")
    print(f"Total URLs:   {len(urls)}")
    for u in urls[:10]:
        print(f"  - {u}")
    if len(urls) > 10:
        print(f"  ... and {len(urls) - 10} more")
    print("-" * 60)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = resp.getcode()
            resp_body = resp.read().decode("utf-8", errors="replace").strip()
            desc = HTTP_CODE_DESCRIPTIONS.get(status_code, f"{status_code} Response")
            print(f"Status: {desc}")
            if resp_body:
                print(f"Response: {resp_body}")
            print("=" * 60)
            print("IndexNow submission completed successfully!")
            print("=" * 60)
            return True

    except urllib.error.HTTPError as e:
        status_code = e.code
        desc = HTTP_CODE_DESCRIPTIONS.get(status_code, f"{status_code} Error")
        print(f"HTTP Error {status_code}: {desc}", file=sys.stderr)
        try:
            err_body = e.read().decode("utf-8", errors="replace").strip()
            if err_body:
                print(f"Server response:\n{err_body}", file=sys.stderr)
        except Exception:
            pass
        return False

    except urllib.error.URLError as e:
        print(f"Network error communicating with IndexNow: {e.reason}", file=sys.stderr)
        return False

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Submit URLs to Bing IndexNow for https://pdf.softcoverbooks.co.za/"
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="Optional list of specific URLs to submit. Defaults to homepage or sitemap.",
    )
    parser.add_argument(
        "--sitemap",
        action="store_true",
        help="Read and submit all URLs declared in the local sitemap.xml.",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"IndexNow API endpoint (default: {DEFAULT_ENDPOINT})",
    )

    args = parser.parse_args()

    # Determine URL list
    if args.urls:
        urls_to_submit = args.urls
    elif args.sitemap:
        sitemap_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "website",
            "public",
            "sitemap.xml",
        )
        urls_to_submit = get_sitemap_urls(sitemap_path)
        if not urls_to_submit:
            print("Warning: Could not read URLs from sitemap, falling back to default URL.")
            urls_to_submit = [DEFAULT_URL]
    else:
        urls_to_submit = [DEFAULT_URL]

    success = submit_to_indexnow(urls_to_submit, endpoint=args.endpoint)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
