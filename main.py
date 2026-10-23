from pathlib import Path
from models.student import Student
from services.student_manager import StudentManager

def display_student(students:list[Student]) -> None:
    if not students:
        print("No student found")
        return 

    for student in students:
        print(
            f"\n ID: {student.student_id}"
            f"\n name: {student.name}"
            f"\n email: {student.email}"
            f"\nMarks: {student.marks:.2f}"
        )

def read_student_details()->tuple[str,str,float]:
    name=input("Enter student name: ").strip()
    email=input("Enter email: ").strip()
    marks=float(input("Enter marks (0-100) : "))

    return name,email,marks

def main() -> None:
    data_file=Path(__file__).resolve().parent /"data"/"students.json"
    manager=StudentManager(data_file)

    while True:
        print("\n Student Management System")
        print("1.Add student")
        print("2.view student")
        print("3.search student")
        print("4.Update student")
        print("5.delete student")
        print("6.Exit")

        number=input("Enter your choice:").strip()

        try:
            if number=="1":
                name,email,marks=read_student_details()
                student=manager.add_student(name,email,marks)
                print(f"Student added successfully . ID: {student.student_id}")
            
            elif number=="2":             
                display_student(manager.get_students())

            elif number=="3":
                keyword=input("Enter name or email to search: ")
                display_student(manager.search_student(keyword))
            
            elif number=="4":
                student_id = int(input("Enter studetn ID to update: "))
                name,email,marks=read_student_details()

                student=manager.update_student(student_id,name,email,marks) 

                print(f"student {student.student_id} update successfully")

            elif number=="5":
                student_id = int(input("Enter student id want to delete :"))
                confirm=input("Are you sure you want to delete this task? (y/n): ").casefold()

                if confirm not in ("y", "yes"):
                    print("Deletion cancelled.")
                

                manager.delete_student(student_id)
                print("Student deleted successfully")
            elif number=="6":
                print("Exiting student management system")
                break
            else:
                print("Invalid choice. please enter 1 to 6")
        except ValueError as exc:
            print(f"Error: {exc}")
        except OSError as exc:
            print(f"file operation file: {exc}")

if __name__=="__main__":
    main()                