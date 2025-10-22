-- ---------------------------------------------------
-- 1) CREATE students table
-- ---------------------------------------------------
CREATE TABLE students (
    student_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_name VARCHAR2(100),
    marks NUMBER(5,2),        
    grade VARCHAR2(2),         
    created_at DATE DEFAULT SYSDATE
);

-- ---------------------------------------------------
-- 2) CREATE student_audit table (to log changes)
-- ---------------------------------------------------
CREATE TABLE student_audit (
    audit_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    student_id NUMBER,
    operation VARCHAR2(10),       
    old_marks NUMBER(5,2),
    new_marks NUMBER(5,2),
    old_grade VARCHAR2(2),
    new_grade VARCHAR2(2),
    changed_by VARCHAR2(30),      
    changed_at DATE DEFAULT SYSDATE
);


INSERT INTO students (student_name, marks) VALUES ('Aisha Sharma', 95);
INSERT INTO students (student_name, marks) VALUES ('Rohit Kumar', 82.5);

-- ---------------------------------------------------
-- 3) BEFORE trigger: assign grade automatically
--    (runs before each row is inserted or updated)
-- ---------------------------------------------------
CREATE OR REPLACE TRIGGER trg_assign_grade
BEFORE INSERT OR UPDATE ON students
FOR EACH ROW
BEGIN
    IF :NEW.marks IS NULL THEN
        :NEW.grade := NULL;
    ELSE
        IF :NEW.marks >= 90 THEN
            :NEW.grade := 'A';
        ELSIF :NEW.marks >= 80 THEN
            :NEW.grade := 'B';
        ELSIF :NEW.marks >= 70 THEN
            :NEW.grade := 'C';
        ELSIF :NEW.marks >= 60 THEN
            :NEW.grade := 'D';
        ELSE
            :NEW.grade := 'F';
        END IF;
    END IF;

END;

-- ---------------------------------------------------
-- 4) AFTER trigger: log changes into student_audit
--    (runs after each row is inserted or updated)
-- ---------------------------------------------------
CREATE OR REPLACE TRIGGER trg_student_audit
AFTER INSERT OR UPDATE ON students
FOR EACH ROW
DECLARE
    v_op VARCHAR2(10);
BEGIN
    -- Determine operation type
    IF INSERTING THEN
        v_op := 'INSERT';
    ELSIF UPDATING THEN
        v_op := 'UPDATE';
    ELSE
        v_op := 'OTHER';
    END IF;

    -- Insert audit record capturing old/new marks and grades
    INSERT INTO student_audit (
        student_id,
        operation,
        old_marks,
        new_marks,
        old_grade,
        new_grade,
        changed_by,
        changed_at
    ) VALUES (
        NVL(:NEW.student_id, -1), -- should be present; -1 just as safe fallback
        v_op,
        :OLD.marks,
        :NEW.marks,
        :OLD.grade,
        :NEW.grade,
        USER,         -- Oracle USER returns current DB username
        SYSDATE
    );
END;

INSERT INTO students (student_name, marks) VALUES ('Meena Patel', 74);
INSERT INTO students (student_name, marks) VALUES ('Vikram Singh', 59.99);
INSERT INTO students (student_name, marks) VALUES ('Sara Jain', NULL);

-- ---------------------------------------------------
-- 6) Verify students table
-- ---------------------------------------------------
SELECT student_id, student_name, marks, grade, TO_CHAR(created_at,'YYYY-MM-DD HH24:MI:SS') created_at
FROM students
ORDER BY student_id;

-- ---------------------------------------------------
-- 7) Example update (changes marks -> grade updates and audit logs)
-- ---------------------------------------------------
UPDATE students
SET marks = 88
WHERE student_name = 'Meena Patel';
COMMIT;

-- Update marks for a student who previously had NULL marks
UPDATE students
SET marks = 67
WHERE student_name = 'Sara Jain';
COMMIT;

-- ---------------------------------------------------
-- 8) Verify audit log
-- ---------------------------------------------------
SELECT audit_id,
       student_id,
       operation,
       old_marks,
       new_marks,
       old_grade,
       new_grade,
       changed_by,
       TO_CHAR(changed_at,'YYYY-MM-DD HH24:MI:SS') changed_at
FROM student_audit
ORDER BY audit_id;