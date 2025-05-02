🏢 Room Reservation Management System
📖 Project Description

This project is a microservices-based system designed to manage the reservation of meeting rooms within a company.
Users (employees, admins, visitors) can view available rooms, make reservations, and manage their bookings easily.
Authentication is handled through OAuth login (e.g., Google Sign-In), ensuring secure and simple access.
Figma Template : 
https://www.figma.com/design/ekCsGVCh0N0NoAq0x1WHy0/Meeting-Room--Community-?node-id=0-1&t=NJbjaqBdkk6wSAHC-1

![image](https://github.com/user-attachments/assets/ced3af18-a9a9-4712-9f9b-2fa10e5c207a)

![image](https://github.com/user-attachments/assets/07b3437b-8eb2-4a06-bf5e-6046589d246e)

![image](https://github.com/user-attachments/assets/9327536a-f9ee-4550-8688-09c033bb801d)

![image](https://github.com/user-attachments/assets/d7b18f23-d04f-4378-8bde-ebb34105380a)

![image](https://github.com/user-attachments/assets/38218cfc-8a53-40fc-88ce-503a0cdb85e5)

![image](https://github.com/user-attachments/assets/dd586293-0b3f-409a-8e92-e4cc2fe24af8)



The system is built around three key microservices (user-service, salle-service, reservation-service) communicating through Kafka and REST APIs, with PostgreSQL databases for storage.
🚀 How to Run the Project

    Clone the repository

git clone https://github.com/your-username/room-reservation-system.git
cd room-reservation-system

Start Kafka and Zookeeper (for message brokering)
You can use Docker:

docker-compose up -d

Run each microservice

    Navigate into each service directory and start it:

        cd user-service
        npm install
        npm run start

        (Repeat for salle-service and reservation-service.)

    Access the application

        APIs are available locally (e.g., http://localhost:5000,5001,5002 etc.).


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
