import java.util.Arrays;

/**
 * =====================================================================
 *  STUDENT MANAGEMENT SYSTEM
 *  A Java OOP demo project.
 *
 *  Concepts demonstrated:
 *   - Classes & Objects       (Student, Classroom)
 *   - Encapsulation           (private fields, public methods)
 *   - Arrays                  (array of grades, array of Student objects)
 *   - Methods                 (constructors, getters, behavior methods)
 *   - Problem solving          (searching, sorting, computing statistics)
 * =====================================================================
 */

/**
 * Represents a single student: a name, an ID, and an array of grades.
 */
class Student {
    private String name;
    private int id;
    private double[] grades;
    private int gradeCount; // how many grade slots are actually filled

    public Student(String name, int id, int maxGrades) {
        this.name = name;
        this.id = id;
        this.grades = new double[maxGrades];
        this.gradeCount = 0;
    }

    /** Adds a grade into the next free slot of the grades array. */
    public void addGrade(double grade) {
        if (gradeCount < grades.length) {
            grades[gradeCount] = grade;
            gradeCount++;
        } else {
            System.out.println("Cannot add more grades for " + name + " -- array is full.");
        }
    }

    public double getAverage() {
        if (gradeCount == 0) return 0.0;
        double sum = 0;
        for (int i = 0; i < gradeCount; i++) {
            sum += grades[i];
        }
        return sum / gradeCount;
    }

    public double getHighestGrade() {
        if (gradeCount == 0) return 0.0;
        double highest = grades[0];
        for (int i = 1; i < gradeCount; i++) {
            if (grades[i] > highest) highest = grades[i];
        }
        return highest;
    }

    public char getLetterGrade() {
        double avg = getAverage();
        if (avg >= 90) return 'A';
        else if (avg >= 80) return 'B';
        else if (avg >= 70) return 'C';
        else if (avg >= 60) return 'D';
        else return 'F';
    }

    public String getName() { return name; }
    public int getId() { return id; }

    public void display() {
        System.out.printf("ID: %-4d Name: %-16s Average: %-6.2f Grade: %c%n",
                id, name, getAverage(), getLetterGrade());
    }
}

/**
 * Manages a collection of Student objects using an array.
 * Demonstrates object composition, arrays of objects, and simple algorithms.
 */
class Classroom {
    private Student[] students;
    private int studentCount;

    public Classroom(int capacity) {
        students = new Student[capacity];
        studentCount = 0;
    }

    public boolean addStudent(Student s) {
        if (studentCount >= students.length) {
            System.out.println("Classroom is full. Cannot add " + s.getName());
            return false;
        }
        students[studentCount] = s;
        studentCount++;
        return true;
    }

    /** Linear search through the student array by ID. */
    public Student findStudentById(int id) {
        for (int i = 0; i < studentCount; i++) {
            if (students[i].getId() == id) {
                return students[i];
            }
        }
        return null;
    }

    public double classAverage() {
        if (studentCount == 0) return 0.0;
        double total = 0;
        for (int i = 0; i < studentCount; i++) {
            total += students[i].getAverage();
        }
        return total / studentCount;
    }

    public Student topStudent() {
        if (studentCount == 0) return null;
        Student top = students[0];
        for (int i = 1; i < studentCount; i++) {
            if (students[i].getAverage() > top.getAverage()) {
                top = students[i];
            }
        }
        return top;
    }

    /**
     * Bubble sort by average grade, descending.
     * Written by hand (rather than using a library sort) to demonstrate
     * basic algorithmic problem solving.
     */
    public void sortByAverageDescending() {
        for (int i = 0; i < studentCount - 1; i++) {
            for (int j = 0; j < studentCount - 1 - i; j++) {
                if (students[j].getAverage() < students[j + 1].getAverage()) {
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }
            }
        }
    }

    public void printReport() {
        System.out.println("=== Class Report (sorted by average, highest first) ===");
        sortByAverageDescending();
        for (int i = 0; i < studentCount; i++) {
            students[i].display();
        }
        System.out.printf("Class average: %.2f%n", classAverage());
        Student top = topStudent();
        if (top != null) {
            System.out.println("Top student: " + top.getName());
        }
    }
}

/**
 * Entry point. Builds a small classroom, adds students and grades,
 * then exercises the reporting and search functionality.
 */
public class StudentManagementSystem {
    public static void main(String[] args) {
        Classroom classroom = new Classroom(5);

        Student s1 = new Student("Alice Johnson", 101, 5);
        s1.addGrade(92); s1.addGrade(88); s1.addGrade(95);

        Student s2 = new Student("Brian Lee", 102, 5);
        s2.addGrade(78); s2.addGrade(82); s2.addGrade(75);

        Student s3 = new Student("Carla Mendez", 103, 5);
        s3.addGrade(65); s3.addGrade(70); s3.addGrade(68);

        Student s4 = new Student("David Kim", 104, 5);
        s4.addGrade(99); s4.addGrade(97); s4.addGrade(100);

        classroom.addStudent(s1);
        classroom.addStudent(s2);
        classroom.addStudent(s3);
        classroom.addStudent(s4);

        classroom.printReport();

        System.out.println();
        int searchId = 103;
        Student found = classroom.findStudentById(searchId);
        if (found != null) {
            System.out.println("Found student " + searchId + ":");
            found.display();
        } else {
            System.out.println("No student found with ID " + searchId);
        }
    }
}
