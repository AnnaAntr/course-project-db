-- Очистка схемы данных
DROP TABLE IF EXISTS Group_Class;               -- пара у группы
DROP TABLE IF EXISTS Class;                     -- пара
DROP TABLE IF EXISTS Term_Stream_By_Course;     -- семестр у потока по предмету
DROP TABLE IF EXISTS Group_Tb;                  -- группа
DROP TABLE IF EXISTS Teacher_Department;        -- преподаватель на кафедре
DROP TABLE IF EXISTS Direction_Department;      -- направление на кафедре
DROP TABLE IF EXISTS Classroom;                 -- аудитория
DROP TABLE IF EXISTS Department;                -- кафедра
DROP TABLE IF EXISTS Teacher;                   -- преподаватель
DROP TABLE IF EXISTS Building;                  -- корпус
DROP TABLE IF EXISTS Course;                    -- предмет
DROP TABLE IF EXISTS Stream;                    -- поток
DROP TABLE IF EXISTS Direction;                 -- направление


-- Создание схемы данных
CREATE TABLE Direction (
    Code VARCHAR PRIMARY KEY,
    Name VARCHAR NOT NULL
);


CREATE TABLE Course (
    Name VARCHAR PRIMARY KEY
);


CREATE TABLE Building (
    Address VARCHAR PRIMARY KEY
);


CREATE TABLE Teacher (
    Emp_Record_Num VARCHAR PRIMARY KEY,
    Full_Name VARCHAR NOT NULL,
    Position VARCHAR
);


CREATE TABLE Department (
    Dep_Number SMALLINT PRIMARY KEY,
    Name VARCHAR,
    CHECK(Dep_Number > 0)
);


CREATE TABLE Classroom (
    Room_Number VARCHAR,
    Building_Address VARCHAR,
    FOREIGN KEY (Building_Address) REFERENCES Building(Address) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Room_Number, Building_Address)
);


CREATE TABLE Teacher_Department (
    Teacher_Dep_Number SMALLINT,
    Teacher_Emp_Record_Num VARCHAR,
    FOREIGN KEY (Teacher_Dep_Number) REFERENCES Department(Dep_Number) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Teacher_Emp_Record_Num) REFERENCES Teacher(Emp_Record_Num) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Teacher_Dep_Number, Teacher_Emp_Record_Num),
    CHECK(Teacher_Dep_Number > 0)
);


CREATE TABLE Direction_Department (
    Dir_Code VARCHAR,
    Direction_Dep_Number SMALLINT,
    FOREIGN KEY (Dir_Code) REFERENCES Direction(Code) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Direction_Dep_Number) REFERENCES Department(Dep_Number) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Dir_Code, Direction_Dep_Number),
    CHECK(Direction_Dep_Number > 0)
);


CREATE TABLE Stream (
    Entry_Year SMALLINT,
    Stream_Dir_Code VARCHAR,
    FOREIGN KEY (Stream_Dir_Code) REFERENCES Direction(Code) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Entry_Year, Stream_Dir_Code),
    CHECK(Entry_Year > 0)
);


CREATE TABLE Group_Tb (
    Group_Number VARCHAR PRIMARY KEY,
    Curr_Term SMALLINT,
    Group_Dir_Code VARCHAR,
    Group_Entry_Year SMALLINT,
    FOREIGN KEY (Group_Dir_Code, Group_Entry_Year) REFERENCES Stream(Stream_Dir_Code, Entry_Year) ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK(Curr_Term > 0 AND Group_Entry_Year > 0)
);


CREATE TABLE Term_Stream_By_Course (
    Term_Number SMALLINT,
    Lec_Hours SMALLINT,
    Lab_Hours SMALLINT,
    Att_Type VARCHAR,
    Stream_Dir_Code VARCHAR,
    Stream_Entry_Year SMALLINT,
    Course_Name VARCHAR,
    FOREIGN KEY (Stream_Dir_Code, Stream_Entry_Year) REFERENCES Stream(Stream_Dir_Code, Entry_Year) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Course_Name) REFERENCES Course(Name) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Term_Number, Stream_Dir_Code, Stream_Entry_Year, Course_Name),
    CHECK(Lec_Hours >= 0 AND Lab_Hours >= 0 AND Stream_Entry_Year > 0 AND Term_Number > 0)
);


CREATE TABLE Class (
    Week_Day VARCHAR,
    Class_Number SMALLINT,
    Week_Type VARCHAR,
    Room_Number VARCHAR,
    Building_Address VARCHAR,
    Class_Course_Name VARCHAR,
    Teacher_Emp_Record_Num VARCHAR,
    FOREIGN KEY (Room_Number, Building_Address) REFERENCES Classroom(Room_Number, Building_Address) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Class_Course_Name) REFERENCES Course(Name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Teacher_Emp_Record_Num) REFERENCES Teacher(Emp_Record_Num) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Week_Day, Class_Number, Week_Type, Room_Number, Building_Address),
    CHECK(Class_Number > 0 AND Class_Number < 8)
);


CREATE TABLE Group_Class (
    Group_Number VARCHAR,
    Week_Day VARCHAR,
    Class_Number SMALLINT,
    Week_Type VARCHAR,
    Room_Number VARCHAR,
    Building_Address VARCHAR,
    FOREIGN KEY (Group_Number) REFERENCES Group_Tb(Group_Number) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Week_Day, Class_Number, Week_Type, Room_Number, Building_Address) REFERENCES Class(Week_Day, Class_Number, Week_Type, Room_Number, Building_Address) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (Group_Number, Week_Day, Class_Number, Week_Type, Room_Number, Building_Address),
    CHECK(Class_Number > 0 AND Class_Number < 8)
);

CREATE TABLE day_of_week (
    day VARCHAR,
    day_number SMALLINT PRIMARY KEY
);

CREATE TABLE admin (
    id SMALLINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL
);