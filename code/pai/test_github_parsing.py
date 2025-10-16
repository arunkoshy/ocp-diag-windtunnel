# SPDX-FileCopyrightText: 2025 Hewlett Packard Enterprise Development LP
# SPDX-License-Identifier: MIT

#!/usr/bin/env python3
"""
Test script for GitHub URL parsing functionality
"""

from pai import extract_github_urls, convert_github_url_to_raw, fetch_github_content, enhance_prompt_with_github_content


def test_url_extraction():
    """Test URL extraction from text."""
    print("=== Testing URL Extraction ===")
    
    test_text = """
    Check out the spec text https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec
    the json schema https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec/output
    the api https://github.com/opencomputeproject/ocp-diag-core-python
    the python quickstarts https://github.com/opencomputeproject/ocp-diag-quickstart/tree/main/python
    this diag as an example https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py
    """
    
    urls = extract_github_urls(test_text)
    print(f"Found {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    return urls


def test_url_conversion():
    """Test URL conversion to raw/API URLs."""
    print("\n=== Testing URL Conversion ===")
    
    test_urls = [
        "https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec",
        "https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec/output", 
        "https://github.com/opencomputeproject/ocp-diag-core-python",
        "https://github.com/opencomputeproject/ocp-diag-quickstart/tree/main/python",
        "https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py"
    ]
    
    for url in test_urls:
        raw_url, content_type = convert_github_url_to_raw(url)
        print(f"\nOriginal: {url}")
        print(f"Raw/API:  {raw_url}")
        print(f"Type:     {content_type}")


def test_content_fetching():
    """Test fetching content from a single GitHub file."""
    print("\n=== Testing Content Fetching ===")
    
    # Test with a single file URL
    test_url = "https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py"
    print(f"Fetching content from: {test_url}")
    
    content = fetch_github_content(test_url)
    if content:
        print("Content fetched successfully!")
        print(f"Content length: {len(content)} characters")
        print("First 200 characters:")
        print(content[:200] + "..." if len(content) > 200 else content)
    else:
        print("Failed to fetch content")


def test_prompt_enhancement():
    """Test the full prompt enhancement functionality."""
    print("\n=== Testing Prompt Enhancement ===")
    
    test_prompt = """
    Can you explain the OCP diagnostic spec? Please look at:
    
    - The spec documentation: https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec
    - The Python API: https://github.com/opencomputeproject/ocp-diag-core-python
    - This example implementation: https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py
    
    What patterns should I follow for my own diagnostic?
    """
    
    print("Original prompt length:", len(test_prompt))
    enhanced_prompt = enhance_prompt_with_github_content(test_prompt)
    print("Enhanced prompt length:", len(enhanced_prompt))
    
    if len(enhanced_prompt) > len(test_prompt):
        print("✓ Prompt was successfully enhanced with GitHub content")
    else:
        print("✗ No enhancement occurred")


if __name__ == "__main__":
    print("GitHub URL Parsing Test Suite")
    print("=" * 50)
    
    try:
        test_url_extraction()
        test_url_conversion()
        test_content_fetching()
        test_prompt_enhancement()
        
        print("\n" + "=" * 50)
        print("Test suite completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()