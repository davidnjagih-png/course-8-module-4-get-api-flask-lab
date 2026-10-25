from flask import Flask, jsonify, request
from data import products
 
app = Flask(__name__)
 
 
# Homepage: confirms the API is running and lists available endpoints
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Product Catalog API",
        "endpoints": ["/products", "/products/<id>", "/products?category=<name>"],
    }), 200
 
 
# GET /products: returns the full product list, or only products in a
# category when ?category= is given (case-insensitive match)
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    if category:
        wanted = category.strip().lower()
        filtered = [p for p in products if p["category"].lower() == wanted]
        return jsonify(filtered), 200
    return jsonify(products), 200
 
 
# GET /products/<id>: returns a single product, or a JSON 404 if the ID is unknown
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": f"Product with id {id} not found"}), 404
    return jsonify(product), 200
 
 
# Any unknown route (or a non-integer ID) also gets a JSON 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404
 
 
if __name__ == "__main__":
    app.run(debug=True)
 