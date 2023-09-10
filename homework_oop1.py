from statistics import mean


class Student:
    student_list = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.student_list.append(self)

    def get_raitings(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached \
                and course in self.courses_in_progress and 0 < grade <= 10:
            if course not in lecturer.marks:
                lecturer.marks[course] = [grade]
            else:
                lecturer.marks[course].append(grade)
        else:
            print('Неверный ввод данных!')

    def average_marks(self):  # Находим среднюю оценку по всем курсам
        summ_marks = 0
        count_marks = 0
        for lst in self.grades.values():
            summ_marks += sum(lst)
            count_marks += len(lst)
        if count_marks != 0:
            return summ_marks / count_marks
        else:
            return None

    def __str__(self):
        return (
            f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.average_marks()}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def __eq__(self, other):
        if not isinstance(other, Student):
            raise TypeError('Операнд справа должен иметь тип Lecturer')
        return self.average_marks() == other.average_marks()

    def __lt__(self, other):
        if not isinstance(other, Student):
            raise TypeError('Операнд справа должен иметь тип Lecturer')
        return self.average_marks() < other.average_marks()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    lecturers_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.marks = {}
        Lecturer.lecturers_list.append(self)

    def average_marks(self):  # Найдем среднюю оценку по всем курсам
        summ_marks = 0
        count_marks = 0
        for lst in self.marks.values():
            summ_marks += sum(lst)
            count_marks += len(lst)
        if count_marks != 0:
            return summ_marks / count_marks
        else:
            return None

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_marks()}'

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError('Операнд справа должен иметь тип Lecturer')
        return self.average_marks() == other.average_marks()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError('Операнд справа должен иметь тип Lecturer')
        return self.average_marks() < other.average_marks()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Неверный ввод данных!')

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def average_studentmarks_for_cours(students: list, cours: str):
    count = 0
    summ = 0
    for student in students:
        if not isinstance(student, Student):
            raise TypeError('Список должен содержать только объекты типа "Student"')
        if cours in student.grades:
            summ += mean(student.grades[cours])
            count += 1
    return summ / count


def average_lectormarks_for_cours(lecturers: list, cours: str):
    count = 0
    summ = 0
    for lecturer in lecturers:
        if not isinstance(lecturer, Lecturer):
            raise TypeError('Список должен содержать только объекты типа "Lecturer"')
        if cours in lecturer.marks:
            summ += mean(lecturer.marks[cours])
            count += 1
    return summ / count

# test
student1 = Student('Dwayne', 'Johnson', 'man')
student2 = Student('Jennifer', 'Aniston', 'woman')
student1.finished_courses.append('Git')
student2.finished_courses.append('Java')
student1.courses_in_progress = ['Python', 'Django', 'Flask', 'React', 'Sql']
student2.courses_in_progress = ['Python', 'Django', 'Flask', 'React', 'Sql', 'API']

lector1 = Lecturer('Pavel', 'Durov')
lector2 = Lecturer('Evgeniy', 'Kaspersky')
lector1.courses_attached = ['Python', 'Django', 'Flask']
lector2.courses_attached = ['Python', 'React', 'Sql', 'API']

student1.get_raitings(lector1, 'Python', 10)
student1.get_raitings(lector1, 'Python', 8)
student1.get_raitings(lector1, 'Django', 4)
student1.get_raitings(lector1, 'Django', 6)
print(lector1)

student2.get_raitings(lector2, 'React', 10)
student2.get_raitings(lector2, 'Sql', 8)
student2.get_raitings(lector2, 'API', 4)
student2.get_raitings(lector2, 'React', 2)
student2.get_raitings(lector2, 'Python', 2)

print('-' * 10)
print(lector2)
print(lector2 < lector1)
print(lector2 == lector1)
print(lector2 > lector1)

reviewer1 = Reviewer('Al', 'Sweigart')
reviewer2 = Reviewer('Michael', 'Dawson')
reviewer1.courses_attached = ['Python', 'Django', 'Flask', 'React']
reviewer2.courses_attached = ['Python', 'Django', 'Flask', 'React', 'API']
reviewer1.rate_hw(student1, 'Python', 2)
reviewer1.rate_hw(student1, 'Python', 4)
reviewer1.rate_hw(student1, 'Django', 3)
reviewer1.rate_hw(student1, 'Django', 3)
reviewer1.rate_hw(student1, 'Django', 2)
reviewer2.rate_hw(student2, 'API', 5)
reviewer2.rate_hw(student2, 'Django', 5)
reviewer2.rate_hw(student2, 'Python', 5)
reviewer2.rate_hw(student2, 'Python', 5)
print(student1.grades)
print(student2.grades)
print(student1)
print('-' * 10)
print(student2)
print(student1 == student2)
print(student1 < student2)

student3 = Student('Bill', 'Lubanovic', 'man')
student3.courses_in_progress = ['Python', 'Django', 'Flask', 'React', 'Sql', 'API']
reviewer2.rate_hw(student3, 'API', 2)
reviewer2.rate_hw(student3, 'Django', 3)
reviewer2.rate_hw(student3, 'Python', 3)
reviewer2.rate_hw(student3, 'Python', 2)

print(student1.grades)
print(student2.grades)
print(student3.grades)
print(average_studentmarks_for_cours(Student.student_list, 'Python'))

print(lector1.marks)
print(lector2.marks)
print(average_lectormarks_for_cours(Lecturer.lecturers_list, 'Python'))