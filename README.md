# Placement Portal

A comprehensive web application for managing campus placements, connecting students, companies, and administrators in a seamless recruitment process.

## Features

- **User Authentication & Authorization**
  - Role-based access control (Admin, Student, Company)
  - Secure login and registration
  - Password hashing with Werkzeug security

- **Admin Dashboard**
  - User and company management
  - Placement statistics and reports
  - Export functionality for data analysis

- **Company Features**
  - Job posting and management
  - Student applications tracking
  - Resume screening and filtering

- **Student Features**
  - Job search and application submission
  - Profile management
  - Application status tracking
  - Resume upload

- **Cache Management**
  - Optimized performance with Flask caching
  - Faster data retrieval

- **File Management**
  - Resume uploads
  - Export reports

## Tech Stack

### Backend
- **Framework:** Flask
- **Database:** SQLAlchemy ORM
- **Authentication:** Werkzeug Security
- **Email:** Flask-Mail
- **Caching:** Flask-Caching
- **CORS:** Flask-CORS

### Frontend
- **Framework:** Vue.js
- **Build Tool:** (Configured in frontend setup)

## Installation

### Prerequisites
- Python 3.8+
- Node.js & npm
- Virtual Environment

### Backend Setup

1. **Clone the repository**
   ```bash
   cd c:\Users\shiva\OneDrive\Desktop\Placement_Portal_23f1003137
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the backend directory
   - Add database URL, mail configuration, and API keys

5. **Run the application**
   ```bash
   python app.py
   ```
   The backend will start at `http://localhost:5000`

### Frontend Setup
Refer to the frontend directory's README for Vue.js setup and installation.

## Project Structure

```
Placement_Portal_23f1003137/
├── backend_content/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── models.py              # Database models
│   ├── extensions.py          # Flask extensions
│   ├── routes/
│   │   ├── auth.py           # Authentication routes
│   │   ├── admin.py          # Admin routes
│   │   ├── company.py        # Company routes
│   │   └── student.py        # Student routes
│   ├── uploads/              # User file uploads
│   └── exports/              # Generated reports
└── frontend/                 # Vue.js frontend
```

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Admin (`/admin`)
- Manage users and companies
- View statistics

### Company (`/company`)
- Post and manage job listings
- Track applications

### Student (`/student`)
- Browse job postings
- Submit applications
- Manage profile

### File Management
- `GET /uploads/<filename>` - Download uploaded files
- `GET /exports/<filename>` - Download exported reports

## Default Admin Account

The system automatically creates a default admin account on first run:
- **Email:** admin@portal.com
- **Password:** admin123


## Usage

1. **Access the application**
   - Backend API: `http://localhost:5000`
   - Frontend: Configure in Vue.js setup

2. **Login**
   - Use appropriate credentials based on user role
   - Select role: Admin, Student, or Company

3. **Navigate based on role**
   - **Admin:** Manage platform users and statistics
   - **Company:** Post jobs and track applications
   - **Student:** Find jobs and apply

## Configuration

Update `config.py` for:
- Database connection string
- Flask mail server settings
- Secret keys
- Cache settings
- CORS origins

## Requirements

See `requirements.txt` for complete dependencies list.
