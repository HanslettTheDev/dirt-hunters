Based on the codebase context, you're asking for a README document for the **Dirt Hunters Cleaning Services** Flask web application located in the `HanslettTheDev/dirt-hunters` repository <cite/>. This is a Flask-based web application that uses SQLite for data persistence and Microsoft Graph API for email functionality [1](#0-0) .

# Dirt Hunters Cleaning Services - Local Installation Guide

## Prerequisites

Before starting, ensure you have the following installed <cite/>:
- Python 3.8 or higher
- pip package manager  
- Git for version control
- A Microsoft Azure account with Graph API access (for email functionality)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/HanslettTheDev/dirt-hunters.git
cd dirt-hunters
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it [2](#0-1) :

```bash
cp .env.example .env
```

Edit the `.env` file with your actual values:

```env
SQLALCHEMY_DATABASE_URI=sqlite:///hunters.db
CLIENT_ID=your-azure-client-id
CLIENT_SECRET=your-azure-client-secret
TENANT_ID=your-azure-tenant-id
MAIL_USERNAME=business@company.com
AUTHORITY=https://login.microsoftonline.com/{TENANT_ID}
SCOPE=["https://graph.microsoft.com/.default"]
```

The application automatically detects the environment and loads the appropriate `.env` file [3](#0-2) .

### 5. Database Setup

Initialize the database with sample data using the provided seeding script [4](#0-3) :

```bash
python seed_reviews.py
```

This script will:
- Drop existing tables
- Create new database tables  
- Populate sample customer reviews

### 6. Run the Application

Start the Flask development server [1](#0-0) :

```bash
python main.py
```

The application will be available at `http://localhost:5000`.

## Application Structure

The application uses Flask's application factory pattern [1](#0-0) :

- **Entry Point**: `main.py` imports and runs the Flask app
- **Application Factory**: `dirt_hunters.create_app()` handles initialization
- **Database**: SQLite database (`hunters.db`) with SQLAlchemy ORM
- **Email**: Microsoft Graph API integration for contact form submissions [5](#0-4) 
- **Frontend**: Jinja2 templates with responsive design and JavaScript form handling

## Key Features

- **Homepage**: Single-page application with service showcase, company information, and customer reviews [6](#0-5) 
- **Contact Form**: Asynchronous form submission with email notifications
- **Review System**: Customer review display and submission functionality
- **Responsive Design**: Mobile-optimized interface

## Verification

After setup, verify your installation:

1. **Database**: Confirm `hunters.db` file exists in your project directory
2. **Web Interface**: Navigate to `http://localhost:5000` to see the homepage
3. **Reviews**: Verify that seeded reviews appear in the reviews section
4. **Contact Form**: Test the quote request form (requires Azure configuration)

## Troubleshooting

- **Missing Environment Variables**: Ensure all required variables in `.env` are configured
- **Database Errors**: Re-run `python seed_reviews.py` to reset the database
- **Email Issues**: Verify Microsoft Azure Graph API credentials are correct
- **Port Conflicts**: Flask's default port 5000 may conflict with other services

## Notes

The application includes a comprehensive seeding script that populates the database with sample customer reviews [7](#0-6) . The email functionality requires proper Microsoft Azure configuration for the contact form to work correctly [8](#0-7) . The application uses environment detection to automatically load the correct configuration based on the deployment context [3](#0-2) .

Wiki pages you might want to explore:
- [Getting Started (HanslettTheDev/dirt-hunters)](/wiki/HanslettTheDev/dirt-hunters#2)
- [Application Architecture (HanslettTheDev/dirt-hunters)](/wiki/HanslettTheDev/dirt-hunters#3)
- [Frontend (HanslettTheDev/dirt-hunters)](/wiki/HanslettTheDev/dirt-hunters#4)

### Citations

**File:** main.py (L1-3)
```python
from dirt_hunters import create_app

app = create_app()
```

**File:** dirt_hunters/config.py (L6-11)
```python
if "liveconsole" in gethostname():
    project_folder = os.path.expanduser("~/dirt-hunters")
    load_dotenv(os.path.join(project_folder, ".env"))
else:
    load_dotenv()

```

**File:** seed_reviews.py (L1-23)
```python
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
```

**File:** seed_reviews.py (L45-49)
```python
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_reviews()
```

**File:** dirt_hunters/mails.py (L10-15)
```python
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
```

**File:** dirt_hunters/mails.py (L37-69)
```python
def send_email_via_graph_api(subject, recipients, body, content_type="text"):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": content_type,
                "content": body,
            },
            "from": {
                "emailAddress": {
                    "address": MAIL_USERNAME,
                }
            },
            "toRecipients": recipients,
        }
    }
    user_endpoint = f"https://graph.microsoft.com/v1.0/users/{MAIL_USERNAME}/sendMail"
    response = requests.post(
        user_endpoint, headers=headers, data=json.dumps(email_data)
    )

    if response.status_code != 202:
        raise Exception(
            f"Error sending Email: {response.status_code} - {response.text}"
        )

    return response.status_code
```

**File:** dirt_hunters/core/routes.py (L12-15)
```python
@core.route("/", methods=["GET", "POST"])
def index():
    reviews = db.session.execute(db.select(Reviews)).scalars()
    return render_template("index.html", reviews=reviews)
```
