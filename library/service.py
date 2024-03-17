import requests


class OpenLibraryService:
    @staticmethod
    def fetch_book_details(isbn):
        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("title", ""),
                    "author": data["authors"][0]["key"],
                }
            else:
                return None
        except requests.RequestException:
            return None
