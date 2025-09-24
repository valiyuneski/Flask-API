# Flask-API

python3 -m venv venv
pip install flask
pip install requests
pip3 install Flask-Limiter

Now you can:
•	GET /api/books → list all books (default 10 per page).
•	GET /api/books?author=George Orwell → filter by author.
•	GET /api/books?page=2&limit=1 → paginate results.
•	POST /api/books → add new book.
•	PUT /api/books/<id> → update a book.
•	DELETE /api/books/<id> → delete a book.