import requests


class BookDetailsError(Exception):
    pass


def get_book_details(isbn):
    url = f"https://openlibrary.org/isbn/{isbn}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for non-2xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        raise BookDetailsError(f"Error retrieving book details: {e}")
    except requests.exceptions.HTTPError as e:
        # Handle non-successful HTTP status codes
        status_code = response.status_code

        if status_code == 404:
            # ISBN not found
            raise BookDetailsError("Book details not found")
        else:
            raise BookDetailsError(f"HTTP error: {status_code}")
