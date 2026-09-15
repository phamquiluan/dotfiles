#!/usr/bin/env python3
"""Download arXiv papers as PDFs.

Usage:
    python3 download_arxiv.py --output-dir ./pdfs 2408.13729 2405.09330 2510.04711
"""

import argparse
import os
import random
import ssl
import time
import urllib.request
import urllib.error


def _build_ssl_context() -> ssl.SSLContext:
    """Build an SSL context, falling back to unverified if certs are unavailable."""
    try:
        ctx = ssl.create_default_context()
        # Test that the context can actually verify certificates
        urllib.request.urlopen("https://arxiv.org", context=ctx, timeout=5)
        return ctx
    except (ssl.SSLCertVerificationError, urllib.error.URLError):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


def download_paper(arxiv_id: str, output_dir: str, ssl_context: ssl.SSLContext, max_retries: int = 3) -> bool:
    """Download a single arXiv paper as PDF with retry logic.

    Returns True if downloaded, False if skipped (already exists) or failed after retries.
    """
    filename = f"{arxiv_id}.pdf"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"Skipped (exists): {filename}")
        return False

    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    # arxiv.org/pdf is an Allowed path (robots.txt Crawl-delay: 15). A descriptive
    # User-Agent with a contact helps avoid robot-detection blocks.
    headers = {"User-Agent": "related-works-search/1.0 (mailto:noreply@example.com)"}

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                data = response.read()
            # arXiv's Varnish/Fastly layer can return HTTP 200 with a tiny
            # "Rate exceeded." body instead of the PDF. Treat that as rate limiting.
            if len(data) < 1024 and data.lstrip()[:13] == b"Rate exceeded":
                raise urllib.error.HTTPError(url, 429, "Rate exceeded", response.headers, None)
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"Downloaded: {filename}")
            return True
        except urllib.error.HTTPError as e:
            # 404 = no such PDF (e.g. bad/hallucinated ID): don't retry.
            if e.code == 404:
                print(f"Not found (HTTP 404), skipping: {filename}")
                return False
            if attempt < max_retries - 1:
                # 429/503 are often server-wide; back off harder (10s, 20s, 40s).
                wait_time = (2 ** attempt) * 10 if e.code in (429, 503) else (2 ** attempt) * 5
                print(f"Failed attempt {attempt + 1}/{max_retries} for {filename}: HTTP {e.code}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed to download {filename} after {max_retries} attempts (HTTP {e.code})")
                return False
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s
                print(f"Failed attempt {attempt + 1}/{max_retries} for {filename}: {type(e).__name__}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed to download {filename} after {max_retries} attempts")
                return False
        except Exception as e:
            print(f"Unexpected error downloading {filename}: {type(e).__name__}: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Download arXiv papers as PDFs")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save downloaded PDFs",
    )
    parser.add_argument(
        "arxiv_ids",
        nargs="+",
        help="arXiv IDs to download (e.g., 2408.13729 2405.09330)",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    ssl_context = _build_ssl_context()

    downloaded = 0
    failed = 0
    for i, arxiv_id in enumerate(args.arxiv_ids):
        if download_paper(arxiv_id, args.output_dir, ssl_context):
            downloaded += 1
        else:
            failed += 1
        if i < len(args.arxiv_ids) - 1:
            time.sleep(5)  # Increased delay between downloads to reduce rate limiting

    print(f"\nDone. Downloaded {downloaded}/{len(args.arxiv_ids)} papers to {args.output_dir}")
    if failed > 0:
        print(f"Failed to download {failed} papers (check output above for details)")


if __name__ == "__main__":
    main()
