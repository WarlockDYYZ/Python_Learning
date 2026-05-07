from Some_Projects.Student_Performance_Management_System.student import Student
from Some_Projects.Student_Performance_Management_System.school import School
from Some_Projects.Student_Performance_Management_System.course import Course
from Some_Projects.Student_Performance_Management_System.grade import Grade


# 创建学校实例
school = School()

# 添加课程
courses = [
    Course("C001", "数学", 4),
    Course("C002", "英语", 3),
    Course("C003", "计算机基础", 4),
    Course("C004", "Python编程", 3)
]
for course in courses:
    school.add_course(course)

# 添加学生
students = [
    Student("S001", "Alice"),
    Student("S002", "Bob"),
    Student("S003", "Charlie"),
    Student("S004", "David")
]
for student in students:
    school.add_student(student)

# 录入成绩
grades = [
    Grade(students[0], courses[0], 95),  # Alice 数学 95分
    Grade(students[0], courses[1], 88),  # Alice 英语 88分
    Grade(students[0], courses[2], 92),  # Alice 计算机基础 92分
    Grade(students[0], courses[3], 98),  # Alice Python编程 98分
    Grade(students[1], courses[0], 85),  # Bob 数学 85分
    Grade(students[1], courses[1], 78),  # Bob 英语 78分
    Grade(students[1], courses[2], 88),  # Bob 计算机基础 88分
    Grade(students[1], courses[3], 82),  # Bob Python编程 82分
    Grade(students[2], courses[0], 90),  # Charlie 数学 90分
    Grade(students[2], courses[1], 85),  # Charlie 英语 85分
    Grade(students[2], courses[2], 90),  # Charlie 计算机基础 90分
    Grade(students[2], courses[3], 88),  # Charlie Python编程 88分
    Grade(students[3], courses[0], 75),  # David 数学 75分
    Grade(students[3], courses[1], 80),  # David 英语 80分
    Grade(students[3], courses[2], 78),  # David 计算机基础 78分
    Grade(students[3], courses[3], 85),  # David Python编程 85分
]

# 显示系统信息
school.list_students()
school.list_courses()

# 计算班级平均分
class_avg = school.calculate_class_average()
print(f"班级平均GPA: {class_avg:.2f}")
print()

# 查询特定学生信息
student_id = "S001"
student = school.find_student_by_id(student_id)
if student:
    print(f"查询学生：{student}")
    print("成绩详情：")
    for grade in student.grades:
        print(f"  - {grade.course}: {grade.score}分")
    print(f"GPA: {student.calculate_gpa():.2f}")
