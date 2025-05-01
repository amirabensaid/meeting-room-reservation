FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV JWT_SECRET_KEY=your-secret-key-change-in-production

EXPOSE 5001

CMD ["python", "app.py"]
