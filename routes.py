from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import Admin, Level, Section, Lesson, Question, Exercise, UserProgress
from forms import LoginForm, LevelForm, SectionForm, LessonForm, QuestionForm, ExerciseForm
import uuid


@app.route('/')
def index():
    levels = Level.query.order_by(Level.order).all()
    return render_template('index.html', levels=levels)


@app.route('/level/<int:level_id>')
def level_detail(level_id):
    level = Level.query.get_or_404(level_id)
    sections = Section.query.filter_by(level_id=level_id).order_by(Section.order).all()
    return render_template('level.html', level=level, sections=sections)


@app.route('/section/<int:section_id>')
def section_detail(section_id):
    section = Section.query.get_or_404(section_id)
    lessons = Lesson.query.filter_by(section_id=section_id).order_by(Lesson.order).all()
    
    # Get user progress
    session_id = session.get('user_session')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['user_session'] = session_id
    
    progress = {}
    for lesson in lessons:
        user_progress = UserProgress.query.filter_by(
            session_id=session_id, 
            lesson_id=lesson.id
        ).first()
        progress[lesson.id] = user_progress.completed if user_progress else False
    
    return render_template('section.html', section=section, lessons=lessons, progress=progress)


@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    exercises = Exercise.query.filter_by(lesson_id=lesson_id).order_by(Exercise.order).all()
    
    # Get user progress
    session_id = session.get('user_session')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['user_session'] = session_id
    
    user_progress = UserProgress.query.filter_by(
        session_id=session_id, 
        lesson_id=lesson_id
    ).first()
    
    return render_template('lesson.html', lesson=lesson, exercises=exercises, progress=user_progress)


@app.route('/lesson/<int:lesson_id>/test')
def lesson_test(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    questions = Question.query.filter_by(lesson_id=lesson_id).order_by(Question.order).all()
    
    if not questions:
        flash('Для этого урока нет тестовых вопросов.', 'info')
        return redirect(url_for('lesson_detail', lesson_id=lesson_id))
    
    return render_template('test.html', lesson=lesson, questions=questions)


@app.route('/lesson/<int:lesson_id>/submit_test', methods=['POST'])
def submit_test(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    
    session_id = session.get('user_session')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['user_session'] = session_id
    
    # Calculate score
    correct_answers = 0
    total_questions = len(questions)
    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer == question.correct_answer:
            correct_answers += 1
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Update or create progress record
    user_progress = UserProgress.query.filter_by(
        session_id=session_id, 
        lesson_id=lesson_id
    ).first()
    
    if user_progress:
        user_progress.test_score = score
        user_progress.completed = score >= 70  # 70% to pass
    else:
        user_progress = UserProgress(
            session_id=session_id,
            lesson_id=lesson_id,
            test_score=score,
            completed=score >= 70
        )
        db.session.add(user_progress)
    
    db.session.commit()
    
    flash(f'Тест завершен! Ваш результат: {score:.1f}% ({correct_answers}/{total_questions})', 
          'success' if score >= 70 else 'warning')
    
    return redirect(url_for('lesson_detail', lesson_id=lesson_id))


# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('admin/login.html', form=form)


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin_dashboard():
    levels = Level.query.order_by(Level.order).all()
    return render_template('admin/dashboard.html', levels=levels)


@app.route('/admin/lesson/<int:lesson_id>/edit')
@login_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    questions = Question.query.filter_by(lesson_id=lesson_id).order_by(Question.order).all()
    exercises = Exercise.query.filter_by(lesson_id=lesson_id).order_by(Exercise.order).all()
    return render_template('admin/edit_lesson.html', lesson=lesson, questions=questions, exercises=exercises)


@app.route('/admin/lesson/<int:lesson_id>/update', methods=['POST'])
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    lesson.title = request.form.get('title')
    lesson.theory_content = request.form.get('theory_content')
    
    # Update questions
    Question.query.filter_by(lesson_id=lesson_id).delete()
    
    question_texts = request.form.getlist('question_text')
    for i, text in enumerate(question_texts):
        if text.strip():
            question = Question(
                text=text,
                option_a=request.form.getlist('option_a')[i],
                option_b=request.form.getlist('option_b')[i],
                option_c=request.form.getlist('option_c')[i],
                option_d=request.form.getlist('option_d')[i],
                correct_answer=request.form.getlist('correct_answer')[i],
                lesson_id=lesson_id,
                order=i + 1
            )
            db.session.add(question)
    
    # Update exercises
    Exercise.query.filter_by(lesson_id=lesson_id).delete()
    
    exercise_titles = request.form.getlist('exercise_title')
    exercise_descriptions = request.form.getlist('exercise_description')
    exercise_solutions = request.form.getlist('exercise_solution')
    
    for i, title in enumerate(exercise_titles):
        if title.strip():
            exercise = Exercise(
                title=title,
                description=exercise_descriptions[i] if i < len(exercise_descriptions) else '',
                solution=exercise_solutions[i] if i < len(exercise_solutions) else '',
                lesson_id=lesson_id,
                order=i + 1
            )
            db.session.add(exercise)
    
    db.session.commit()
    flash('Урок успешно обновлен!', 'success')
    return redirect(url_for('edit_lesson', lesson_id=lesson_id))


@app.route('/admin/level/new', methods=['GET', 'POST'])
@login_required
def new_level():
    form = LevelForm()
    if form.validate_on_submit():
        level = Level(
            title=form.title.data,
            description=form.description.data,
            order=form.order.data
        )
        db.session.add(level)
        db.session.commit()
        flash('Новый уровень создан!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_lesson.html', form=form, title='Новый уровень')


@app.route('/admin/section/new', methods=['GET', 'POST'])
@login_required
def new_section():
    form = SectionForm()
    form.level_id.choices = [(l.id, l.title) for l in Level.query.order_by(Level.order).all()]
    
    if form.validate_on_submit():
        section = Section(
            title=form.title.data,
            description=form.description.data,
            order=form.order.data,
            level_id=form.level_id.data
        )
        db.session.add(section)
        db.session.commit()
        flash('Новый раздел создан!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_lesson.html', form=form, title='Новый раздел')


@app.route('/admin/lesson/new', methods=['GET', 'POST'])
@login_required
def new_lesson():
    form = LessonForm()
    form.section_id.choices = [(s.id, f"{s.level.title} - {s.title}") for s in Section.query.join(Level).order_by(Level.order, Section.order).all()]
    
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            theory_content=form.theory_content.data,
            order=form.order.data,
            section_id=form.section_id.data
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Новый урок создан!', 'success')
        return redirect(url_for('edit_lesson', lesson_id=lesson.id))
    return render_template('admin/edit_lesson.html', form=form, title='Новый урок')
