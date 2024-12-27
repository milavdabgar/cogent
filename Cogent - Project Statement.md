### Cogent - Project Statement

#### **Project Overview**

This project aims to develop a web portal using **FastAPI** for the backend and **Vue.js** for the frontend. The portal will cater to the administrative and academic needs of the **Department of Technical Education (DTE), Gujarat Technological University (GTU),** and its affiliated colleges, covering a wide range of diploma, bachelor’s, and master’s degree programs.

The platform will centralize operations for all stakeholders, including **students, faculty, department heads, college administrators, GTU, and DTE.** It will streamline processes like student enrollment, curriculum management, academic progress tracking, timetable scheduling, resource management, and feedback analysis.

#### **Key Entities and Relationships**

1. **Institutions and Departments:**
   - **Government Polytechnics (GP):** Offer diploma programs in branches like Electrical Engineering (ECE), Information Technology (ICT), etc.
   - **Government Engineering Colleges (GECs):** Offer bachelor’s and master’s programs in branches like Computer Science (CSE), Mechanical Engineering, etc.
   - Each college has **departments** offering programs at multiple levels.
2. **Branches and Programs:**
   - GTU defines engineering branches (e.g., ECE, CSE) and their associated programs (e.g., Diploma in ECE, Bachelor’s in CSE).
   - A program comprises multiple subjects, each identified by a **unique subject code.**
3. **Students:**
   - Students are admitted through ACPDC (for diplomas) or ACPC (for bachelor’s/master’s programs).
   - Enrolled students are associated with specific colleges and programs.
   - Students may be detained due to backlogs and later rejoin another batch.
4. **Faculty:**
   - Faculties are assigned to specific branches and colleges by the DTE.
   - They may transfer between colleges and take on administrative or academic roles (e.g., lab in-charge, exam coordinator).
5. **Administrative Hierarchy:**
   - **DTE:** Manages colleges, faculty assignments, and policy enforcement.
   - **GTU:** Manages academic frameworks, branches, programs, and subjects.
   - **Principals:** Oversee college-level operations and form committees.
   - **HODs:** Oversee department-specific tasks and allocate responsibilities.

------

#### **Key Features and Functionalities**

### **1. Role-Based Access Control (RBAC):**

- Allow users to perform tasks based on assigned roles.
- Enable multi-role access (e.g., HOD + faculty or Principal + departmental admin).
- Provide role-specific dashboards with clear task segregation.

------

### **2. Student Management:**

- **Admission Data:**
  - Import ACPDC/ACPC data for admitted students.
  - Record students leaving before enrollment.
- **Enrollment:**
  - Facilitate enrollment forms for GTU and manage enrolled student lists.
  - Handle detention and re-enrollment for students with backlogs.
- **Student Profiles:**
  - Maintain comprehensive records, including attendance, grades, and backlog status.
  - Enable tracking across multiple terms and programs.

------

### **3. Academic Management:**

- **Curriculum and Subject Management:**
  - Define programs with unique subject codes, credits, lecture theory hours, and practical components.
  - Allow GTU to update curriculum data.
- **Timetable Management:**
  - Auto-generate timetables for departments and faculties.
  - Manage conflicts and rescheduling.
- **Assignment and Material Sharing:**
  - Faculty upload assignments, lecture notes, and lab manuals.
  - Students access materials via their portal.

------

### **4. Faculty Management:**

- **Faculty Assignments:**
  - Assign faculties to specific branches, programs, and colleges.
  - Manage transfers and role changes (e.g., exam coordinator, lab in-charge).
- **Committee Management:**
  - Principals form college-level committees (e.g., Hostel, TPO, AICTE).
  - HODs assign department-level roles and track performance.

------

### **5. Feedback Management:**

- **Student Feedback:**
  - Collect department-specific feedback.
  - Share aggregated feedback with institute and DTE administrators.
- **Faculty Feedback:**
  - Collect and analyze feedback at the department or college level.

------

### **6. Resource and Inventory Management:**

- Track lab equipment, library resources, and department inventories.
- Log equipment usage, maintenance requests, and availability.

