import sqlite3

con = sqlite3.connect("school.sqlite")

cursor = con.cursor()

# замена номера аудитории для определенного курса
""" cursor.executescript('''
    UPDATE class
    SET room = :room
    WHERE course_start_schedule_id = :course_id
''',{"room": "B107", "course_id": 5}) """

#обновление посещаемости для студента
""" cursor.executescript('''
    UPDATE attendance
    SET presence = :presence_number
    WHERE student_id = :student_id
''',{"presence_number":1,"student_id":1}) """

#выбор студента его группы
""" cursor.executescript('''
    SELECT FIO_student, group_name FROM student
    INNER JOIN `group` ON `group`.id_group = student.group_id
    ORDER BY FIO_student
''') """

con.close()