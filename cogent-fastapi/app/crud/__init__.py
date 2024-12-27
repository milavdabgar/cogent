from app.crud.crud_user import (
    get_user,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
    authenticate,
    count_total_users,
    count_total_colleges,
    count_active_students,
    count_active_faculty,
    count_total_courses,
    count_total_labs
)

from app.crud.crud_college import (
    get_college,
    get_colleges,
    create_college,
    update_college,
    delete_college,
    get_department,
    get_departments,
    create_department,
    update_department,
    delete_department
)

from app.crud.crud_course import (
    get_course,
    get_courses,
    create_course,
    update_course,
    delete_course,
    get_faculty_assignment,
    get_faculty_assignments,
    create_faculty_assignment,
    update_faculty_assignment,
    delete_faculty_assignment
)

college = crud_college
course = crud_course
user = crud_user
