# 🚗 SmartCarService

A full-stack web application for managing vehicle maintenance and service appointments, developed as a graduation project for the Full-Stack Python Program 2026.

SmartCarService combines a Django web application, PostgreSQL database, role-based access control, and an Agentic AI assistant that can interact with real application services through controlled backend tools.

---

## 📌 Project Overview

SmartCarService provides a centralized platform for managing vehicles, maintenance records, technicians, and service appointments.

The system supports multiple user roles and applies role-based permissions to protect application data and operations.

The project also includes an integrated Agentic AI Assistant. Instead of functioning only as a conversational chatbot, the AI can understand a user's request, select an appropriate backend tool, execute authorized operations, and return the result to the user.

---

## ✨ Key Features

### 🔐 Authentication & RBAC
- User registration and login
- Logout functionality
- Role-Based Access Control (RBAC)
- Customer, Technician, Manager, and Admin roles
- Ownership and assignment-based authorization

### 🚗 Vehicle Management
- Add vehicles
- View vehicles
- Edit vehicle information
- Delete vehicles
- Associate vehicles with their owners

### 🔧 Maintenance Management
- Create maintenance records
- View maintenance history
- Edit maintenance records
- Delete maintenance records
- Maintenance status tracking
- Service date and next service date
- Maintenance cost tracking

### 📅 Appointment Management
- View appointments
- Edit authorized appointments
- Cancel appointments
- Delete authorized appointments
- Appointment status management
- Technician assignment

### 🤖 Agentic AI Assistant
The integrated AI Assistant can:

- Retrieve the authenticated user's vehicles
- Retrieve maintenance history
- Identify due maintenance services
- Retrieve available technicians
- Retrieve available service slots
- Book service appointments
- Cancel appointments after explicit confirmation

The AI uses backend tools instead of directly accessing the database.

### 🛡️ AI Security
- AI requests use the authenticated user's context
- Backend tools perform authorization checks
- User ownership is validated
- Technician assignments are validated
- Tool parameters are validated
- Destructive actions require explicit confirmation

---

## 🧠 Agentic AI Workflow

The AI follows a controlled workflow:

```text
User Request
     ↓
Understand User Goal
     ↓
Select Appropriate Tool
     ↓
Validate User Permissions
     ↓
Execute Backend Tool
     ↓
Interact with Database / Services
     ↓
Observe Result
     ↓
Return Final Response