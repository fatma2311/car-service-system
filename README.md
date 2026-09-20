# 🚗 Smart Car Service & Maintenance System

A full-stack web application for managing vehicle maintenance operations — built as a graduation project for the **Full-Stack Python Program 2026**.

## 📋 Overview

The system helps car service centers manage vehicles, maintenance records, technicians, and appointments — with an **AI-powered agent** that analyzes a vehicle's maintenance history and proactively suggests or schedules upcoming service based on technician and spare-part availability.

## ✨ Key Features

- **Role-Based Access Control (RBAC)** — Admin, Manager, Technician, and Customer roles with distinct permissions
- **Vehicle & Maintenance Tracking** — full service history per vehicle
- **Smart Appointment Scheduling** — availability-aware booking for technicians and parts
- **AI Agent Assistant** — uses tool-calling to query maintenance data, predict upcoming service needs, and assist with scheduling decisions
- **Analytics Dashboard** — service trends, technician workload, and delay rates

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript (ES6) |
| AI | LLM API with function/tool calling |

## 👥 Team

| Name | Role |
|---|---|
| Fatma | Team Lead — Data Models, RBAC, AI Agent |
| Habiba | Frontend, Views, CRUD |

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/<your-username>/car-service-system.git
cd car-service-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

## 📁 Project Structure

```
car-service-system/
├── config/            # Project settings
├── accounts/          # Authentication & RBAC
├── vehicles/          # Vehicle & maintenance models
├── appointments/      # Scheduling logic
├── ai_agent/          # AI agent & tool-calling integration
├── static/
├── templates/
└── requirements.txt
```

## 📄 License

This project is developed for academic purposes as part of the Full-Stack Python Program 2026 graduation requirements.
