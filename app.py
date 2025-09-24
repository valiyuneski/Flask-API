from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit per IP
    default_limits=[]
)
limiter.init_app(app)


# In-memory "database"
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id: int):
    return next((book for book in books if book["id"] == book_id), None)


def validate_book_data(data: dict) -> bool:
    return isinstance(data, dict) and "title" in data and "author" in data


# ----------------------------
# Routes
# ----------------------------

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        # Query params
        author = request.args.get('author')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        filtered_books = books
        if author:
            filtered_books = [book for book in books if book.get('author') == author]

        # Pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_books = filtered_books[start_index:end_index]

        return jsonify(paginated_books), 200

    elif request.method == 'POST':
        new_book = request.get_json()
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400

        # Assign a new unique ID
        new_book["id"] = max((book["id"] for book in books), default=0) + 1
        books.append(new_book)
        return jsonify(new_book), 201

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id: int):
    book = find_book_by_id(id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    new_data = request.get_json()
    if not new_data:
        return jsonify({"error": "Invalid update data"}), 400

    book.update(new_data)
    return jsonify(book), 200


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id: int):
    book = find_book_by_id(id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify(book), 200


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.route('/api/books', methods=['GET'])
@limiter.limit("10/minute")  # Limit each IP to 10 requests per minute
def handle_Limiter_books():
    # Example response
    return jsonify({"message": "This is a rate-limited endpoint"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9191, debug=True)