------

### **7. Examination Management:**

- Manage internal and external exam schedules.
- Track student grades and synchronize results with GTU.
- Allow faculties to submit and review grades before finalization.

------

### **8. Event and Activity Management:**

- Cultural and Academic Events:
  - Plan and track student/faculty participation.
- Training and Placement (TPO):
  - Manage student placements and training records.

------

### **9. Reports and Analytics:**

- Generate insights on student performance, feedback, and enrollment trends.
- Provide reports for GTU, DTE, principals, and HODs.

------

### **10. Technology Stack Recommendations:**

- **Backend:** FastAPI for API development.
- **Frontend:** Vue.js for user-friendly, dynamic interfaces.
- **Database:** PostgreSQL for relational data.
- **Authentication:** OAuth2 with JWT.
- **Deployment:** Docker and Kubernetes for scalability, with cloud-based or on-premise hosting options.

------

#### **Additional Considerations:**

- Ensure **data integrity and security** for sensitive academic and administrative data.
- Integrate APIs for GTU systems for real-time updates.
- Implement **multi-language support** for Gujarati and English.
- Future-proof with modules for AI-based analytics and chatbot assistance.

------

### **Roles and Their Dedicated Portal Features, Functions, and Tasks**

Below is a detailed breakdown of all roles and the features, functions, and tasks they can perform from their respective portals.

------

## **1. Department of Technical Education (DTE) Administrator**

### **Features and Tasks**

- **College Management:**
  - Add, edit, deactivate, or remove colleges.
  - Assign and track principal appointments.
  - View reports on college performance and compliance.
- **Faculty Management:**
  - Add, edit, transfer, or deactivate faculty members.
  - Assign faculty roles to specific colleges and branches.
- **Program and Curriculum Oversight:**
  - Approve or update programs proposed by GTU.
  - Oversee branch and program creation at colleges.
- **Compliance Monitoring:**
  - Review academic compliance reports submitted by colleges.
  - Approve or flag deviations in reports.
- **Reporting and Analytics:**
  - Generate insights on faculty utilization, program enrollments, and student success rates across colleges.

------

## **2. GTU Administrator**

### **Features and Tasks**

- **Branch and Program Management:**
  - Add, update, or deactivate branches and programs.
  - Define program-specific subjects with credits, lecture hours, and practical hours.
- **Subject Management:**
  - Create and manage subjects with unique codes.
  - Assign subjects to programs and ensure curriculum compliance.
- **Enrollment Oversight:**
  - Manage enrolled student lists for all colleges.
  - Oversee detention and backlog management.
- **Examination Management:**
  - Oversee external exam schedules for all colleges.
  - Monitor grade submissions and ensure final result processing.
- **Reporting and Data Analytics:**
  - Generate program-wise performance reports.
  - Share data insights with DTE and affiliated colleges.

------

## **3. Principal**

### **Features and Tasks**

- **Committee Management:**
  - Form institute-level committees (e.g., Hostel, TPO, AICTE, CWAN).
  - Assign faculty members to committees and monitor their progress.
- **Faculty Oversight:**
  - Approve department-specific faculty roles assigned by HODs.
  - View faculty workloads across the college.
- **Student Management:**
  - Monitor overall student enrollment, dropout, and re-enrollment data.
  - Review reports on student feedback and academic progress.
- **College Infrastructure Management:**
  - Oversee inventory requests and allocations at the department level.
  - Approve maintenance logs for labs and other resources.
- **Event Management:**
  - Approve or schedule college-wide cultural and academic events.
- **Analytics and Reporting:**
  - Access detailed analytics on college performance and feedback.
  - Submit compliance reports to GTU and DTE.

------

## **4. Head of Department (HOD)**

### **Features and Tasks**

- **Faculty Management:**
  - Assign department-specific responsibilities (e.g., exam coordinator, lab in-charge).
  - Monitor faculty workload and feedback reports.
- **Student Management:**
  - Manage student enrollment and attendance.
  - Handle detention and re-enrollment cases within the department.
