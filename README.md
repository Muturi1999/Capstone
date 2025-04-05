# Event Management API

A full-featured Event Management API built with Django and Django REST Framework (DRF). This project allows users to manage events, register, book seats, join waitlists, and more — with secure JWT authentication and a fully interactive Swagger UI for API testing.

## Project Overview

This backend project simulates a real-world event management platform. It provides:

- User management with roles (Admin, Organizer, Attendee)
- Event CRUD operations
- Booking & waitlist system
- Feedback and calendar sync
- JWT-based authentication
- Swagger documentation

---

 <!-- Live API Documentation -->

<!-- Base URL:   -->
http://127.0.0.1:8000/api/

<!-- Swagger UI:  -->
http://127.0.0.1:8000/swagger/?format=openapi


Explore all API endpoints and test them in-browser!


 <!-- Technology Stack -->

- Python 3.x
- Django
- Django REST Framework (DRF)
- Simple JWT
- drf-yasg (Swagger)
- PostgreSQL

 <!-- Project Structure -->

event_management/
├── events/                   
├── users/                    
├── templates/                
├── celery/                   
├── event_management_api/     
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env                    
├── manage.py              
├── pytest.ini                
├── requirements.txt       
├── README.md
└── venv/                     


<!-- !-- Setup Instructions --> -->

<!-- 1. Clone the Repository -->

git clone https://github.com/muturi1999/event-management-api.git

cd event-management-api

<!-- 2. Create a Virtual Environment -->

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

<!-- 3. Install Dependencies -->
pip install -r requirements.txt

 <!-- 4. Create and confidure database i.e mysql, postgres -->
 update data base configuration on env enviroment variables

<!-- 5. Set up email configuration  -->
configure email 

<!-- 6. Apply Migrations -->
python3 manage.py makemigrations
python3 manage.py migrate

<!-- 7. Running Tests -->
python3 manage.py test

<!-- 8. Access the API Docs -->
http://127.0.0.1:8000/swagger/?format=openapi



<!-- list of api and endpoints -->
<!-- Authentication & User Management -->

- Register a new user 
  `POST /users/api/register/`

- Log in and obtain JWT access and refresh tokens 
  `POST /users/api/login/`

- Log out the currently authenticated user 
  `POST /users/api/logout/`

- Obtain a new JWT token pair  
  `POST /users/api/token/`

- Refresh your access token using a valid refresh token  
  `POST /users/api/token/refresh/`

- Request a password reset email 
  `POST /users/api/request-password-reset/`

- Reset password using a secure token and user ID 
  `POST /users/api/reset-password/{uid}/{token}/`

- Assign a role to a user (Admin, Organizer) 
  `POST /users/api/user/{id}/assign-role/`

- Verify email using a token   
  `GET /users/api/verify-email/`


 <!-- Event Management -->

- List all events  
  `GET /events/`

- Create a new event (Organizer only)  
  `POST /events/`

- **List only upcoming events  
  `GET /events/list/`

- Retrieve a specific event by ID 
  `GET /events/{id}/`

- Update an existing event (Organizer only)  
  `PUT /events/{id}/`

- Delete an event (Organizer only)
  `DELETE /events/{id}/`

 <!-- Bookings & Waitlists -->

- Book an event
  `POST /events/{event_id}/book/`

-Cancel your existing booking for an event  
  `DELETE /events/{event_id}/cancel-booking/`

- Join the waitlist if the event is full  
  `POST /events/{event_id}/join-waitlist/`



<!-- Feedback & Calendar Sync -->

- Leave feedback for a specific event
  `POST /events/{event_id}/feedback/`

- Sync the event with an external calendar 
  `POST /events/{event_id}/sync/`

