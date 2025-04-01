# Event Management API

## Project Overview
The Event Management API is a scalable and secure RESTful API built with Django REST Framework (DRF) and PostgreSQL. It allows users to create, manage, and book events, implementing role-based access control (RBAC), JWT authentication, event notifications, filtering, pagination, and recurring events.

## Features
- **User Authentication & Management**
  - JWT-based authentication
  - User registration, login, and email confirmation
  - User profile management
  - Role-based access control (Admin, Organizer, Attendee)

- **Event Management**
  - Create, update, delete events (Admin/Organizer only)
  - List all events with pagination & filtering
  - View event details
  - Recurring events (weekly/monthly)

- **Event Booking & RSVP**
  - Book an event
  - Cancel bookings
  - View booked events
  - Waitlist for fully booked events

- **Search & Filtering**
  - Search by title, location, date range
  - Pagination for large datasets

- **Notifications & Feedback**
  - Email notifications for upcoming events
  - User feedback for past events

- **Calendar Integration**
  - Add events to Google Calendar

- **API Documentation**
  - Swagger UI for interactive testing

## Technologies Used
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** JWT (Django Simple JWT)
- **Email Service:** SMTP (Configured via .env)
- **Documentation:** Swagger UI
- **Environment Management:** Python-dotenv

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/event-management-api.git
cd event-management-api
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and configure the following:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://organizer:Mike_12#$@localhost:5432/eventmanagementapi
EMAIL_HOST=smtp.yourmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints

### 1. User Authentication & Management
| Endpoint | Method | Access |
|----------|--------|--------|
| /api/register/ | POST | Public |
| /api/token/ | POST | Public |
| /api/token/refresh/ | POST | Public |
| /api/confirm-email/?token=<token> | GET | Public |
| /api/user/profile/ | GET/PUT | Authenticated Users |

### 2. Event Management
| Endpoint | Method | Access |
|----------|--------|--------|
| /api/events/ | POST | Admin Only |
| /api/events/ | GET | Public |
| /api/events/{id}/ | GET | Public |
| /api/events/{id}/ | PUT | Organizer Only |
| /api/events/{id}/ | DELETE | Organizer Only |

### 3. Event Booking & RSVP
| Endpoint | Method | Access |
|----------|--------|--------|
| /api/events/{id}/book/ | POST | Authenticated Users |
| /api/events/{id}/cancel-booking/ | DELETE | Authenticated Users |
| /api/user/booked-events/ | GET | Authenticated Users |

### 4. Admin & Role-Based Access
| Endpoint | Method | Access |
|----------|--------|--------|
| /api/user/{id}/assign-role/ | PATCH | Admin Only |

### 5. Event Filtering & Search
| Endpoint | Method | Access |
|----------|--------|--------|
| /api/events/?title=<>&location=<>&date_from=<>&date_to=<> | GET | Public |
| /api/events/upcoming/ | GET | Public |

## Testing the API
Run tests to verify functionality:
```bash
python manage.py test
```
