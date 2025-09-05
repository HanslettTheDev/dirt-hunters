import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from dirt_hunters import db
from dirt_hunters.mails import send_email_via_graph_api
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

        # Build email body
        subject = f"New Cleaning Service Request - {data['service']}"
        body = f"""
            New cleaning service request received:

            Full Name: {data['fullName']}
            Email: {data['email']}
            Phone: {data.get('phone', 'Not provided')}
            Service Type: {data['service']}
            Message:
            {data['message']}

            Sent from website(www.dirt-hunters.com) contact form.
        """

        recipients = [
            {
                "emailAddress": {
                    "address": os.getenv("RECIPIENT_EMAIL"),
                },
            }
        ]

        # Send email to mail account
        send_email_via_graph_api(subject, recipients, body)

        blob = {
            "subject": "Thank you! Your Message has been receieved",
            "body": "Thank you for contacting Dirt-Hunters Cleaning Services. We have recieved your request and we will get back to you shortly",
            "recipients": [
                {
                    "emailAddress": {
                        "address": data["email"],
                    },
                }
            ],
        }
        # Send confirmation message that email has been received
        send_email_via_graph_api(
            blob.get("subject"), blob.get("recipients"), blob.get("body")
        )

        customer_request.is_email_sent = True
        db.session.add(customer_request)
        db.session.commit()

        return jsonify({"message": "Form submitted successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"An unexpected error occured"}), 400
