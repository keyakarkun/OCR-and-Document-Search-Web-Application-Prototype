import cv2
import numpy as np
import re


def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Remove noise from the image
    kernel = np.ones((1, 1), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    return thresh

def search_keywords(text, keywords):
    # Split keywords into individual words
    keywords = [keyword.strip().lower() for keyword in keywords.split(',')]

    # Initialize search results
    search_results = []

    # Iterate over each keyword
    for keyword in keywords:
        # Use regular expression to find all occurrences of the keyword
        matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE)

        # Add matches to search results
        for match in matches:
            search_results.append((match.start(), match.end()))

    return search_results