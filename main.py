import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

project_folder = os.path.expanduser("~/dirt-hunters")
load_dotenv(os.path.join(project_folder, ".env"))

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Use your email provider's SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")  # Your email address
app.config["MAIL_PASSWORD"] = os.getenv(
    "EMAIL_PASSWORD"
)  # Your email password or app password
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_USER")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")


mail = Mail(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)

from datetime import datetime, timezone

# db models
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Reviews(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    rating: Mapped[int]
    review_title: Mapped[str]
    review_content: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now((timezone.utc))
    )


class CustomerRequests(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[int] = mapped_column(default=0)
    service_type: Mapped[str]
    message: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now((timezone.utc))
    )

    def __str__(self):
        return f"Customer Request: {self.full_name}"


@app.template_filter("datetime_format")
def datetime_format(value: datetime, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


@app.route("/", methods=["GET", "POST"])
def index():
    reviews = db.session.execute(db.select(Reviews)).scalars()
    return render_template("index.html", reviews=reviews)


@app.route("/reviews", methods=["GET", "POST"])
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

        return redirect(url_for("index", _anchor="reviews"))
    return render_template("review.html")


@app.route("/api/send_email", methods=["POST"])
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

        # Create email message
        # msg = Message(
        #     subject=f"New Cleaning Service Request - {data['service']}",
        #     recipients=[
        #         os.getenv("RECIPIENT_EMAIL")
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

        return jsonify({"message": "Form submitted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occured"}), 400
