#!/usr/bin/env python3
"""
Database initialization script for JavaScript Learning Platform
"""

from werkzeug.security import generate_password_hash
from app import app, db
from models import Admin, Level, Section, Lesson, Question, Exercise

def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        admin = Admin.query.filter_by(username='bodryakov.web').first()
        if not admin:
            admin = Admin(
                username='bodryakov.web',
                password_hash=generate_password_hash('Anna-140275')
            )
            db.session.add(admin)
            
        # Create sample content
        level1 = Level.query.filter_by(title='Основы JavaScript').first()
        if not level1:
            level1 = Level(
                title='Основы JavaScript',
                description='Изучение базовых концепций языка JavaScript',
                order=1
            )
            db.session.add(level1)
            db.session.flush()  # Get the ID
            
            # Add sections to level 1
            section1 = Section(
                title='Введение в JavaScript',
                description='Первое знакомство с языком программирования JavaScript',
                order=1,
                level_id=level1.id
            )
            db.session.add(section1)
            db.session.flush()
            
            # Add lesson to section 1
            lesson1 = Lesson(
                title='Что такое JavaScript?',
                theory_content='''
                <h2>Что такое JavaScript?</h2>
                <p>JavaScript — это высокоуровневый язык программирования, который изначально был создан для создания интерактивных веб-страниц. Сегодня JavaScript используется не только в браузере, но и на серверах, в мобильных приложениях и даже в настольных программах.</p>
                
                <h3>Основные особенности JavaScript:</h3>
                <ul>
                    <li><strong>Динамическая типизация</strong> — тип переменной определяется во время выполнения</li>
                    <li><strong>Интерпретируемый язык</strong> — код выполняется построчно без предварительной компиляции</li>
                    <li><strong>Прототипное наследование</strong> — объекты могут наследовать свойства от других объектов</li>
                    <li><strong>Функции первого класса</strong> — функции могут храниться в переменных и передаваться как параметры</li>
                </ul>
                
                <h3>Где используется JavaScript?</h3>
                <p>Современный JavaScript можно использовать для:</p>
                <ul>
                    <li>Создания интерактивных веб-сайтов</li>
                    <li>Разработки веб-приложений (React, Vue, Angular)</li>
                    <li>Серверной разработки (Node.js)</li>
                    <li>Мобильной разработки (React Native, Ionic)</li>
                    <li>Настольных приложений (Electron)</li>
                </ul>
                
                <h3>Первый пример кода</h3>
                <pre><code>// Это комментарий в JavaScript
console.log("Привет, мир!");

// Объявление переменной
let message = "Добро пожаловать в мир JavaScript!";
console.log(message);</code></pre>
                ''',
                order=1,
                section_id=section1.id
            )
            db.session.add(lesson1)
            db.session.flush()
            
            # Add questions to lesson 1
            questions_data = [
                {
                    'text': 'Что такое JavaScript?',
                    'option_a': 'Язык разметки для создания веб-страниц',
                    'option_b': 'Высокоуровневый язык программирования',
                    'option_c': 'База данных для веб-приложений',
                    'option_d': 'Графический редактор',
                    'correct_answer': 'B'
                },
                {
                    'text': 'Какая особенность НЕ характерна для JavaScript?',
                    'option_a': 'Динамическая типизация',
                    'option_b': 'Интерпретируемый язык',
                    'option_c': 'Статическая типизация',
                    'option_d': 'Прототипное наследование',
                    'correct_answer': 'C'
                },
                {
                    'text': 'Где НЕ может использоваться JavaScript?',
                    'option_a': 'В веб-браузере',
                    'option_b': 'На сервере',
                    'option_c': 'В мобильных приложениях',
                    'option_d': 'В микроволновой печи',
                    'correct_answer': 'D'
                }
            ]
            
            for i, q_data in enumerate(questions_data):
                question = Question(
                    text=q_data['text'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    lesson_id=lesson1.id,
                    order=i + 1
                )
                db.session.add(question)
            
            # Add exercises to lesson 1
            exercise1 = Exercise(
                title='Вывод сообщения в консоль',
                description='Напишите код, который выводит в консоль сообщение "Я изучаю JavaScript!"',
                solution='console.log("Я изучаю JavaScript!");',
                lesson_id=lesson1.id,
                order=1
            )
            db.session.add(exercise1)
            
            exercise2 = Exercise(
                title='Создание переменной',
                description='''Создайте переменную с именем "name" и присвойте ей ваше имя, 
                затем выведите это значение в консоль.''',
                solution='''let name = "Ваше имя";
console.log(name);''',
                lesson_id=lesson1.id,
                order=2
            )
            db.session.add(exercise2)
            
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")
        print("Admin login: bodryakov.web")
        print("Admin password: Anna-140275")

if __name__ == '__main__':
    init_database()
