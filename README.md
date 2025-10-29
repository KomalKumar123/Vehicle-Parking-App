# 🚗 Vehicle Parking System

A **full-stack vehicle parking management system** built using **Flask (Backend)** and **Vue.js (Frontend)**.  
The system supports **Admin** and **User** roles, real-time parking spot updates, and asynchronous background jobs for reports and notifications.

---

## 👨‍💻 Author

**Name:** Komal Kumar  
**Roll Number:** 24f1001472  
**Email:** [24f1001472@ds.study.iitm.ac.in](mailto:24f1001472@ds.study.iitm.ac.in)  

**About Me:**  
I’m a passionate developer with a keen interest in building full-stack web applications.  
I enjoy tackling challenges related to system architecture, database design, and creating seamless user experiences.

---

## 📝 Project Description

This project implements a **comprehensive vehicle parking management system** with a clear separation between the backend (Flask REST API) and the frontend (Vue.js SPA).  

Key highlights:
- Two distinct roles: **Admin** and **User**
- Real-time parking spot tracking
- Asynchronous background jobs (Celery + Redis)
- Secure authentication and role-based authorization
- Exportable booking reports

> 💡 Approximately 40% of the code was generated using an AI assistant for initial setup, database modeling, and component scaffolding.

---

## 🛠️ Technologies Used

### Backend (Flask)
- **Flask** – Core REST API framework  
- **Flask-SQLAlchemy** – ORM for database modeling  
- **Flask-JWT-Extended** – JWT-based authentication  
- **Flask-Bcrypt** – Secure password hashing  
- **Celery** – Distributed task queue for background jobs  
- **Redis** – Message broker for Celery tasks  

### Frontend (Vue.js)
- **Vue.js 3** – Reactive frontend framework  
- **Vue Router** – Client-side navigation  
- **Pinia** – State management  
- **Axios** – HTTP client for API calls  
- **Bootstrap 5** – Responsive UI styling  

---

## 🗄️ Database Schema Design

The database consists of **four main tables**, ensuring normalized structure and referential integrity.

### 1. `users`
| Column | Type | Description |
|---------|------|-------------|
| id | Integer (PK) | Unique user identifier |
| username | String | User’s display name |
| email | String | Used for login |
| password_hash | String | Securely hashed password |
| role | String | `'user'` or `'admin'` |

### 2. `parking_lots`
| Column | Type | Description |
|---------|------|-------------|
| id | Integer (PK) | Unique lot ID |
| name | String | Public name of the lot |
| address | Text | Physical address |
| pin_code | String | Postal code |
| price_per_hour | Float | Hourly parking rate |
| capacity | Integer | Total parking spots |

### 3. `parking_spots`
| Column | Type | Description |
|---------|------|-------------|
| id | Integer (PK) | Unique spot ID |
| spot_number | Integer | Spot number within the lot |
| status | String | `'Available'` or `'Occupied'` |
| lot_id | Integer (FK) | References `parking_lots.id` |

### 4. `bookings`
| Column | Type | Description |
|---------|------|-------------|
| id | Integer (PK) | Booking transaction ID |
| user_id | Integer (FK) | References `users.id` |
| spot_id | Integer (FK) | References `parking_spots.id` |
| park_in_time | DateTime | Start time |
| park_out_time | DateTime | End time |
| cost | Float | Final parking cost |

**Design rationale:**  
Bookings are separated from `parking_spots` to maintain a historical log of transactions while keeping spot status simple and real-time.

---

## 🌐 API Design

The REST API is modular and organized using **Flask Blueprints**.

### 🔐 Authentication (`/auth`)
- `POST /register` – Register a new user  
- `POST /login` – Authenticate and issue JWT  

### 👤 User API (`/api`)
- View parking lots  
- Book/release parking spots  
- View booking history  
> All routes require a valid `'user'` JWT token.

### 🧑‍💼 Admin API (`/admin`)
- Full CRUD for parking lots  
- Monitor users and parking spot status  
> All routes protected by a custom `@admin_required` decorator.

---

## 🏗️ Architecture and Features

### 🧩 Project Structure
vehicle-parking-system/
│
├── backend/
│ ├── routes/
│ ├── models/
│ ├── tasks/
│ ├── config.py
│ └── app.py
│
└── frontend/
├── src/
│ ├── views/
│ ├── components/
│ ├── router/
│ ├── store/
│ └── services/


### ⚙️ Key Features
- **Role-Based Access Control:** Secure endpoints for admins and users  
- **Parking Lifecycle:** Book, release, and view active spots  
- **Admin Dashboard:** Manage lots and monitor live status  
- **Background Jobs:**
  - Async CSV export of booking history  
  - Scheduled reports and reminders via Celery Beat  
- **Booking History:** Full transaction records for users and admins  

---

## 🎥 Demo Video

▶️ **[Watch the demo here](https://drive.google.com/file/d/1-LRzg2nhqFBk73qizOass4SRWXo-pviQ/view?usp=sharing)**

---

## 📄 License

This project is developed as part of academic coursework at **IIT Madras (BS Program)**.  
Use, modification, and distribution should comply with institutional policies.
