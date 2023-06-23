# Event Management App

The Event Management App is a web application that allows users to manage and participate in various events. It provides functionality for both administrators and regular users, allowing them to create, view, and book tickets for events. This README provides an overview of the project and instructions for setting up and running the application.

## Features

- Admin Features:
  - Create new events
  - Update event details
  - View event summaries
  - Set maximum available seats for events
  - Define booking open window for events

- User Features:
  - View upcoming events
  - Book tickets for events
  - View booked tickets
  - View all registered events chronologically

## Technologies Used

- Python: The programming language used for the backend development.
- Django: A Python web framework used for building the application.
- Django Rest Framework: A powerful and flexible toolkit for building Web APIs.
- PostgreSQL: The chosen database management system for data storage.
- Docker: Used for containerization of the application.

## Getting Started

To run the Event Management App locally, follow these steps:


   ```bash
   git clone https://github.com/your-username/event-management-app.git
   cd eventmanagementproject
   
   python -m venv myenv
   source myenv/bin/activate
 
   pip install -r requirements.txt
   
   python manage.py migrate
   
   python manage.py runserver
   
   python manage.py test
   
   for coverage:
   coverage report
   
   ````
## For Docker
   ```bash
     docker compose up
   ```



    

