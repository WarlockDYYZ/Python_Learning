from Some_Projects.Student_Performance_Management_System.student import Student
from Some_Projects.Student_Performance_Management_System.course import Course


class Grade:
    def __init__(self, student: Student, course: Course, score: float):
        self.student = student
        self.course = course
        self.score = score
        # 将成绩添加到学生的成绩列表中
        # student.add_grade(self) 就是把当前创建的 Grade 实例，添加到传入的那个学生的 grades 列表中
        student.add_grade(self)

    def __str__(self):
        return f"{self.student} - {self.course}: {self.score}分"
