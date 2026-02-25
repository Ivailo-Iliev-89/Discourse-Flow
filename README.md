# Django Blog Engine

### A Secure, Content-Driven Platform with Nested Discussions
**Django Blog Engine** is a full featured content management system, designed for personal storytelling.
It focuses on robust authorization logic, dynamic media handling, and an interactive commenting system to showcase clean full-stack development patterns.

## Key Technical Features
- **Authorization**: Implemented custom `LoginRequiredMixin` and `UserPassesTestMixin` to ensure strict object-level permissions, allowing only authors to manage their own content.
- **Commenting System**: Built a hierarchical discussion engine that supports nested replies, enhancing user engagement.
- **Automated Media Management**: Integrated dynamic image handling for blog posts with automated cleanup and storage patterns.
- **Responsive Architecture**: Crafted a sleek, card-based UI using Bootstrap 5, focusing on modular CSS for maintainability and scalability.
- **CRUD Logic**: Full lifecycle management for blog entries, from draft creation to secure deletion.
  
## Tech Stack
- **Backend**: Python, Django
- **Frontend**: HTML, Custom CSS, JavaScript (ES6+), Bootstrap 5
- **Database**: SQLite (Development) / PostgreSQL (Ready)
- **Authentication**: Django Built-in Auth System

## Instructions to setup

- Clone the repository:
- ```bash
- git clone https://github.com/ivailoiliev89-netizen/Blog-Project.git
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## What I Learned 

- **Mixins & Reusability**: Used Django Mixins to reduce code duplication in Class-Based Views.
- **Media Handling**: Managing the lifecycle of user-uploaded files and media root configurations.
- **Relational Mapping**: Designing complex self-referencing relationships for the commenting system.
