# JavaScript Learning Platform

## Overview

This is a comprehensive JavaScript learning platform built with Flask that provides structured lessons, interactive tests, and practical exercises. The platform features a hierarchical content structure (Levels → Sections → Lessons) with admin management capabilities and user progress tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: SQLite (default) with PostgreSQL support via environment configuration
- **Authentication**: Flask-Login for admin authentication with session-based user tracking
- **Forms**: WTForms with Flask-WTF for form handling and validation
- **Template Engine**: Jinja2 templating with Bootstrap 5 frontend

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with custom CSS theming
- **JavaScript**: Vanilla JavaScript for interactivity and theme management
- **Icons**: Font Awesome 6 for consistent iconography
- **Rich Text**: TinyMCE integration for content editing
- **Responsive Design**: Mobile-first approach with dark/light theme support

## Key Components

### Data Models
- **Admin**: User authentication for content management
- **Level**: Top-level course organization (e.g., "JavaScript Basics")
- **Section**: Grouped lessons within levels (e.g., "Introduction to JavaScript")
- **Lesson**: Individual learning units with theory content
- **Question**: Multiple-choice quiz questions for lesson assessment
- **Exercise**: Practical coding exercises (structure defined, implementation pending)
- **UserProgress**: Session-based progress tracking without user registration

### Content Management
- **Admin Dashboard**: Hierarchical content overview with CRUD operations
- **Rich Text Editor**: TinyMCE integration for lesson content creation
- **Ordered Content**: Numeric ordering system for levels, sections, and lessons
- **Cascade Deletion**: Automatic cleanup of related content when parent items are deleted

### User Experience
- **Progress Tracking**: Session-based completion status using UUID sessions
- **Interactive Testing**: Multiple-choice quizzes with scoring (70% passing threshold)
- **Responsive Navigation**: Breadcrumb navigation and tabbed lesson interface
- **Theme System**: Dark/light mode with localStorage persistence

## Data Flow

### Content Creation Flow
1. Admin logs in via `/admin/login`
2. Creates hierarchical content: Level → Section → Lesson
3. Adds theory content, questions, and exercises to lessons
4. Content immediately available to learners

### Learning Flow
1. User browses levels on homepage
2. Selects level → section → lesson progression
3. Studies theory content in tabbed interface
4. Completes quiz questions (if available)
5. Works on practical exercises (if available)
6. Progress tracked via session ID stored in Flask session

### Assessment Flow
1. User takes quiz by answering multiple-choice questions
2. Answers submitted to `/lesson/<id>/test` endpoint
3. Score calculated and stored in UserProgress
4. 70% threshold required for lesson completion
5. Progress reflected in UI with completion badges

## External Dependencies

### Python Packages
- **Flask**: Web framework core
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: Authentication management
- **Flask-WTF**: Form handling and CSRF protection
- **Werkzeug**: Password hashing and WSGI utilities

### Frontend Libraries
- **Bootstrap 5**: UI framework via CDN
- **Font Awesome 6**: Icon library via CDN
- **TinyMCE 6**: Rich text editor via CDN

### Database
- **SQLite**: Default development database
- **PostgreSQL**: Production database (configurable via DATABASE_URL environment variable)

## Deployment Strategy

### Environment Configuration
- **SESSION_SECRET**: Flask session encryption key
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **Debug Mode**: Enabled in development, should be disabled in production

### Database Initialization
- **Automatic Schema**: Tables created on application startup
- **Sample Data**: Initial admin user and content via `init_db.py` script
- **Migration Strategy**: Currently uses SQLAlchemy create_all() (manual migrations needed for production)

### Production Considerations
- **WSGI Setup**: ProxyFix middleware configured for reverse proxy deployment
- **Security**: Environment-based secret key management
- **Database**: Connection pooling and ping configured for reliability
- **Logging**: Debug level logging enabled (should be adjusted for production)

### Default Admin Credentials
- Username: `bodryakov.web`
- Password: `Anna-140275`
(These should be changed immediately in production)