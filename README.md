
# 🧩 Microservices Booking Platform

This project is a containerized microservices-based booking system with CI/CD, monitoring, and cloud deployment. It includes three main services:

- 🧍 **User Service** (port `5000`)
- 🛏️ **Room Service** (port `5001`)
- 📅 **Reservation Service** (port `5002`)

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions
- **Deployment**: Render (container deployment)

---

## 🧱 Architecture Overview

```

```
        ┌────────────────────────────┐
        │        Ingress (Nginx)     │
        └────────────┬───────────────┘
                     │
 ┌───────────────────┼────────────────────┐
 │                   │                    │
```

┌────▼────┐        ┌─────▼─────┐        ┌─────▼─────┐
│ user    │        │ room      │        │ reservation│
│ service │        │ service   │        │ service    │
└─────────┘        └───────────┘        └────────────┘
│                   │                    │
└───────────────────┴────────────────────┘
│
┌──────────▼──────────┐
│     Prometheus      │
└──────────┬──────────┘
│
┌─────▼─────┐
│  Grafana  │
└───────────┘

````

---

## 🚀 Setup & Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
````

2. **Build Docker images**:

   ```bash
   docker build -t user-service ./user-service
   docker build -t room-service ./room-service
   docker build -t reservation-service ./reservation-service
   ```

3. **Start Kubernetes cluster** (with Minikube or similar), then:

   ```bash
   kubectl apply -f k8s/
   ```

4. **Access services**:

   * User Service: `/users`
   * Room Service: `/rooms`
   * Reservation Service: `/reservations`

---

## 📦 CI/CD with GitHub Actions

* **Trigger**: On push or pull request to `main`.
* **Steps**:

  1. Run `pytest` for each service.
  2. Build Docker images with Buildx.
  3. Deploy each service to Render using API key from GitHub secrets.

### Secrets Used:

| Key              | Purpose                       |
| ---------------- | ----------------------------- |
| `HEROKU_API_KEY` | *Not used in final version*   |
| `dep`            | Render API key for deployment |

---

## 📊 Monitoring with Prometheus & Grafana

### Prometheus Configuration:

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'user-service'
    static_configs:
      - targets: ['user-service:5000']
  - job_name: 'room-service'
    static_configs:
      - targets: ['room-service:5001']
  - job_name: 'reservation-service'
    static_configs:
      - targets: ['reservation-service:5002']
```

### Grafana Dashboard:

* **Panel**: Average Response Time
* **PromQL**:

  ```promql
  rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
  ```
* **Alert**: Triggers if avg response time > 5s for 5 minutes

---

## 🚢 Deployment to Render

Each service is deployed as a container using `render container:push` and `render container:release`.

Update service names and environment as needed:

```bash
render container:push web --service user-service --env production
render container:release web --service user-service --env production
```

---

## 🔐 Environment Variables

Each service uses a shared JWT key:

```env
JWT_SECRET_KEY=your_jwt_key_here
```



https://www.figma.com/design/ekCsGVCh0N0NoAq0x1WHy0/Meeting-Room--Community-?node-id=0-1&t=NJbjaqBdkk6wSAHC-1

![image](https://github.com/user-attachments/assets/ced3af18-a9a9-4712-9f9b-2fa10e5c207a)

![image](https://github.com/user-attachments/assets/07b3437b-8eb2-4a06-bf5e-6046589d246e)

![image](https://github.com/user-attachments/assets/9327536a-f9ee-4550-8688-09c033bb801d)

![image](https://github.com/user-attachments/assets/d7b18f23-d04f-4378-8bde-ebb34105380a)

![image](https://github.com/user-attachments/assets/38218cfc-8a53-40fc-88ce-503a0cdb85e5)

![image](https://github.com/user-attachments/assets/dd586293-0b3f-409a-8e92-e4cc2fe24af8)

---

## ✅ To-Do / Future Improvements

* Add healthcheck (`/health`) endpoints for each service
* Use Kubernetes secrets for secure config
* Add frontend / gateway if needed
* Add database persistence layer (PostgreSQL, etc.)

---

## 🤝 Contributing

Feel free to fork the repo and submit PRs or issues!

---

## 📄 License

MIT License. See `LICENSE` file.

```

---

Let me know if you’d like this translated into French or want to add a frontend section too!
```
