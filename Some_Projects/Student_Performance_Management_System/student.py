class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = []  # 存储该学生的所有成绩

    def add_grade(self, grade):
        """添加成绩"""
        self.grades.append(grade)

    def calculate_gpa(self):
        """计算GPA（简化版）"""
        # 计算当前学生所有课程的总 GPA （加权平均分）
        total_credit = 0
        total_score = 0
        for grade in self.grades:
            # 计算总分
            total_credit += grade.course.credit
            # 计算加权学分
            total_score += grade.score * grade.course.credit
        if total_credit == 0:
            return 0.0
        return total_score / total_credit

    def __str__(self):
        return f"{self.name}（学号：{self.student_id}）"
