from asyncio import Task
import asyncio
from typing import Callable

class AsyncLimiter:
    tasks: list[Task]
    remaining_elements: list
    done_tasks_count: int
    print_progress_str: str
    max_task_count: int
    function_for_task: Callable # str bc idc how to put a function there lmao

    def __init__(self,
                 function_to_task, #Function to call
                 print_progress_str: str = "Downloaded/Remaining tasks: {downloaded!s}/{remaining!s}, Running tasks: {running_tasks!s}      ",
                 max_task_count: int = 20
                 ) -> None:
        self.done_tasks_count = 0
        self.remaining_elements = []
        self.tasks = []
        self.print_progress_str = print_progress_str
        self.function_for_task = function_to_task
        self.max_task_count = max_task_count

    # To be called & returned when an error occurs
    # eg:
    # try:
    #     ....
    # except:
    #     return fail(elem)
    #
    # Will automatically add back to the remaining list & return false
    def fail(self, element):
        print("Failed apparently...")
        self.remaining_elements.append(element)
        return False

    async def grab_all(self):
        while True:    
            for element in self.remaining_elements:
                if (len(self.tasks) > self.max_task_count):
                    break
                self.tasks.append(asyncio.create_task(self.function_for_task(element)))
                self.remaining_elements.remove(element)

            for task in self.tasks:
                if task.done():
                    self.tasks.remove(task)
                    self.done_tasks_count += 1

            print(self.print_progress_str.format(
                downloaded=self.done_tasks_count,
                remaining=len(self.remaining_elements),
                running_tasks=len(self.tasks)
            ), end="\r")

            if len(self.tasks) == 0:
                break

            await asyncio.sleep(.2)
        
        print("\n== Done with batch ==")