import asyncio
from pathlib import Path
from models.student import Student
from services import io_tasks
from services.student_manager import StudentManager
from storage.json_storage import JSONStorage

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

def run_io_comparison(manager: StudentManager) -> None:
    students = manager.list_all()
    if not students:
        print("Add at least one student first.")
        return
    print(f"Running {len(students) * len(io_tasks.Task_delays)} simulated I/O tasks "
          f"for {len(students)} student(s) in 3 modes...")
    io_tasks.print_report(asyncio.run(io_tasks.compare(students)))

def read_student_details()->tuple[str,str,float]:
    name=input("Enter student name: ").strip()
    email=input("Enter email: ").strip()
    marks=float(input("Enter marks (0-100) : "))

    return name,email,marks

def run_add_and_view(manager:StdeuntManager) -> None:
    name,email,marks=read_student_details()
    student,students = asyncio.run(
        io_tasks.add_and_view(manager.add_student,manager.list_all,name,email,marks)
    )    
    print(f"Student added successfully. ID : {student.student_id}")
    display_student(students)

def main() -> None:
    data_file=Path(__file__).resolve().parent /"data"/"students.json"
    storage = JSONStorage(data_file)

    manager=StudentManager(storage)
    print([m for m in dir(manager) if not m.startswith("_")])

    while True:
        print("\n Student Management System")
        print("1.Add student")
        print("2.view student")
        print("3.search student")
        print("4.Update student")
        print("5.delete student")
        print("6.Add & view student togher (async)")
        print("7.Exit")

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
                run_add_and_view(manager)

            elif number=="7":
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