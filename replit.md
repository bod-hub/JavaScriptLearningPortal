# JavaScript Learning Platform

## Overview

This is a comprehensive JavaScript learning platform built with Flask that provides structured lessons, interactive tests, and practical exercises. The platform features a hierarchical content structure (Levels → Sections → Lessons) with admin management capabilities and user progress tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (January 2025)

- **Major Architecture Change**: Converted from dynamic database-driven structure to static HTML pages
- **New Structure**: 4 separate HTML files for each level (level-1.html, level-2.html, level-3.html, level-4.html)
- **Content Organization**: Each level contains 2 sections with 2 lesson cards each
- **Navigation**: Added section navigation with anchor links for easy scrolling
- **Bootstrap**: Maintained Bootstrap 5 for consistent styling
- **Routes**: Updated Flask routes to serve static level pages

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: SQLite (default) with PostgreSQL support via environment configuration
- **Authentication**: Flask-Login for admin authentication with session-based user tracking
- **Forms**: WTForms with Flask-WTF for form handling and validation
- **Template Engine**: Jinja2 templating with Bootstrap 5 frontend

### Frontend Architecture
- **UI Framework**: Pure CSS with custom responsive design (Bootstrap 5 removed)
- **JavaScript**: Vanilla JavaScript for interactivity, theme management, and tab navigation
- **Icons**: Font Awesome 6 for consistent iconography
- **Rich Text**: Quill Editor integration for content editing
- **Responsive Design**: Mobile-first approach with dark/light theme support and CSS Grid layouts

## Key Components

### Content Structure
- **Static Level Pages**: 4 HTML files for each learning level
  - level-1.html: Основы JavaScript (variables, data types)
  - level-2.html: Функции и объекты (functions, objects, arrays)
  - level-3.html: DOM и события (DOM manipulation, events)
  - level-4.html: Продвинутый JS (async programming, modules)
- **Section Navigation**: Each level has internal navigation with anchor links
- **Lesson Cards**: Each section contains lesson cards with theory, questions, and exercises
- **Data Models**: Admin, Level, Section, Lesson, Question, Exercise, UserProgress (maintained for admin functionality)

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
1. User browses 4 levels on homepage with course description section
2. Selects level to access dedicated level page
3. Uses section navigation to jump to specific topics via anchor links
4. Views lesson cards organized by sections
5. Each lesson card shows available content: theory, questions, exercises
6. Static content structure with progress tracking (to be implemented)

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