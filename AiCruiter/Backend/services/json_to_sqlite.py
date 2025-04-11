import sqlite3
import json

class ResumeDatabase:
    def __init__(self, db_name="resumes.db"):
        self.conn = sqlite3.connect(db_name,check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                certifications TEXT,
                achievements TEXT,
                tech_stack TEXT,
                resume_id TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def resume_exists(self, resume_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM resumes WHERE resume_id = ?', (json.dumps(resume_id),))
        return cursor.fetchone() is not None

    def insert_resume(self, resume):
        resume_id = resume.get("resume_id")
        if resume_id and not self.resume_exists(resume_id):
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO resumes (name, email, phone, skills, education, experience, certifications, achievements, tech_stack, resume_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                resume.get("name"),
                resume.get("email"),
                resume.get("phone"),
                json.dumps(resume.get("skills")),
                json.dumps(resume.get("education")),
                json.dumps(resume.get("experience")),
                json.dumps(resume.get("certifications")),
                json.dumps(resume.get("achievements")),
                json.dumps(resume.get("tech_stack")),
                json.dumps(resume.get("resume_id"))
            ))
            self.conn.commit()
            return cursor.lastrowid
        else:
            return None  # Resume already exists or no resume_id
    
    def get_resume_by_sql_id(self, sql_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (sql_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "skills": json.loads(row[4]),
                "education": json.loads(row[5]),
                "experience": json.loads(row[6]),
                "certifications": json.loads(row[7]),
                "achievements": json.loads(row[8]),
                "tech_stack": json.loads(row[9]),
                "resume_id": json.loads(row[10])
            }
        return None
    def close(self):
        self.conn.close()
