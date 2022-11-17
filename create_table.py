import os
import sqlite3

DB_PATH = 'school.sqlite'
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

con = sqlite3.connect("school.sqlite")
con.executescript('''
-- -----------------------------------------------------
-- Table `teacher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `teacher` (
  `id_teacher` INTEGER PRIMARY KEY AUTOINCREMENT,
  `FIO_teacher` VARCHAR(80) NOT NULL,
  `telnumber_teacher` VARCHAR(15) NOT NULL
  );

  -- -----------------------------------------------------
-- Table `course`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `course` (
  `id_course` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(60) NOT NULL
  );


-- -----------------------------------------------------
-- Table `group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `group` (
  `id_group` INTEGER PRIMARY KEY AUTOINCREMENT,
  `group_name` VARCHAR(60) NOT NULL
  );


-- -----------------------------------------------------
-- Table `student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `student` (
  `id_student` INTEGER PRIMARY KEY AUTOINCREMENT,
  `group_id` INTEGER NOT NULL,
  `FIO_student` VARCHAR(80) NOT NULL,
  `telnumber_student` VARCHAR(15) NOT NULL,
  CONSTRAINT student_group_fk
    FOREIGN KEY (`group_id`)
    REFERENCES `group` (`id_group`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
    );


-- -----------------------------------------------------
-- Table `teacher_course`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `teacher_course` (
  `teacher_course_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `teacher_id` INTEGER NOT NULL,
  `course_id` INTEGER NOT NULL,
  CONSTRAINT teacher_course_fk_teacher
    FOREIGN KEY (`teacher_id`)
    REFERENCES `teacher` (`id_teacher`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT teacher_course_fk_course
    FOREIGN KEY (`course_id`)
    REFERENCES `course` (`id_course`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
    );


-- -----------------------------------------------------
-- Table `course_start_schedule`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `course_start_schedule` (
  `course_start_schedule_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `group_id` INTEGER NOT NULL,
  `teacher_course_id` INTEGER NOT NULL,
  `start_date` DATETIME NOT NULL,
  `price` DECIMAL NULL,
  `period` INTEGER NOT NULL,
  `week_amount` INTEGER NOT NULL,
  CONSTRAINT course_start_schedule_fk_teacher_course
    FOREIGN KEY (`teacher_course_id`)
    REFERENCES `teacher_course` (`teacher_course_id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT course_start_schedule_fk_group
    FOREIGN KEY (`group_id`)
    REFERENCES `group` (`id_group`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
    );

-- -----------------------------------------------------
-- Table course_week
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS course_week (
  `course_week_id` INTEGER PRIMARY KEY,
  `day_id` INTEGER NOT NULL,
  `course_start_schedule_id` INTEGER NOT NULL,
  CONSTRAINT course_week_fk_course_start_schedule
    FOREIGN KEY (`course_start_schedule_id`)
    REFERENCES `course_start_schedule` (`course_start_schedule_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
    );

-- -----------------------------------------------------
-- Table `class`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `class` (
  `class_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `course_start_schedule_id` INTEGER NOT NULL,
  `date` DATETIME NOT NULL,
  `room` VARCHAR(5),
  CONSTRAINT class_fk_course_start_schedule
    FOREIGN KEY (`course_start_schedule_id`)
    REFERENCES `course_start_schedule` (`course_start_schedule_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
    );


-- -----------------------------------------------------
-- Table `attendance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attendance` (
  `attendance_id` INTEGER PRIMARY KEY,
  `class_id` INTEGER NOT NULL,
  `presence` INTEGER,
  `student_id` INTEGER NOT NULL,
  CONSTRAINT attendance_fk_class
    FOREIGN KEY (`class_id`)
    REFERENCES `class` (`class_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT attendance_fk_student
    FOREIGN KEY (`student_id`)
    REFERENCES `student` (`id_student`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
    );

''')
con.commit()
con.close()
