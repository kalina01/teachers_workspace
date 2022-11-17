import sqlite3

DB_PATH = 'school.sqlite'

con = sqlite3.connect(DB_PATH)

#Заполнение таблицы teacher
con.executescript('''
    INSERT INTO teacher (FIO_teacher, telnumber_teacher)
    VALUES
    ('Иванов Иван Иванович','+79996543423'),
    ('Степанов Степан Степанович','+79670900021'),
    ('Евгеньева Евгения Евгеньевна','+74563634587'),
    ('Якимов Яким Якимович','+72346642831'),
    ('Викторов Виктор Викторович','+74438872385');
''')

#Заполнение таблицы course
con.executescript('''
    INSERT INTO course (name)
    VALUES
    ('Математика ЕГЭ профиль'),
    ('Математика ЕГЭ база'),
    ('Математика ОГЭ'),
    ('Русский язык для иностранцев'),
    ('Программирование для школьников'),
    ('Английский язык ЕГЭ');
''')

#Заполнение таблицы teacher_course
con.executescript('''
    INSERT INTO teacher_course (teacher_id, course_id)
    VALUES
    (1,1),
    (1,2),
    (1,3),
    (2,4),
    (3,5),
    (4,7),
    (4,8),
    (5,6);
''')


#Заполнение таблицы qroup
con.executescript('''
    INSERT INTO `group` (group_name)
    VALUES
    ('Мат 10'),
    ('Мат 11'),
    ('Мат 9'),
    ('Прог 8'),
    ('Англ 10');
''')

#Заполнение таблицы student
con.executescript('''
    INSERT INTO student (group_id, FIO_student, telnumber_student)
    VALUES
    (1,'Тимофеева Ольга Владимировна','+76543457698'),
    (1,'Жаров Арсений Алексеевич','+72346545654'),
    (1,'Алексеева Алёна Егоровна','+78876654676'),
    (1,'Иванов Артём Иванович','+75457653454'),
    (1,'Щербакова Александра Максимовна','+77653454565'),
    (1,'Осипова Анастасия Александровна','+79987765676'),
    (2,'Вишневский Владимир Максимович','+71124432365'),
    (2,'Соколов Илья Сергеевич','+78887654535'),
    (2,'Зыков Илья Михайлович','+79764563476'),
    (2,'Маслова Арина Кирилловна','+72345547656'),
    (2,'Пахомов Юрий Михайлович','+78763345465'),
    (3,'Ильина Карина Марковна','+77763345465'),
    (3,'Кравцова Майя Петровна','+78764456523'),
    (3,'Горячев Александр Евгеньевич','+79874567634'),
    (4,'Леонов Александр Григорьевич','+78088870956'),
    (4,'Васильева Дарина Артёмовна','+77650076708'),
    (4,'Матвеева Эмилия Данииловна','+73480070001'),
    (5,'Яковлева Полина Эминовна','+73458865908'),
    (5,'Козлова Анастасия Никитична','+74568859706');
''')

#Заполнение таблицы course_start_schedule
con.executescript('''
    INSERT INTO course_start_schedule 
    (group_id, teacher_course_id, start_date, price, period, week_amount)
    VALUES
    (1, 1, '2022-09-01', 500, 2, 24),
    (2, 1, '2022-09-01', 500, 2, 24),
    (3, 3, '2022-09-01', 500, 2, 24),
    (4, 5, '2022-09-05', 650, 3, 20),
    (5, 6, '2022-09-05', 650, 3, 20);
''')

#Заполнение таблицы class с триггером
con.executescript('''
    CREATE TRIGGER create_class
    AFTER INSERT ON course_week
    BEGIN	
	    INSERT INTO class (course_start_schedule_id, `date`)
	    SELECT 
		    course_start_schedule_id, 
		    d as `date`
	    FROM (
		    WITH RECURSIVE recursive_table AS (
			    SELECT 
				    Date((SELECT start_date FROM course_start_schedule WHERE course_start_schedule_id = new.course_start_schedule_id), '+' || ((7 - strftime('%w', (SELECT start_date FROM course_start_schedule WHERE course_start_schedule_id = new.course_start_schedule_id)) + new.day_id) % 7) || ' days')
					    AS d,
				    new.course_start_schedule_id 
					    AS course_start_schedule_id
			    UNION ALL
			    SELECT 
				    Date(d, '+7 days'),
				    new.course_start_schedule_id 
					    AS course_start_schedule_id
			    FROM recursive_table
			    WHERE d < Date((SELECT start_date FROM course_start_schedule WHERE course_start_schedule_id = new.course_start_schedule_id), '+' || ((SELECT week_amount FROM course_start_schedule WHERE course_start_schedule_id = new.course_start_schedule_id) * 7) || ' days')
		    )
		    SELECT * FROM recursive_table
	    )
	    JOIN course_start_schedule USING(course_start_schedule_id)
	    WHERE course_start_schedule_id = new.course_start_schedule_id;	
    END;   
''')

#Заполнение таблицы course_week
con.executescript('''
    INSERT INTO course_week (day_id, course_start_schedule_id)
    VALUES
    (2,1),
    (6,1),
    (2,2),
    (6,2),
    (3,3),
    (6,3),
    (1,4),
    (3,4),
    (5,4),
    (2,5),
    (4,5),
    (6,5);
''')

#Заполнение аудиторий в таблице class
con.executescript('''
    UPDATE class
    SET room = "B323"
    WHERE course_start_schedule_id = 1
''')
con.executescript('''
    UPDATE class
    SET room = "D555"
    WHERE course_start_schedule_id = 2
''')
con.executescript('''
    UPDATE class
    SET room = "D733"
    WHERE course_start_schedule_id = 3
''')
con.executescript('''
    UPDATE class
    SET room = "G303"
    WHERE course_start_schedule_id = 4
''')
con.executescript('''
    UPDATE class
    SET room = "B107"
    WHERE course_start_schedule_id = 5
''')

#Заполнение таблицы attendance
con.executescript('''
    INSERT INTO attendance (student_id, class_id)
    SELECT id_student AS student_id, class_id FROM student
    INNER JOIN course_start_schedule
    ON student.group_id = course_start_schedule.group_id
    JOIN class USING(course_start_schedule_id)
    ORDER BY id_student
''')


con.commit()
con.close()