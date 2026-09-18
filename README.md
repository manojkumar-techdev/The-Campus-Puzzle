
# 👩🏻‍💻📓✍🏻💡 My Task Manager
<br /> **Advanced Algorithm M603A** 

# 📋 Introduction

University timetabling is a problem of constraint satisfaction which involves graph colouring, bin packing and combinatorial optimisation. 
It is NP-hard in general, thus the use of a pipeline of complementary algorithms in practical systems.

The assessment brief needs to include the following: 
(1) a Greedy baseline; 
(2) a Welsh–Powell colouring of a conflict graph; 
(3) a room allocator for the DP which mixes recursive backtracking with best-effort; 
(4) a Conflict Report; 
(5) a Manual Fix Log.


# 💻 Front-End UI Design

<img width="1456" height="1818" alt="Task_Manager  UserInterface" src="https://github.com/user-attachments/assets/a699e08a-b8a8-48ee-83e6-b210a611d6cb" />


# 💻🛠 System Architecture

<img width="1733" height="395" alt="System Architecture" src="https://github.com/user-attachments/assets/8eccc0a6-3352-4fac-b610-0b440da2484b" />


# 📗 API Design

<img width="1305" height="334" alt="API_Design" src="https://github.com/user-attachments/assets/d9ce025f-a0d0-47c8-a2c8-db06ecd19638" />


# 📂 Repository Structure
<div>
    <pre>
task-manager-java/
├── pom.xml
└── src/main/
├── java/com/m604/taskmanager/
│ ├── TaskManagerApplication.java
│ ├── config/DataInitializer.java
│ ├── controller/TaskController.java
│ ├── dto/{ErrorResponse, TaskRequest}.java
│ ├── exception/{GlobalExceptionHandler,
│ │ InvalidInputException,
│ │ TaskNotFoundException}.java
│ ├── model/Task.java
│ ├── repository/TaskRepository.java
│ └── service/TaskService.java
└── resources/
├── application.properties
└── static/index.html
    </pre>
<div />

# 📌 **Features**
<br />✅ Backend Development
<br />✅ Data Interaction
<br />✅ API Development 
<br />✅ Error Handling

# ✨ **Objectives**
    🚀Create a Java backend using Spring Boot.
    🚀Implement an relational database with JPA.
    🚀Use a RESTful API to implement all the CRUD operations.
    🚀Make a GUI that runs in a browser.
    🚀Use holistic error-handling.
    🚀Make use of OOP concepts throughout.


# 🛠️ Technology Stack & Tools
---
| **Technology** | **Version** |**Purpose** |
| --- | --- | --- |
| **Java** | 17 (LTS) | Programming language |
| **Spring Boot** | 3.2.5 | Backend framework |
| **Spring Data** JPA | 3.2.5 | Database abstraction feature |
| **Hibernate** | 6.4.4 | ORM implementation |
| **H2 / SQLite** | 2.2.224 / 3.45.1 | Databases |
| **Maven** | 3.9.16 | Build tool |
| **Tomcat** | 10.1.20 | Embedded server |
---

# 🚀 How to Run
    Run:
    
<br />01.--bash
<br />02.--cd C:\Users\DELL\Desktop\task-manager-java
<br />03.--mvn spring-boot:run
<br />04.--After running above 2 commands then the server has been started on the http://localhost:5000 link which is the localhost open it in any browser which you want to run the application with the GUI.
    
# 📈 Future Improvements
    ➜ Docker containerization and Spring Security
    ➜ Pagination
    ➜ Unit tests with the JUnit
    ➜ Swagger documentation 
    ➜ cloud deployment 
    ➜ Mobile App Development

# 👨‍💻 Author

**Er. Manoj Kumar**

Aspiring Software Developer | AI & ML Enthusiast

