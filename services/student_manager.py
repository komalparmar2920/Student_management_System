from models.student import Student
from storage.json_storage import JSONStorage

class StudentManager:
    def __init__(self,storage: JSONStorage):
        self.storage = storage
        self.students: list[Student] =[]
        self._load_students()
    
    def _load_students(self) -> None:
        records=self.storage.load()
        self.students=[Student.from_dict(record) for record in records]

        ids=[student.student_id for student in self.students]
        email=[student.email.casefold() for student in self.students]

        if len(ids) != len(set(ids)):
            raise ValueError("Dublicate student student id found in storage")
        if len(email) != len(set(email)):
            raise ValueError("Dublicate student email found in storage")    

    def _save_student(self) -> None:
        record = [student.to_dict() for student in self.students]
        self.storage.save(record)

    @staticmethod
    def _validate_details(name:str,email: str,marks:float) -> None:
        if not name.strip():
            raise ValueError("Student name cannot be empty")

        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Enter a valid email address")

        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 to 100")

    def add_student(self,name:str,email:str,marks:float) -> Student:
        self._validate_details(name,email,marks)
        email=email.strip().casefold()
        if any(student.email.casefold()==email for student in self.students):
            raise ValueError("This email is already registered")
        student_id = max(
            (students.student_id for students in self.students),default=0,
        )+1

        student=Student(
            student_id=student_id,
            name=name.strip(),
            email=email,
            marks=marks,
        )

        self.students.append(student)
        self._save_student()
        return student

    def get_students(self) -> list[Student]:
        return self.students.copy()

    def list_all(self) -> list[Student]:
        return self.get_students()

    def get(self,student_id:int) -> Student | None:
        return next((student for students in self.students if student.student_id==student_id), None)        

    def search_student(self,keyword:str) -> list[Student]:
        keyword=keyword.strip().casefold()    
        if not keyword:
            raise ValueError("Search keyworld is not in list")        

        return[
            student
            for student in self.students
            if keyword in student.name.casefold()
            if keyword in student.email.casefold()
        ]    

    def update_student(
        self,student_id:int,name:str,email:str,marks:float,
    ) -> Student:
        self._validate_details(name,email,marks)
        email=email.strip().casefold()

        for student in self.students:
            if(
                student.student_id != student_id and student.email.casefold() == email
            ):
                raise ValueError("This email belongs to another student")

        for student in self.students:
            if student.student_id == student_id:
                student.name = name.strip()
                student.email = email
                student.marks=marks   
                self._save_student()
                return student
        raise ValueError(f"Student ID {student_id} was not found")
    def delete_student(self,student_id:int) -> None:
        for index,student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[index]
                self._save_student()
                return                     
        raise ValueError(f"Student ID {student_id} was not found.")       