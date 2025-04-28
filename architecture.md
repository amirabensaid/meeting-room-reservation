Architecture du projet de Gestion de Réservations de Salles
1. Liste des Microservices
Microservice	Fonction principale
User-Service	Gère les utilisateurs : inscription, connexion OAuth, gestion des rôles (Admin, Employé, Visiteur).
Salle-Service	Gère les salles : création, mise à jour, suppression, et affichage des disponibilités.
Reservation-Service	Gère les réservations : réserver une salle, annuler une réservation, consulter l'historique.
2. Interaction entre Microservices

    Communication via Kafka pour les événements importants (par exemple : lorsqu'un utilisateur réserve ou annule une salle).

    API Gateway :

        Reçoit toutes les requêtes des clients.

        Redirige vers le bon microservice (User, Salle ou Reservation).

    Flux d’exemple :

        Un utilisateur se connecte → API Gateway → User-Service.

        Il consulte les salles disponibles → API Gateway → Salle-Service.

        Il fait une réservation → API Gateway → Reservation-Service → Kafka notifie Salle-Service pour mettre à jour la disponibilité.

3. Structure de la Base de Données (PostgreSQL)

(Chaque microservice a sa propre base de données séparée.)
User-Service Database (users table)
Champ	Type	Description
id	UUID (Primary Key)	Identifiant unique utilisateur
email	VARCHAR	Email de l'utilisateur
name	VARCHAR	Nom complet
role	VARCHAR	Rôle (Admin / Employé / Visiteur)
created_at	TIMESTAMP	Date de création
Salle-Service Database (rooms table)
Champ	Type	Description
id	UUID (Primary Key)	Identifiant unique salle
name	VARCHAR	Nom de la salle
capacity	INTEGER	Capacité de la salle
available	BOOLEAN	Disponibilité (true/false)
created_at	TIMESTAMP	Date de création
Reservation-Service Database (reservations table)
Champ	Type	Description
id	UUID (Primary Key)	Identifiant unique réservation
user_id	UUID (Foreign Key vers users.id)	Utilisateur qui réserve
room_id	UUID (Foreign Key vers rooms.id)	Salle réservée
reservation_date	DATE	Date de la réservation
created_at	TIMESTAMP	Date de création
4. Flux d’authentification de base

    Inscription/Connexion :

        L'utilisateur se connecte via Google OAuth.

        OAuth renvoie un token (JWT).

        Le token est stocké côté client et envoyé dans chaque requête.

    Vérification :

        Chaque requête passe par l'API Gateway.

        Le Gateway vérifie le token avec le User-Service avant de rediriger vers les autres services.

    Gestion des permissions :

        Le rôle (Admin/Employé/Visiteur) est inclus dans le token JWT.

        Les microservices vérifient le rôle pour autoriser ou non certaines actions (par exemple, seul un Admin peut créer une salle).

🎯 Résumé rapide

    3 microservices séparés : User, Salle, Reservation.

    Communication entre services par Kafka.

    API Gateway pour centraliser les appels.

    OAuth + JWT pour l'authentification sécurisée.

    3 bases de données simples et indépendantes.

    Docker et Kubernetes pour le déploiement et la scalabilité.
