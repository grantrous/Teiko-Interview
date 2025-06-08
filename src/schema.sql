PRAGMA foreign_keys = ON;

-- Drop existing tables in reverse order of dependencies
DROP TABLE IF EXISTS cell_counts;
DROP TABLE IF EXISTS samples;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS projects;

-- Create tables in order of dependencies
CREATE TABLE projects (
    project TEXT PRIMARY KEY
);

CREATE TABLE subjects (
    subject TEXT PRIMARY KEY,
    age INTEGER,
    sex TEXT CHECK (sex IN ('M', 'F')),
    condition TEXT
);

CREATE TABLE treatments (
    treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    treatment TEXT UNIQUE NOT NULL
);

CREATE TABLE samples (
    sample TEXT PRIMARY KEY,
    project TEXT,
    subject TEXT,
    treatment_id INTEGER,
    sample_type TEXT,
    time_from_treatment_start INTEGER,
    response TEXT,
    FOREIGN KEY (project) REFERENCES projects(project),
    FOREIGN KEY (subject) REFERENCES subjects(subject),
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
);

CREATE TABLE cell_counts (
    sample TEXT,
    b_cell INTEGER,
    cd8_t_cell INTEGER,
    cd4_t_cell INTEGER,
    nk_cell INTEGER,
    monocyte INTEGER,
    FOREIGN KEY (sample) REFERENCES samples(sample)
);