# Triply – Smart Travel Itinerary & Budget Planner

## Project Overview
Travellers struggle with scattered tools for itineraries, budgets, maps, and documents, causing stress and overspending. Triply unifies day-wise itineraries, budget tracking, interactive maps, document storage, and travel tools—making journeys organized, efficient, and collaborative.  

---

## Technical Implementation

- **Backend:** Django (v5.2.3), Django REST Framework (v3.16.0)  
- **Database:** PostgreSQL (v17.5)  

---

## Django Apps

- `accounts` → Handles user registration, authentication, and profile management  
- `trips` → Manages trips and participants  
- `itineraries` → Handles day-wise itineraries and activities  
- `budgets` → Manages trip budgets and expense tracking  
- `documents` → Stores uploaded trip-related files  
- `collaboration` → Handles co-editing and trip sharing  

---

## API Endpoints

- `api/v1/auth/` → Authentication & user management  
- `api/v1/trips/` → Trip management  
- `api/v1/itineraries/` → Itinerary management  
- `api/v1/budgets/` → Budget tracking  
- `api/v1/documents/` → Document storage and management  
- `api/v1/collaboration/` → Trip collaboration and sharing

---

## Database Tables

### Main Tables (created from your models)

| Table Name | Model | Purpose |
|------------|-------|---------|
| `users` | `User` | Stores user info (email login, profile, phone, bio, etc.) |
| `trips` | `Trip` | Stores trips created by users |
| `expenses` | `Expense` | Stores expense records (amount, category, paid_by, trip, date, receipt, etc.) |
| `budgets` | `Budget` | Stores budget info for a trip |
| `itineraries` | `Itinerary` | Stores day-wise schedules and activities |
| `documents` | `Document` | Stores uploaded files for trips |
| `collaboration` | `Collaboration` | Stores trip sharing info / co-editing details |

### Automatically Created Tables by Django

| Table Name | Reason |
|------------|--------|
| `expenses_split_between` | Many-to-Many table linking `Expense` ↔ `User` for `split_between` field |
| `auth_group`, `auth_permission` | Django’s built-in permission system |
| `django_migrations` | Tracks migrations applied |
| `django_content_type` | Used internally by Django for generic relations |
| `sessions` | Stores session data (if `django.contrib.sessions`) |
| `admin_log` | Tracks admin actions (if `django.contrib.admin`) |
| Any other ManyToMany intermediate tables | For example, `trips_trip_participants` for `Trip.participants` |

> **Note:** Tables like `expenses_split_between` are automatically generated to handle ManyToMany relationships in PostgreSQL.


