import requests

BASE_URL = "http://127.0.0.1:9191/api/books"  # Change if running in Codio with a public URL


def test_get_books():
    print("GET /api/books")
    resp = requests.get(BASE_URL)
    print(resp.status_code, resp.json())


def test_post_book():
    print("\nPOST /api/books")
    new_book = {"title": "Test Driven Development", "author": "Kent Beck"}
    resp = requests.post(BASE_URL, json=new_book)
    print(resp.status_code, resp.json())
    return resp.json()["id"]  # return the new book’s ID


def test_put_book(book_id):
    print(f"\nPUT /api/books/{book_id}")
    update = {"title": "TDD by Example"}
    resp = requests.put(f"{BASE_URL}/{book_id}", json=update)
    print(resp.status_code, resp.json())


def test_delete_book(book_id):
    print(f"\nDELETE /api/books/{book_id}")
    resp = requests.delete(f"{BASE_URL}/{book_id}")
    print(resp.status_code, resp.json())


def test_filtered_books():
    print("\nGET /api/books?author=George Orwell")
    resp = requests.get(BASE_URL, params={"author": "George Orwell"})
    print(resp.status_code, resp.json())


def test_paginated_books():
    print("\nGET /api/books?page=1&limit=1")
    resp = requests.get(BASE_URL, params={"page": 1, "limit": 1})
    print(resp.status_code, resp.json())


if __name__ == "__main__":
    test_get_books()
    new_id = test_post_book()
    test_put_book(new_id)
    test_filtered_books()
    test_paginated_books()
    test_delete_book(new_id)
    test_get_books()