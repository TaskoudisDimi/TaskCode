from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from .models import Product, Category, Order, OrderItem
from . import db


shop = Blueprint("shop", __name__)

@shop.route("/products")
def products():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("products.html", products=products, categories=categories)


@shop.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

@shop.route("/add_to_cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get("quantity", 1))

    if quantity > product.stock:
        flash("Not enough stock available.")
        return redirect(url_for("shop.product_detail", product_id=product_id))

    # For simplicity, we'll store cart in session (in production, use a proper cart model)
    if "cart" not in session:
        session["cart"] = []

    # Check if product is already in cart
    for item in session["cart"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        session["cart"].append({"product_id": product_id, "quantity": quantity})

    session.modified = True
    flash("Product added to cart.")
    return redirect(url_for("shop.products"))

@shop.route("/cart")
@login_required
def view_cart():
    cart_items = []
    total = 0
    if "cart" in session:
        for item in session["cart"]:
            product = Product.query.get(item["product_id"])
            if product:
                cart_items.append({
                    "product": product,
                    "quantity": item["quantity"],
                    "subtotal": product.price * item["quantity"]
                })
                total += product.price * item["quantity"]
    return render_template("cart.html", cart_items=cart_items, total=total)

@shop.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        if "cart" not in session or not session["cart"]:
            flash("Your cart is empty.")
            return redirect(url_for("shop.cart"))

        # Create a new order
        total_amount = 0
        order = Order(user_id=current_user.id, total_amount=0, status="Pending")
        db.session.add(order)
        db.session.flush()  # Get order ID before committing

        for item in session["cart"]:
            product = Product.query.get(item["product_id"])
            if not product or product.stock < item["quantity"]:
                flash(f"Product {product.name} is out of stock.")
                db.session.rollback()
                return redirect(url_for("shop.cart"))

            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=product.price
            )
            total_amount += product.price * item["quantity"]
            product.stock -= item["quantity"]  # Update stock
            db.session.add(order_item)

        order.total_amount = total_amount
        db.session.commit()

        # Clear cart
        session.pop("cart", None)
        flash("Order placed successfully!")
        return redirect(url_for("shop.orders"))

    return render_template("checkout.html")

@shop.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("orders.html", orders=orders)