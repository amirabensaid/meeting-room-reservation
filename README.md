🏢 Room Reservation Management System
📖 Project Description

This project is a microservices-based system designed to manage the reservation of meeting rooms within a company.
Users (employees, admins, visitors) can view available rooms, make reservations, and manage their bookings easily.
Authentication is handled through OAuth login (e.g., Google Sign-In), ensuring secure and simple access.

The system is built around three key microservices (user-service, salle-service, reservation-service) communicating through Kafka and REST APIs, with PostgreSQL databases for storage.
🚀 How to Run the Project

    Clone the repository

git clone https://github.com/your-username/room-reservation-system.git
cd room-reservation-system

Start Kafka and Zookeeper (for message brokering)
You can use Docker:

docker-compose up -d

Start the databases

    Ensure PostgreSQL is running for each service.

    Apply the database migrations if necessary (SQL scripts provided per service).

Run each microservice

    Navigate into each service directory and start it:

        cd user-service
        npm install
        npm run start

        (Repeat for salle-service and reservation-service.)

    Access the application

        APIs are available locally (e.g., http://localhost:3000, etc.).

        Frontend (if included) can consume these APIs for a complete experience.

🛠️ Services Overview

    user-service

        Handles user authentication and profile management.

        Manages user roles (Admin / Employee / Visitor).

        OAuth 2.0 login integration (Google).

    salle-service

        Manages meeting room information: creation, update, deletion.

        Publishes room availability updates.

    reservation-service

        Handles creating, cancelling, and listing room reservations.

        Ensures a room is available before confirming a reservation.

        Communicates with user-service and salle-service for validations.

🖥️ Technologies Used
Technology	Purpose
Node.js	Backend server for microservices
Express.js	REST APIs for communication
PostgreSQL	Database for each microservice
Kafka	Message brokering between services
OAuth 2.0 (Google)	User authentication and authorization
JWT (JSON Web Token)	Secure communication between services
Docker / Docker-Compose	Running Kafka, Zookeeper, and databases easily
Swagger	API documentation (optional, if you add it)
