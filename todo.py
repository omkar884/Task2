# -*- coding: utf-8 -*-
# todo.py
import os
import json
import getpass

USERS_FILE = "users.txt"

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                username, password = line.strip().split(":")
                users[username] = password
    return users

def register():
    users = load_users()
    username = raw_input("Choose a username: ")
    if username in users:
        print("Username already exists.")
        return None
    password = getpass.getpass("Choose a password: ")
    with open(USERS_FILE, "a") as f:
        f.write("%s:%s\n" % (username, password))
    print("Registration successful.")
    return username

def login():
    users = load_users()
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    if users.get(username) == password:
        print("Login successful.")
        return username
    else:
        print("Invalid credentials.")
        return None

def get_task_file(username):
    return "tasks_%s.json" % username

def load_tasks(username):
    task_file = get_task_file(username)
    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            return json.load(f)
    return []

def save_tasks(username, tasks):
    task_file = get_task_file(username)
    with open(task_file, "w") as f:
        json.dump(tasks, f)

def add_task(username, tasks):
    task_text = raw_input("Enter the task: ")
    task = {
        "task": task_text,
        "completed": False
    }
    tasks.append(task)
    save_tasks(username, tasks)
    print("Task added.")

def view_tasks(tasks, show_completed=False):
    has_tasks = False
    print("\nYour Tasks:")
    for i, task in enumerate(tasks):
        if show_completed and task["completed"]:
            print("%d. %s" % (i + 1, task["task"]))
            has_tasks = True
        elif not show_completed and not task["completed"]:
            print("%d. [ ] %s" % (i + 1, task["task"]))
            has_tasks = True
    if not has_tasks:
        print("No tasks to show.")

def remove_task(username, tasks):
    view_tasks(tasks)
    try:
        index = int(raw_input("Enter task number to remove: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(username, tasks)
            print("Removed task: %s" % removed["task"])
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def mark_complete(username, tasks):
    view_tasks(tasks)
    try:
        index = int(raw_input("Enter task number to mark as complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            save_tasks(username, tasks)
            print("Marked as complete: %s" % tasks[index]["task"])
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def export_tasks(username, tasks):
    filename = "exported_tasks_%s.txt" % username
    with open(filename, "w") as f:
        for i, task in enumerate(tasks):
            status = "[✓]" if task["completed"] else "[ ]"
            f.write("%d. %s %s\n" % (i + 1, status, task["task"]))
    print("Tasks exported to %s" % filename)

def main_menu(username):
    tasks = load_tasks(username)

    while True:
        print("\n--- TO-DO LIST MENU ---")
        print("1. View Pending Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Task as Complete")
        print("5. View Completed Tasks")
        print("6. Export Tasks")
        print("7. Logout")

        choice = raw_input("Choose an option (1-7): ")

        if choice == "1":
            view_tasks(tasks, show_completed=False)
        elif choice == "2":
            add_task(username, tasks)
        elif choice == "3":
            remove_task(username, tasks)
        elif choice == "4":
            mark_complete(username, tasks)
        elif choice == "5":
            view_tasks(tasks, show_completed=True)
        elif choice == "6":
            export_tasks(username, tasks)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def main():
    print("--- TO-DO LIST LOGIN ---")
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

        choice = raw_input("Choose an option (1-3): ")

        if choice == "1":
            user = login()
            if user:
                main_menu(user)
        elif choice == "2":
            user = register()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
