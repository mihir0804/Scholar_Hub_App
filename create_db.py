import sqlite3

conn = sqlite3.connect("Scholar_Hub.db")
cursor = conn.cursor()

# -------------------- Create Tables --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY,
    level_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS streams (
    id INTEGER PRIMARY KEY,
    stream_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY,
    exam_name TEXT,
    level_id INTEGER,
    stream_id INTEGER,
    FOREIGN KEY(level_id) REFERENCES levels(id),
    FOREIGN KEY(stream_id) REFERENCES streams(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    subject TEXT,
    teacher_name TEXT,
    youtube_url TEXT,
    rating INTEGER,
    FOREIGN KEY(exam_id) REFERENCES exams(id)
)
""")

# -------------------- Insert Levels --------------------
cursor.executemany("INSERT OR IGNORE INTO levels (id, level_name) VALUES (?, ?)", [
    (1, "Class 10"),
    (2, "Class 11"),
    (3, "Class 12")
])

# -------------------- Insert Streams --------------------
cursor.executemany("INSERT OR IGNORE INTO streams (id, stream_name) VALUES (?, ?)", [
    (1, "Science"),
    (2, "Commerce"),
    (3, "Arts")
])

# -------------------- Insert Exams --------------------
cursor.executemany("INSERT OR IGNORE INTO exams (id, exam_name, level_id, stream_id) VALUES (?, ?, ?, ?)", [
    (1, "Board Exam", 1, None),

    (37, "Class 11 Science CBSE", 2, 1),
    (38, "Class 11 Commerce CBSE", 2, 2),
    (39, "Class 11 Arts CBSE", 2, 3),

    (6, "CA Foundation", 3, 2),
    (7, "CS Foundation", 3, 2),
    (8, "CMA Foundation", 3, 2),
    (9, "CFP Exam", 3, 2),
    (10, "CPA Exam", 3, 2),
    (11, "B.Com Entrance", 3, 2),
    (12, "BBA Entrance", 3, 2),
    (13, "B.Econ Entrance", 3, 2),
    (14, "LLB Entrance", 3, 2),
    (15, "Investment Banking Prep", 3, 2),
    (16, "Financial Analyst Prep", 3, 2),
    (17, "Data Analyst Prep", 3, 2),
    (18, "Digital Marketing Prep", 3, 2),
    (19, "BA LLB Entrance", 3, 3),
    (20, "Journalism & Mass Comm Entrance", 3, 3),
    (21, "Hotel Management Entrance", 3, 3),
    (22, "Fashion Design Entrance", 3, 3),
    (23, "Psychology Entrance", 3, 3),
    (24, "Social Work Entrance", 3, 3),
    (25, "UPSC Civil Services", 3, 3),
    (26, "Fine Arts & Performing Arts", 3, 3),
    (27, "Digital Marketing Prep", 3, 3),
    (28, "Engineering Entrance (JEE Main)", 3, 1),
    (29, "Architecture Entrance (NATA)", 3, 1),
    (30, "Computer Applications & IT Entrance", 3, 1),
    (31, "Defense & Merchant Navy Entrance", 3, 1),
    (32, "NEET (MBBS/BDS) Entrance", 3, 1),
    (33, "Allied Health Sciences Entrance", 3, 1),
    (34, "Biotechnology Entrance", 3, 1),
    (35, "Pharmacy Entrance", 3, 1),
    (36, "Veterinary Sciences Entrance", 3, 1)
])

# -------------------- Insert Resources --------------------
cursor.executemany("""
INSERT OR IGNORE INTO resources (exam_id, subject, teacher_name, youtube_url, rating)
VALUES (?, ?, ?, ?, ?)
""", [
    # Class 10
    (1, "Science", "Physics Wallah", "https://www.youtube.com/@PhysicsWallah", 5),
    (1, "Science", "Vedantu Class 9 & 10", "https://www.youtube.com/@VedantuClass910", 5),
    (1, "Mathematics", "Dear Sir", "https://www.youtube.com/@DearSir", 5),
    (1, "Mathematics", "Vedantu Class 9 & 10", "https://www.youtube.com/@VedantuClass910", 5),
    (1, "English", "English Academy", "https://www.youtube.com/@englishacademy", 5),
    (1, "English", "Shipra Mishra", "https://www.youtube.com/@ShipraMishra", 5),
    (1, "English", "Unacademy Class 10", "https://www.youtube.com/@UnacademyClass10", 5),
    (1, "Social Science", "Magnet Brains - Dhiraj Sir", "https://www.youtube.com/@MagnetBrainsEducation", 5),
    (1, "Social Science", "Vedantu Class 9 & 10", "https://www.youtube.com/@VedantuClass910", 5),
    (1, "Social Science", "Unacademy Class 10", "https://www.youtube.com/@UnacademyClass10", 5),

    # Class 11 Science
    (37, "Physics", "Physics Wallah", "https://www.youtube.com/@PhysicsWallah", 5),
    (37, "Chemistry", "Physics Wallah", "https://www.youtube.com/@PhysicsWallah", 5),
    (37, "Biology", "Biology at Ease", "https://www.youtube.com/@BiologyAtEase", 5),
    (37, "Mathematics", "Mathematics Wallah", "https://www.youtube.com/@MathematicsWallah", 5),

    # Class 11 Commerce
    (38, "Accountancy", "Sunil Panda", "https://www.youtube.com/@SunilPanda", 5),
    (38, "Accountancy", "CA Parag Gupta", "https://www.youtube.com/@CAParagGupta", 5),
    (38, "Accountancy", "Commerce Baba", "https://www.youtube.com/@CommerceBaba", 5),
    (38, "Economics", "Rajat Arora", "https://www.youtube.com/@RajatAroraEconomics", 5),

    # Class 11 Arts
    (39, "Psychology", "Syllabus with Rohit", "https://www.youtube.com/@SyllabuswithRohit", 5),
    (39, "Sociology", "Sleepy Classes IAS", "https://www.youtube.com/@SleepyClassesIAS", 5),

    # Class 12 & Competitive
    (28, "JEE Prep", "Vidyapeeth PW", "https://www.youtube.com/@VidyapeethPW", 5),
    (29, "Architecture (NATA)", "PW Design & Arch", "https://www.youtube.com/@PWDesignandArch", 5),
    (32, "NEET Prep", "Vidyapeeth PW", "https://www.youtube.com/@VidyapeethPW/playlists", 5),
    (25, "UPSC", "Drishti IAS", "https://www.youtube.com/@DrishtiIASvideos", 5),
    (6, "CA Foundation", "CA Wallah", "https://www.youtube.com/@CAWallahbyPW", 5),
    (7, "CS Foundation", "CS Wallah", "https://www.youtube.com/@PW-CSWallah", 5),
    (8, "CMA Foundation", "Finology PK", "https://www.youtube.com/@finologywithpk", 5),
    (9, "CFP Exam", "Zell Education", "https://www.youtube.com/@ZellEducation/featured", 5),
    (10, "CPA Exam", "NorthStar Academy", "https://www.youtube.com/@NorthStarAcademy/videos", 5),
    (35, "Pharmacy", "Imperfect Pharmacy", "https://www.youtube.com/@imperfectpharmacy", 5),
    (34, "Biotechnology", "Biotecnika", "https://www.youtube.com/@biotecnika/playlists", 5),
    (33, "Allied Health", "Medicosis Perfectionalis", "https://www.youtube.com/@MedicosisPerfectionalis/playlists", 5),
    (17, "Data Analytics", "WsCube Tech", "https://www.youtube.com/@wscubetech", 5),

    # Other
    (18, "Digital Marketing", "WsCube Tech", "https://www.youtube.com/@wscubetech", 5),
    (20, "Mass Comm & Journalism", "Media Mentor", "https://www.youtube.com/@MEDIAMENTOR", 5),
    (21, "Hotel Management", "DOT NET Institute", "https://www.youtube.com/@DOTNETInstitute", 5),
    (22, "Fashion Design", "Art and Design by Miraaz", "https://www.youtube.com/@artanddesignbymiraaz", 5),
    (23, "Psychology", "Next Guru by R.K. Vaishnav", "https://www.youtube.com/@Nextgurubyr.k.vaishnav", 5),
    (26, "Fine Arts", "Imagination Academy", "https://www.youtube.com/@imaginationacademyoffinear3926", 5)
])

conn.commit()
conn.close()

print("✅ Scholar_Hub database created and updated successfully.")
