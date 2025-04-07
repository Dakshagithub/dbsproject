-- Drop existing database if exists
DROP DATABASE IF EXISTS university_db;
CREATE DATABASE university_db;
USE university_db;

-- Create Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Student', 'Faculty') NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Create Departments table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(50) NOT NULL,
    department_code VARCHAR(10) UNIQUE NOT NULL,
    budget DECIMAL(10,2) NOT NULL,
    established_year INT NOT NULL,
    description TEXT
);

-- Create Courses table
CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(50) NOT NULL,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    department_id INT,
    credits INT NOT NULL,
    description TEXT,
    prerequisites TEXT,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    year INT NOT NULL,
    CONSTRAINT fk_courses_department FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Create Students table
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    department_id INT,
    enrollment_date DATE NOT NULL,
    graduation_date DATE,
    gpa DECIMAL(3,2) DEFAULT 0.00,
    attendance_percentage DECIMAL(5,2) DEFAULT 100.00,
    status ENUM('Active', 'Inactive', 'Graduated', 'On Leave') DEFAULT 'Active',
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT fk_students_department FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Create Faculty table
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    department_id INT,
    title ENUM('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer') NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    office_location VARCHAR(50),
    CONSTRAINT fk_faculty_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT fk_faculty_department FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Create Enrollments table
CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE NOT NULL,
    grade CHAR(2),
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    year INT NOT NULL,
    CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id) REFERENCES Students(student_id),
    CONSTRAINT fk_enrollments_course FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Insert Departments
INSERT INTO Departments (department_name, department_code, budget, established_year, description) VALUES
('Computer Science', 'CS', 1000000.00, 1990, 'Department of Computer Science'),
('Mathematics', 'MATH', 800000.00, 1985, 'Department of Mathematics'),
('Physics', 'PHY', 900000.00, 1988, 'Department of Physics'),
('Chemistry', 'CHEM', 850000.00, 1987, 'Department of Chemistry'),
('Biology', 'BIO', 950000.00, 1989, 'Department of Biology'),
('Engineering', 'ENG', 1200000.00, 1992, 'Department of Engineering'),
('Business', 'BUS', 1100000.00, 1991, 'Department of Business'),
('Arts', 'ART', 700000.00, 1986, 'Department of Arts'),
('History', 'HIST', 750000.00, 1984, 'Department of History'),
('Languages', 'LANG', 800000.00, 1983, 'Department of Languages');

-- Insert Admin User
INSERT INTO Users (username, email, password, role, first_name, last_name, phone, address) VALUES
('admin', 'admin@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Admin', 'John', 'Smith', '1234567890', '123 Admin St');