- **Timetable Management:**
  - Create and approve department-level timetables.
  - Resolve conflicts in resource or faculty availability.
- **Feedback Management:**
  - Collect and analyze department-level feedback from students.
  - Share department insights with the principal.
- **Inventory and Resource Management:**
  - Track department lab equipment and submit maintenance requests.
  - Approve inventory usage logs.
- **Event and Activity Coordination:**
  - Plan department-level events, workshops, and guest lectures.

------

## **5. Faculty**

### **Features and Tasks**

- **Academic Responsibilities:**
  - Upload assignments, lecture notes, and lab manuals.
  - Evaluate student submissions and provide grades or feedback.
- **Student Progress Monitoring:**
  - Track student attendance and performance for assigned subjects.
  - Submit internal assessment grades.
- **Timetable and Resource Management:**
  - View and manage teaching schedules.
  - Book resources (labs, projectors, etc.) for classes.
- **Role-Specific Duties:**
  - Fulfill committee-specific responsibilities (e.g., TPO, exam invigilator).
  - Log activity reports for assigned roles.

------

## **6. Students**

### **Features and Tasks**

- **Academic Dashboard:**
  - View personal profiles, including attendance, grades, and backlogs.
  - Download assignments, lecture notes, and other study materials.
- **Feedback Submission:**
  - Provide feedback on faculty and courses.
- **Resource Access:**
  - Access lab schedules and submit resource usage requests.
- **Exam and Result Management:**
  - View exam schedules and results.
  - Track re-enrollment status after detention.
- **Event Participation:**
  - Register for department or college events.
  - Submit participation certificates for extracurricular activities.

------

## **7. Admission Committee (ACPDC/ACPC)**

### **Features and Tasks**

- Admission Data Management:
  - Upload and manage lists of admitted students for diploma and degree programs.
  - Track admission trends and submit data to DTE and GTU.

------

## **8. Examination Coordinator (Institute/Department Level)**

### **Features and Tasks**

- **Exam Schedule Management:**
  - Plan and publish internal exam schedules.
  - Coordinate with GTU for external exam logistics.
- **Grade Submission:**
  - Collect and verify internal assessment grades from faculty.
  - Submit grades to GTU for final processing.

------

## **9. Training and Placement Officer (TPO)**

### **Features and Tasks**

- **Placement Management:**
  - Maintain company and student placement records.
  - Organize placement drives and workshops.
- **Student Training Records:**
  - Track training sessions attended by students.
  - Maintain reports on skill development initiatives.

------

## **10. Lab In-Charge**

### **Features and Tasks**

- Lab Management:
  - Maintain lab equipment logs and utilization data.
  - Submit maintenance and inventory requests.

------

## **11. Inventory Manager**

### **Features and Tasks**

- Inventory Tracking:
  - Oversee department and institute inventory.
  - Approve or decline inventory usage requests.

------

By structuring the portal with these roles and associated tasks, the system can ensure a smooth workflow for academic, administrative, and operational processes at every level.

/api/v1/gtu-admin/
  departments/
    GET    /                   # List all departments
    POST   /                   # Create department
    GET    /{id}              # Get department details
    PUT    /{id}              # Update department
    DELETE /{id}              # Delete department

  degree-levels/
    GET    /                   # List all degree levels
    POST   /                   # Create degree level
    GET    /{id}              # Get degree level details
    PUT    /{id}              # Update degree level
    DELETE /{id}              # Delete degree level

  degree-programs/
    GET    /                   # List all degree programs
    POST   /                   # Create degree program
    GET    /{id}              # Get program details
    PUT    /{id}              # Update program
    DELETE /{id}              # Delete program
    GET    /{id}/subjects     # Get subjects in program

  subjects/
    GET    /                   # List all subjects
    POST   /                   # Create subject
    GET    /{id}              # Get subject details
    PUT    /{id}              # Update subject
    DELETE /{id}              # Delete subject

  program-subjects/
    GET    /program/{program_id}  # Get subjects mapped to program
    POST   /                      # Map subject to program
    PUT    /{id}                 # Update subject mapping
    DELETE /{id}                 # Remove subject from program