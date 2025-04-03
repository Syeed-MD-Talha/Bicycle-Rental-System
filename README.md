# Bicycle Rental System

A Django-based web application for managing bicycle rentals. This system allows users to rent bicycles, manage inventory, and handle rental transactions efficiently.

## Features

- User authentication and authorization
- Bicycle inventory management
- Rental booking system
- Email notifications
- Admin dashboard
- Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Installation

1. Clone the repository (if using Git):
```bash
git clone <repository-url>
cd Bicycle-Rental-System
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# Linux/Mac
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with the following content:
```
EMAIL=your-email@gmail.com
PASSWORD=your-app-specific-password
```

Note: For Gmail, you'll need to use an App Password instead of your regular password. You can generate one in your Google Account settings under Security > 2-Step Verification > App passwords.

## Database Setup

1. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

3. Access the admin dashboard at:
```
http://127.0.0.1:8000/admin/
```

## Project Structure

```
Bicycle-Rental-System/
├── bicycle_rental/     # Main project directory
├── rental/            # Main application directory
├── media/            # User-uploaded files
├── templates/        # HTML templates
├── manage.py        # Django management script
├── requirements.txt # Project dependencies
└── .env            # Environment variables
```

## Dependencies

- Django 5.1.7
- Pillow 11.2.0
- python-dotenv 1.1.0
- Other dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.

## Acknowledgments

- Django framework and its contributors
- All other open-source libraries used in this project 