-- Insert Faculty Users
INSERT INTO Users (username, email, password, role, first_name, last_name, phone, address) VALUES
('jdoe', 'jdoe@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Jane', 'Doe', '1234567891', 'Faculty Housing 1'),
('rjohnson', 'rjohnson@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Robert', 'Johnson', '1234567892', 'Faculty Housing 2'),
('msmith', 'msmith@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Mary', 'Smith', '1234567893', 'Faculty Housing 3'),
('jwilson', 'jwilson@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'James', 'Wilson', '1234567894', 'Faculty Housing 4'),
('sbrown', 'sbrown@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Sarah', 'Brown', '1234567895', 'Faculty Housing 5'),
('dlee', 'dlee@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'David', 'Lee', '1234567896', 'Faculty Housing 6'),
('pwhite', 'pwhite@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Patricia', 'White', '1234567897', 'Faculty Housing 7'),
('mblack', 'mblack@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Michael', 'Black', '1234567898', 'Faculty Housing 8'),
('agreen', 'agreen@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Amy', 'Green', '1234567899', 'Faculty Housing 9'),
('tred', 'tred@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Faculty', 'Thomas', 'Red', '1234567900', 'Faculty Housing 10');

-- Insert Faculty Records
INSERT INTO Faculty (user_id, department_id, title, specialization, hire_date, salary, office_location) VALUES
(2, 1, 'Professor', 'Artificial Intelligence', '2020-01-01', 90000.00, 'CS Building 101'),
(3, 2, 'Associate Professor', 'Applied Mathematics', '2019-01-01', 80000.00, 'MATH Building 101'),
(4, 3, 'Professor', 'Quantum Physics', '2018-01-01', 95000.00, 'PHY Building 101'),
(5, 4, 'Assistant Professor', 'Organic Chemistry', '2021-01-01', 75000.00, 'CHEM Building 101'),
(6, 5, 'Professor', 'Molecular Biology', '2017-01-01', 90000.00, 'BIO Building 101'),
(7, 6, 'Associate Professor', 'Mechanical Engineering', '2019-01-01', 85000.00, 'ENG Building 101'),
(8, 7, 'Professor', 'Business Management', '2016-01-01', 100000.00, 'BUS Building 101'),
(9, 8, 'Assistant Professor', 'Fine Arts', '2021-01-01', 70000.00, 'ART Building 101'),
(10, 9, 'Associate Professor', 'Modern History', '2018-01-01', 80000.00, 'HIST Building 101'),
(11, 10, 'Professor', 'Linguistics', '2017-01-01', 90000.00, 'LANG Building 101');

-- Insert Student Users
INSERT INTO Users (username, email, password, role, first_name, last_name, phone, address) VALUES
('asmith', 'asmith@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Alice', 'Smith', '1234567901', 'Student Dorm 101'),
('bwilson', 'bwilson@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Bob', 'Wilson', '1234567902', 'Student Dorm 102'),
('cjohnson', 'cjohnson@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Charlie', 'Johnson', '1234567903', 'Student Dorm 103'),
('dbrown', 'dbrown@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'David', 'Brown', '1234567904', 'Student Dorm 104'),
('elee', 'elee@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Emma', 'Lee', '1234567905', 'Student Dorm 105'),
('fwhite', 'fwhite@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Frank', 'White', '1234567906', 'Student Dorm 106'),
('gblack', 'gblack@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Grace', 'Black', '1234567907', 'Student Dorm 107'),
('hgreen', 'hgreen@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Henry', 'Green', '1234567908', 'Student Dorm 108'),
('ired', 'ired@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Isabella', 'Red', '1234567909', 'Student Dorm 109'),
('jblue', 'jblue@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'James', 'Blue', '1234567910', 'Student Dorm 110'),
('kyellow', 'kyellow@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Katherine', 'Yellow', '1234567911', 'Student Dorm 111'),
('lpurple', 'lpurple@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Lucas', 'Purple', '1234567912', 'Student Dorm 112'),
('morange', 'morange@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Mia', 'Orange', '1234567913', 'Student Dorm 113'),
('npink', 'npink@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Noah', 'Pink', '1234567914', 'Student Dorm 114'),
('ogray', 'ogray@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Olivia', 'Gray', '1234567915', 'Student Dorm 115'),
('pnavy', 'pnavy@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Peter', 'Navy', '1234567916', 'Student Dorm 116'),
('qmaroon', 'qmaroon@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Quinn', 'Maroon', '1234567917', 'Student Dorm 117'),
('rteal', 'rteal@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Rachel', 'Teal', '1234567918', 'Student Dorm 118'),
('slime', 'slime@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Samuel', 'Lime', '1234567919', 'Student Dorm 119'),
('tcyan', 'tcyan@university.edu', 'pbkdf2:sha256:260000$d4e5f6g7h8i9j0k1$2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7', 'Student', 'Taylor', 'Cyan', '1234567920', 'Student Dorm 120');

-- Insert Student Records
INSERT INTO Students (user_id, department_id, enrollment_date, graduation_date, gpa, attendance_percentage, status) VALUES
(12, 1, '2023-01-01', '2027-01-01', 3.8, 95.5, 'Active'),
(13, 2, '2023-01-01', '2027-01-01', 3.5, 92.0, 'Active'),
(14, 3, '2023-01-01', '2027-01-01', 3.9, 98.0, 'Active'),
(15, 4, '2023-01-01', '2027-01-01', 3.6, 94.5, 'Active'),
(16, 5, '2023-01-01', '2027-01-01', 3.7, 96.0, 'Active'),
(17, 6, '2023-01-01', '2027-01-01', 3.4, 91.5, 'Active'),
(18, 7, '2023-01-01', '2027-01-01', 3.8, 97.0, 'Active'),
(19, 8, '2023-01-01', '2027-01-01', 3.5, 93.5, 'Active'),
(20, 9, '2023-01-01', '2027-01-01', 3.6, 95.0, 'Active'),
(21, 10, '2023-01-01', '2027-01-01', 3.7, 96.5, 'Active'),
(22, 1, '2023-01-01', '2027-01-01', 3.8, 97.5, 'Active'),
(23, 2, '2023-01-01', '2027-01-01', 3.5, 94.0, 'Active'),
(24, 3, '2023-01-01', '2027-01-01', 3.9, 98.5, 'Active'),
(25, 4, '2023-01-01', '2027-01-01', 3.6, 95.5, 'Active'),
(26, 5, '2023-01-01', '2027-01-01', 3.7, 96.5, 'Active'),
(27, 6, '2023-01-01', '2027-01-01', 3.4, 92.5, 'Active'),
(28, 7, '2023-01-01', '2027-01-01', 3.8, 97.5, 'Active'),
(29, 8, '2023-01-01', '2027-01-01', 3.5, 94.5, 'Active'),
(30, 9, '2023-01-01', '2027-01-01', 3.6, 95.5, 'Active'),
(31, 10, '2023-01-01', '2027-01-01', 3.7, 96.5, 'Active');

-- Insert Courses
INSERT INTO Courses (course_name, course_code, department_id, credits, description, prerequisites, semester, year) VALUES
('Introduction to Programming', 'CS101', 1, 3, 'Basic programming concepts', NULL, 'Fall', 2024),
('Data Structures', 'CS102', 1, 3, 'Advanced data structures', 'CS101', 'Spring', 2024),
('Calculus I', 'MATH101', 2, 4, 'Introduction to calculus', NULL, 'Fall', 2024),
('Linear Algebra', 'MATH102', 2, 3, 'Matrix operations and linear transformations', 'MATH101', 'Spring', 2024),
('Physics I', 'PHY101', 3, 4, 'Classical mechanics', NULL, 'Fall', 2024),
('Physics II', 'PHY102', 3, 4, 'Electromagnetism', 'PHY101', 'Spring', 2024),
('General Chemistry', 'CHEM101', 4, 4, 'Basic chemistry concepts', NULL, 'Fall', 2024),
('Organic Chemistry', 'CHEM102', 4, 4, 'Organic compounds and reactions', 'CHEM101', 'Spring', 2024),
('Biology I', 'BIO101', 5, 4, 'Cell biology and genetics', NULL, 'Fall', 2024),
('Biology II', 'BIO102', 5, 4, 'Ecology and evolution', 'BIO101', 'Spring', 2024);

-- Insert Enrollments
INSERT INTO Enrollments (student_id, course_id, enrollment_date, grade, semester, year) VALUES
(1, 1, '2024-01-01', 'A', 'Fall', 2024),
(1, 2, '2024-01-01', 'A-', 'Spring', 2024),
(2, 3, '2024-01-01', 'B+', 'Fall', 2024),
(2, 4, '2024-01-01', 'B', 'Spring', 2024),
(3, 5, '2024-01-01', 'A', 'Fall', 2024),
(3, 6, '2024-01-01', 'A-', 'Spring', 2024),
(4, 7, '2024-01-01', 'B+', 'Fall', 2024),
(4, 8, '2024-01-01', 'B', 'Spring', 2024),
(5, 9, '2024-01-01', 'A', 'Fall', 2024),
(5, 10, '2024-01-01', 'A-', 'Spring', 2024); 