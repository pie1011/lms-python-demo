# LMS Platform - Django Learning Management System

> **Portfolio Project by Katie Harshman**  
> A comprehensive Learning Management System showcasing modern Django development, database design, and production deployment skills.

🔗 **Live Demo:** [https://lms-python-demo.onrender.com](https://lms-python-demo.onrender.com)

**My Portfolio:** [https://katieharshman.com](https://katieharshman.com)


## 🎭 Try the Demo!

**Experience the full admin interface with read-only access:**

**Username:** `PortfolioDemo`  
**Password:** `ViewOnly123`

**Try the Student Portal:**

- **Username:** `demo_employee` 
- **Password:** `training123`
- **Access:** [Student Portal Login](https://lms-python-demo.onrender.com/student/login/)

*Click anywhere, explore all features - the interface works perfectly but no data is modified for demonstration safety!*

---

## 🚀 Project Overview

This LMS Platform demonstrates professional Django development skills through a complete academic management system. Built with modern web technologies and deployed to production, it showcases complex database relationships, role-based authentication, beautiful UI design, and real-world business logic implementation.

## ✨ Key Features Completed

### 🎨 Modern User Interface
- **Beautiful Landing Page** - Modern design with animations and glassmorphism effects
- **Custom Admin Dashboard** - Real-time statistics, quick actions, and responsive cards
- **Styled Admin Interface** - Professional forms, tables, and navigation
- **Mobile-Responsive Design** - Works seamlessly across all devices

### 🔐 Authentication & Security
- **Role-Based Access Control** - Students, Instructors, and Administrators with appropriate permissions
- **Demo User System** - Safe portfolio exploration without data modification
- **Secure Password Management** - Django's built-in authentication with custom extensions
- **Production Security** - Environment variables, secure deployment practices

### 📚 Academic Management
- **Course Structure** - Hierarchical organization: Courses → Modules → Assignments
- **User Management** - Complete lifecycle from registration to role assignment
- **Enrollment System** - Student-course relationships with grade tracking
- **Assignment Workflow** - Creation, submission, grading, and feedback loop
- **Grade Tracking** - Individual assignment grades with course-level aggregation

### 🛠️ Technical Excellence
- **Database Design** - Complex relationships with data integrity constraints
- **Django Admin Customization** - Custom admin site with real-time data integration
- **Template Architecture** - Clean inheritance structure with reusable components
- **Static File Management** - Organized CSS/JS with production optimization
- **Management Commands** - Automated setup and demo data generation

### 🚀 Production Deployment
- **Live Production Site** - Deployed on Render with PostgreSQL database
- **Automated Deployment** - GitHub integration with automatic builds
- **Environment Management** - Secure configuration for development and production
- **Static File Serving** - WhiteNoise integration for efficient asset delivery

## 🔧 Technology Stack

- **Backend:** Django 5.2.2 with PostgreSQL
- **Frontend:** HTML5, Modern CSS3, Vanilla JavaScript
- **Deployment:** Render Platform with automated GitHub integration
- **Database:** PostgreSQL (production), SQLite (development)
- **Server:** Gunicorn WSGI server
- **Static Files:** WhiteNoise for production serving

## 📊 Database Architecture

The system implements a comprehensive academic data model with proper relationships:

```
Users (Django Auth) ←→ UserProfile (roles)
     ↓
Course → Module → Assignment → Submission
     ↓              ↓
Enrollment ←→ Student    Student
```

### Key Relationships
- **Courses** contain multiple **Modules** (organized learning content)
- **Modules** contain multiple **Assignments** (tasks and assessments)
- **Students** enroll in **Courses** (many-to-many via Enrollments table)
- **Assignments** receive **Submissions** from students (one-to-many)
- **Submissions** include grades and instructor feedback

## 🎯 Skills Demonstrated

### Django Framework Mastery
- **Advanced Models** - Complex relationships, custom fields, data validation
- **Custom Admin Interface** - Tailored admin experience with real-time data
- **Authentication System** - Role-based permissions and user management
- **Template System** - Inheritance, custom tags, and reusable components
- **URL Routing** - Clean URLs with permission-based access control

### Database & Backend Development
- **Schema Design** - Normalized database with appropriate relationships
- **Data Integrity** - Constraints, validation, and error handling
- **Query Optimization** - Efficient database access patterns
- **Migration Management** - Version-controlled schema changes

### Frontend & User Experience
- **Responsive Design** - Mobile-first approach with modern CSS
- **User Interface Design** - Intuitive navigation and beautiful forms
- **Animation & Interactivity** - Smooth transitions and engaging elements
- **Accessibility** - Semantic HTML and keyboard navigation support

### DevOps & Production
- **Deployment Pipeline** - Automated builds and deployments
- **Environment Configuration** - Secure secrets management
- **Database Management** - Production PostgreSQL setup
- **Performance Optimization** - Static file compression and caching

## 🚀 Quick Start

### Demo Access (Recommended)
1. Visit [https://lms-python-demo.onrender.com](https://lms-python-demo.onrender.com)
2. Click "Admin" or go to `/admin/`
3. Login with: `PortfolioDemo` / `ViewOnly123`
4. Explore all features safely!

### Local Development
```bash
# Clone the repository
git clone https://github.com/pie1011/lms-python.git
cd lms-python

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py setup_production    # Creates sample data
python manage.py create_demo_user     # Creates demo account

# Run development server
python manage.py runserver
```

## 🎨 Screenshots & Features

### Admin Dashboard
- **Real-time Statistics**: Live user counts, course metrics, submission tracking
- **Quick Actions**: Direct links to create courses, users, and enrollments
- **Beautiful Cards**: Modern design with hover effects and meaningful data
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile

### Course Management
- **Hierarchical Structure**: Courses contain modules, modules contain assignments
- **Role-Based Access**: Instructors see only their courses, students see enrollments
- **Rich Content**: Full-featured forms with date/time pickers and validation
- **File Upload Ready**: Architecture prepared for assignment file submissions

### User Experience
- **Intuitive Navigation**: Clean sidebar with logical organization
- **Professional Forms**: Beautiful styling with proper validation feedback
- **Search & Filtering**: Find courses, users, and assignments quickly
- **Demo Mode**: Safe exploration for portfolio viewers

## 📈 Project Impact

This LMS Platform demonstrates:

### Business Value
- **Educational Technology** - Addresses real-world needs in academic institutions
- **Scalable Architecture** - Designed to handle growth from small schools to universities
- **User-Centered Design** - Intuitive interfaces that reduce training time
- **Data-Driven Insights** - Analytics foundation for educational improvement

### Technical Excellence
- **Production-Ready Code** - Follows Django best practices and security guidelines
- **Maintainable Architecture** - Clean separation of concerns and documented codebase
- **Performance Considerations** - Optimized queries and efficient asset delivery
- **Security Implementation** - Proper authentication, authorization, and data protection

## 🔮 Future Enhancements

### Phase 1: Student & Instructor Portals
- **Student Dashboard** - Course enrollment, assignment submission, grade viewing
- **Instructor Interface** - Course management, grading tools, student progress tracking
- **File Upload System** - Assignment submissions and course materials

### Phase 2: Advanced Features
- **Grade Calculations** - Automated GPA tracking and weighted assignments
- **Calendar Integration** - Due date tracking and scheduling tools
- **Email Notifications** - Alerts for assignments, grades, and announcements
- **Analytics Dashboard** - Course performance metrics and reporting tools

### Phase 3: Scaling & Optimization
- **API Development** - RESTful API for mobile app integration
- **Advanced Permissions** - Fine-grained access control and approval workflows
- **Performance Optimization** - Caching, pagination, and query optimization
- **Testing Suite** - Comprehensive unit and integration tests

## 👩‍💻 About This Project

This Learning Management System was built as a portfolio project to demonstrate full-stack Django development capabilities. It showcases:

- **Real-world application development** - Practical business logic and user workflows
- **Modern web development practices** - Responsive design, clean code, documentation
- **Production deployment skills** - Live site with proper DevOps practices
- **Problem-solving ability** - Complex database relationships and user experience design

The project emphasizes clean, maintainable code and demonstrates the ability to build production-ready applications that solve real business problems.

---

## 🔗 Links

- **Live Demo:** [https://lms-python-demo.onrender.com](https://lms-python-demo.onrender.com)
- **Demo Credentials:** `PortfolioDemo` / `ViewOnly123`
- **GitHub Repository:** [https://github.com/pie1011/lms-python-demo](https://github.com/pie1011/lms-python-demo)
- **Developer Portfolio:** [https://katieharshman.com](https://katieharshman.com)

---

**Built with ❤️ by Katie Harshman**  
*Demonstrating modern Django development with beautiful design, production deployment, and thoughtful user experience.*