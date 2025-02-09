"""
Unit tests for the ExtractCodewords module.

This module contains tests for the following functions:
- fetch_scroll_content: Fetches the content of the scroll from a given URL.
- extract_secrets: Extracts secrets from the scroll content.
"""

import unittest
from unittest.mock import patch
from ExtractCodewords import fetch_scroll_content, extract_secrets

# FILE: test_extractcodewords.py


class TestExtractCodewords(unittest.TestCase):

    @patch('ExtractCodewords.requests.get')
    def test_fetch_scroll_content(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Sample text'
        url = 'http://example.com'
        result = fetch_scroll_content(url)
        self.assertEqual(result, 'Sample text')
        mock_get.assert_called_once_with(url)

    def test_extract_secrets(self):
        content = 'This is a secret {*secret1*} and another {*secret2*}.'
        expected_secrets = ['secret1', 'secret2']
        result = extract_secrets(content)
        self.assertEqual(result, expected_secrets)

if __name__ == '__main__':
    unittest.main()