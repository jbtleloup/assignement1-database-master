def display_menu():
    print(
        "1. Enter the instructor ID and I will provide you with the name of the instructor, affiliated department and "
        "the location of that department. \n"
        "2. Enter the department name and I will provide you with the location, budget and names of all instructors "
        "that work for the department. \n"
        "3. Insert a record about a new instructor.\n"
        "4. Delete a record about an instructor\n"
        "5. Exit\n")


def get_instructor_info_from_id(instructors, instructor_id):
    if instructor_id in instructors:
        return instructors[instructor_id]
    else:
        return None


def get_dept_info_from_dept_name(departments, dept_name):
    if dept_name in departments:
        return departments[dept_name]
    else:
        return None


def get_instructors_from_dept_name(instructors, dept_name):
    return [instructor_id for instructor_id, instructor_info in instructors.items() if instructor_info[1] == dept_name]


def insert_instructor(instructors, departments):
    print("Enter the instructor id: ")
    instructor_id = input()
    if instructor_id in instructors:
        print("Instructor id already exists in the file")
        return False
    print("Enter the instructor name: ")
    instructor_name = input()
    print("Enter the affiliated department name: ")
    department_name = input()
    if department_name not in departments:
        print("The department does not exist and hence the instructor record cannot be added to the database")
        return False
    # insert in hashtable
    instructors[instructor_id] = [instructor_name, department_name]
    # Update actual file
    update_file('instructor.txt', instructors)


def delete_instructor(instructors):
    print("Enter the instructor id: ")
    instructor_id = input()
    if instructor_id not in instructors:
        print("The ID does not appear in the file.")
        return False
    # Delete from hashtable
    del instructors[instructor_id]
    # Update the actual file
    update_file("instructor.txt", instructors)


def update_file(filename, hashtable):
    _list = map(list, hashtable.items())

    # Clear file content
    open(filename, 'w').close()

    # Append new file content
    with open(filename, 'a') as f:
        for l in _list:
            l_unpacked = [l[0], *l[1]]
            print(','.join(map(str, l_unpacked)), file=f)


def create_hash_table_from_file(filename):
    hashtable = {}
    with open(filename) as f:
        for l in f:
            hashtable[l.replace('\n', '').split(',')[0]] = l.replace('\n', '').split(',')[1:]

    return hashtable


def main():
    # Make two hash tables for easier access
    instructors = create_hash_table_from_file('instructor.txt')
    departments = create_hash_table_from_file('department.txt')
    display_menu()
    user_choice = menu_input_from_user()
    while user_choice != 5:
        execute_menu_action(user_choice, instructors, departments)
        display_menu()
        user_choice = menu_input_from_user()


def menu_input_from_user():
    try:
        user_choice = int(input("-> "))
    except ValueError:
        print("Input needs to be a number")
        user_choice = menu_input_from_user()
    return user_choice


def execute_menu_action(user_choice, instructors, departments):
    if user_choice == 1:
        instructor_id = input("Enter the instructor ID: ")
        instructor_info = get_instructor_info_from_id(instructors, instructor_id)
        if not instructor_info:
            print("The ID does not appear in the file. \n")
            return
        instructor_dept_location = get_dept_info_from_dept_name(departments, instructor_info[1])[0]
        print(*instructor_info, instructor_dept_location)
    elif user_choice == 2:
        dept_name = input("Enter the department name: ")
        dept_info = get_dept_info_from_dept_name(departments, dept_name)
        if not dept_info:
            print("The department name does not appear in the file.")
            return
        instructors_id = get_instructors_from_dept_name(instructors, dept_name)
        instructors_name = [get_instructor_info_from_id(instructors, instructor_id)[0] for instructor_id in
                            instructors_id]
        print(dept_name, *dept_info, *instructors_name)
    elif user_choice == 3:
        insert_instructor(instructors, departments)
    elif user_choice == 4:
        delete_instructor(instructors)
    else:
        return False


if __name__ == '__main__':
    main()
