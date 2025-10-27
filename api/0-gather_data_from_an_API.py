#!/usr/bin/python3
"""
Python script that uses a REST API to get information about an employee's
TODO list progress for a given employee ID.
"""

import requests
import sys


# Constant for the API base URL
BASE_URL = "https://jsonplaceholder.typicode.com"


def get_employee_todo_progress(employee_id):
    """
    Fetch and display the TODO list progress for the specified employee ID.
    """
    # Fetch employee information
    user_url = "{}/users/{}".format(BASE_URL, employee_id)
    user_response = requests.get(user_url)

    if user_response.status_code != 200:
        print("Error: Unable to fetch user information.")
        return

    user_data = user_response.json()
    if not user_data:
        print("Employee not found.")
        return

    employee_name = user_data.get("name")

    # Fetch employee's TODO list
    todos_url = "{}/todos".format(BASE_URL)
    todos_response = requests.get(todos_url, params={"userId": employee_id})

    if todos_response.status_code != 200:
        print("Error: Unable to fetch TODO list.")
        return

    todos = todos_response.json()

    total_tasks = len(todos)
    completed_tasks = [task for task in todos if task.get("completed")]

    # Display progress in the required format
    print("Employee {} is done with tasks({}/{}):"
          .format(employee_name, len(completed_tasks), total_tasks))

    for task in completed_tasks:
        print("\t {}".format(task.get("title")))


if __name__ == "__main__":
    """
    Main entry point of the script.
    Validates arguments and calls the main function.
    """
    if len(sys.argv) != 2:
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)

    get_employee_todo_progress(employee_id)
