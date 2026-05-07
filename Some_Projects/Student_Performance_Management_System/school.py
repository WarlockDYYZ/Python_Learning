from Some_Projects.Student_Performance_Management_System.student import Student
from Some_Projects.Student_Performance_Management_System.course import Course


class School:
    def __init__(self):
        self.students = []  # 所有学生
        self.courses = []  # 所有课程

    def add_student(self, student: Student):
        """添加学生"""
        self.students.append(student)

    def add_course(self, course: Course):
        """添加课程"""
        self.courses.append(course)

    def calculate_class_average(self):
        """计算班级平均分"""
        if not self.students:
            return 0.0
        total_gpa = 0.0
        for student in self.students:
            total_gpa += student.calculate_gpa()
        return total_gpa / len(self.students)

    def find_student_by_id(self, student_id):
        """根据学号查找学生"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def list_students(self):
        """列出所有学生信息"""
        print("=== 学生列表 ===")
        # 遍历 self.students 这个可迭代对象（列表 / 元组等）
        # 同时给出 序号 + 元素，并且序号从 1 开始（默认从 0 开始）
        for i, student in enumerate(self.students, 1):
            gpa = student.calculate_gpa()
            print(f"{i}. {student} - GPA: {gpa:.2f}")
        print()

    def list_courses(self):
        """列出所有课程信息"""
        print("=== 课程列表 ===")
        for i, course in enumerate(self.courses, 1):
            print(f"{i}. {course}")
        print()
