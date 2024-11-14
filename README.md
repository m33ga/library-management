
# Library Management System

A web application designed to manage library book reservations and loans, making it easier for library members to search, reserve, and borrow books. Library staff can use the system to manage inventory and monitor reservations, improving the efficiency of library operations.

## Project Overview

This Library Management System provides the following core functionalities:

- **User Authentication**: Secure login for members and staff using JWT authentication.
- **Book Search and Reservation**: Users can search for books, reserve them, and view their status.
- **Queue Management**: If a book is already reserved, users can join a queue.
- **Notifications**: Users receive updates about reservation availability, due dates, and overdue books.
- **Fine Management**: Automated fines for overdue books, viewable by members and managed by staff.
- **Admin Dashboard**: Provides administrators with tools to manage books, track loans, and view library usage reports.

## Tools and Technologies Used

- **Backend**: Django REST Framework for API development.
- **Database**: PostgreSQL to store and manage library data.
- **Message Broker**: RabbitMQ for handling notifications and asynchronous events.
- **Containerization**: Docker to run each component in isolated containers.

---