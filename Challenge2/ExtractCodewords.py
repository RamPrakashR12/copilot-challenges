"""
ExtractCodewords module.

This module provides functions to fetch scroll content from a URL, extract secrets from the content,
display the extracted secrets, and validate URLs.

Functions:
- fetch_scroll_content: Fetches the content of the scroll from a given URL.
- extract_secrets: Extracts secrets from the scroll content.
- display_secrets: Displays the extracted secrets.
- validate_url: Validates the given URL.
"""

import requests
import re

def fetch_scroll_content(url):
    """
    Fetches the content of the scroll from the given URL.

    Args:
        url (str): The URL of the scroll.

    Returns:
        str: The content of the scroll.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_secrets(content):
    """
    Extracts secrets from the scroll content.

    Args:
        content (str): The content of the scroll.

    Returns:
        list: A list of extracted secrets.
    """
    pattern = r'\{\*(.*?)\*\}'
    secrets = re.findall(pattern, content)
    return secrets

def display_secrets(secrets):
    """
    Displays the extracted secrets.

    Args:
        secrets (list): A list of secrets to display.
    """
    for secret in secrets:
        print(f"Secret: {secret}")

def validate_url(url):
    """
    Validates the given URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/sombaner/copilot-hackathon-challenges/main/Data/Scrolls.txt'
    if validate_url(url):
        scroll_content = fetch_scroll_content(url)
        secrets = extract_secrets(scroll_content)
        display_secrets(secrets)
    else:
        print("Invalid URL")