import os

# File to store tasks
TASK_FILE = "tasks.txt"

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        tasks = [line.strip() for line in f.readlines()]
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

# Show tasks
def show_tasks(tasks):
    if not tasks:
        print("\n✅ No tasks in your list!\n")
        return
    print("\n📌 Your To-Do List:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print()

def main():
    tasks = load_tasks()
    
    while True:
        print("====== TO-DO LIST ======")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("👉 Enter your choice: ")

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            task = input("➕ Enter new task: ")
            tasks.append(task)
            save_tasks(tasks)
            print("✅ Task added!\n")

        elif choice == "3":
            show_tasks(tasks)
            if tasks:
                num = int(input("✔ Enter task number to mark as completed: "))
                if 1 <= num <= len(tasks):
                    tasks[num - 1] += " (Completed)"
                    save_tasks(tasks)
                    print("🎉 Task marked as completed!\n")

        elif choice == "4":
            show_tasks(tasks)
            if tasks:
                num = int(input("🗑 Enter task number to delete: "))
                if 1 <= num <= len(tasks):
                    removed = tasks.pop(num - 1)
                    save_tasks(tasks)
                    print(f"🗑 Task '{removed}' deleted!\n")

        elif choice == "5":
            print("👋 Exiting... Your tasks are saved.")
            break

        else:
            print("❌ Invalid choice! Try again.\n")

if __name__ == "__main__":
    main()
