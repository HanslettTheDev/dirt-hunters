review_data = [
    {
        "name": "Sarah Johnson",
        "rating": 5,
        "title": "Exceptional Service!",
        "content": "The team did an amazing job cleaning my apartment. It's spotless and smells fantastic!",
        "date": "October 15, 2023",
    },
    {
        "name": "Michael Thompson",
        "rating": 4,
        "title": "Great Deep Cleaning",
        "content": "They did a thorough deep cleaning of our house before we moved in. Very satisfied with the results.",
        "date": "October 10, 2023",
    },
    {
        "name": "Emily Rodriguez",
        "rating": 5,
        "title": "Regular Customer",
        "content": "I've been using SparkleClean for my monthly cleaning for over a year now. Consistent quality every time.",
        "date": "October 5, 2023",
    },
]

from dirt_hunters import create_app
from dirt_hunters.extensions import db
from dirt_hunters.models.models import Reviews

app = create_app()


def seed_reviews():
    for r in review_data:
        review = Reviews(
            name=r["name"],
            rating=r["rating"],
            review_title=r["title"],
            review_content=r["content"],
        )

        db.session.add(review)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_reviews()
