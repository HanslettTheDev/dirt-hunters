import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_mail import Message

from dirt_hunters import db, mail
from dirt_hunters.models.models import CustomerRequests, Reviews

core = Blueprint("core", __name__)


@core.route("/", methods=["GET", "POST"])
def index():
    reviews = db.session.execute(db.select(Reviews)).scalars()
    return render_template("index.html", reviews=reviews)


@core.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        review = Reviews(
            name=request.form["name"],
            rating=request.form["rating"],
            review_title=request.form["title"],
            review_content=request.form["content"],
        )

        db.session.add(review)
        db.session.commit()

        return redirect(url_for("core.index", _anchor="reviews"))
    return render_template("review.html")


@core.route("/api/send_email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        required_fields = ["fullName", "email", "service", "message"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Store in the database
        customer_request = CustomerRequests(
            full_name=data["fullName"],
            email=data["email"],
            phone_number=data["phone"],
            service_type=data["service"],
            message=data["message"],
        )
        db.session.add(customer_request)
        db.session.commit()

        # # Create email message
        # msg = Message(
        #     subject=f"New Cleaning Service Request - {data['service']}",
        #     recipients=[
        #         os.getenv("RECIPIENT_EMAIL"),
        #     ],  # Email where you want to receive requests
        # )
        #
        # # Build email body
        # msg.body = f"""
        #     New cleaning service request received:
        #
        #     Full Name: {data['fullName']}
        #     Email: {data['email']}
        #     Phone: {data.get('phone', 'Not provided')}
        #     Service Type: {data['service']}
        #     Message:
        #     {data['message']}
        #
        #     Sent from website(www.dirt-hunters.com) contact form.
        # """
        #
        # mail.send(msg)
        #
        return jsonify({"message": "Form submitted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occured"}), 400
