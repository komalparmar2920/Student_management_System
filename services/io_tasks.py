import asyncio
import time
from dataclasses import dataclass
from models.student import Student
Task_delays={
   "add_student":0.5,
   "view_student":0.2,
}

@dataclass
class RunResult:
    mode:str
    elapsed:float
    tasks_done: int

def _sync_add(store:list[Student],student:Student) -> str:
    time.sleep(Task_delays["add_student"])
    store.append(student)
    return f"added {student.name}"

def _sync_view(store:list[Student]) -> list[str]:
    time.sleep(Task_delays["view_students"])
    return [s.name for s in store] 

def run_sync(students:list[Student]) -> RunResult:
    store:list[Student]=[]
    start=time.perf_counter()
    results=[]
    for s in students:
        results.append(_sync_add(store,s))
        result.append(_sync_view(store))

async def _async_data(store:list[Student],student:Student) -> str:
    await asyncio.sleep(Task_delays["add_student"])
    store.append(student)
    return f"added {student.name}"

async def _async_view(store:list[Student]) -> list[str]:
    await asyncio.sleep(Task_delys["view_students"])
    return [s.name for s in store]    

async def run_async(students:list[Student]) ->RunResult:
    store: list[Student] = []
    start = time.perf_counter()
    results=await asyncio.gather(
        *(coro for s in students for coro in (_sync_add(store,s),_sync_view(store)))
    )
    return RunResult("async (gather)",time.perf_counter() - start,len(results))

async def _blocking_add(store:list[Student], student:Student) -> str:
    time.sleep(Task_delays["add_student"])
    store.append(student)
    return f"added {student.name}"

async def _blocking_view(store:list[Student]) -> list[str]:
    time.sleep(Task_delays["view students"])    
    return [s.name for s in store]

async def run_async_blocking(students: list[Student]) -> RunResult:
    store: list[Student] = []
    start = time.perf_counter()
    results=await asyncio.gather(
        *(coro for s in students for coro in (_blocking_add(store,s), _blocking_view(store)))
    )
    return RunResult("async (blocking call)",time.perf_counter() - start, len(results))

async def compare(students:list[Student]) -> list[RunResult]:
    sync_resut,async_result,blocking_result = await asyncio.gather(
        asyncio.to_thread(run_sync,students),
        run_async(students),
        asyncio.to_thread(asyncio.run,run_async_blocking(students)),
    )        
    return [sync_result,async_result,blocking_result]
async def add_and_view(add_func,view_func,name:str,email:str,marks:float):
    lock = asyncio.Lock()
    async def add():
        async with lock:
            return await asyncio.to_thread(add_func,name,email,marks)
    async def view():
        async with lock:
            return await asyncio.to_thread(view_func)
    return await asyncio.gather(add(),view())    

def print_report(results:list[RunResult]) -> None:
    baseline = result[0].elapsed
    print(f"\n {'mode'<24}{'Tasks':>6}{'Time (s)':>11}{'speed-up':>10}")
    print("-"*51)
    for r in results:
        print(f"{r.mode:<24}{r.tasks_done:>6}{r.elapsed:>11.2f}{baseline/r.elapsed:>9.1f}x")

if __name__=="__main__":
   name=input("enter Student name: ").strip()
   email=input("enter email: ").strip()
   marks=float(input("Enter marks (0-100): "))

   students = [Student(student_id=1,name=name,email=email,marks=marks)]
   print_report(asyncio.run(compare(students)))