import sqlite3
import pandas as pd
import os

def initialize_db(db_name, schema_file):
    """Initialize database with schema"""
    # Remove existing database to ensure clean start
    if os.path.exists(db_name):
        os.remove(db_name)
    
    conn = sqlite3.connect(db_name)
    with open(schema_file, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database {db_name} initialized with schema")

def process_and_load_data(db_name, df):
    """Process and load CSV data into database tables"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Load projects
        projects = pd.DataFrame({'project': df['project'].unique()})
        projects.to_sql('projects', conn, if_exists='replace', index=False)
        
        # Load subjects
        subjects = df[['subject', 'age', 'sex', 'condition']].drop_duplicates().copy()
        subjects.to_sql('subjects', conn, if_exists='replace', index=False)
        
        # Load treatments
        treatments = pd.DataFrame({'treatment': df['treatment'].unique()})
        treatments.reset_index(drop=True, inplace=True)
        treatments.index += 1  # Start treatment_id from 1
        treatments.to_sql('treatments', conn, if_exists='replace', index=True, index_label='treatment_id')
        
        # Load samples with treatment_id mapping
        samples = df[['sample', 'project', 'subject', 'treatment', 
                     'sample_type', 'time_from_treatment_start', 'response']].copy()
        
        # Get treatment mapping
        treatment_map = pd.read_sql("SELECT treatment_id, treatment FROM treatments", conn)
        treatment_dict = dict(zip(treatment_map['treatment'], treatment_map['treatment_id']))
        
        # Map treatments to IDs
        samples['treatment_id'] = samples['treatment'].map(treatment_dict)
        samples = samples.drop('treatment', axis=1)
        samples.to_sql('samples', conn, if_exists='replace', index=False)
        
        # Load cell counts
        cell_counts = df[['sample', 'b_cell', 'cd8_t_cell', 'cd4_t_cell', 
                         'nk_cell', 'monocyte']].copy()
        cell_counts.to_sql('cell_counts', conn, if_exists='replace', index=False)
        
        conn.commit()
        
        # Verify data was loaded
        cursor.execute("SELECT COUNT(*) FROM samples")
        count = cursor.fetchone()[0]
        print(f"Successfully loaded {count} samples")
        
        return count > 0

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def load_data(db_name):
    """Load all data from database with proper table joins"""
    if not os.path.exists(db_name):
        print(f"Database {db_name} does not exist")
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_name)
    
    try:
        query = """
        SELECT 
            s.sample,
            p.project,
            sub.subject,
            sub.age,
            sub.sex,
            sub.condition,
            t.treatment,
            s.sample_type,
            s.time_from_treatment_start,
            s.response,
            c.b_cell,
            c.cd8_t_cell,
            c.cd4_t_cell,
            c.nk_cell,
            c.monocyte
        FROM samples s
        JOIN projects p ON s.project = p.project
        JOIN subjects sub ON s.subject = sub.subject
        JOIN treatments t ON s.treatment_id = t.treatment_id
        LEFT JOIN cell_counts c ON s.sample = c.sample
        ORDER BY s.sample
        """
        
        df = pd.read_sql_query(query, conn)
        print(f"Retrieved {len(df)} rows from database")
        return df
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def remove_sample(db_name, table_name, sample_id):
    """Remove a sample and its related data"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Remove cell counts first (child table)
        cursor.execute("DELETE FROM cell_counts WHERE sample = ?", (sample_id,))
        
        # Remove sample (parent table)
        cursor.execute("DELETE FROM samples WHERE sample = ?", (sample_id,))
        
        conn.commit()
        
        # Check if removal was successful
        cursor.execute("SELECT COUNT(*) FROM samples WHERE sample = ?", (sample_id,))
        count = cursor.fetchone()[0]
        
        return count == 0
        
    except sqlite3.Error as e:
        print(f"Error removing sample: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def add_sample(db_name, sample_data):
    """Add a new sample to the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if sample already exists
        cursor.execute("SELECT COUNT(*) FROM samples WHERE sample = ?", (sample_data['sample'],))
        if cursor.fetchone()[0] > 0:
            print(f"Sample {sample_data['sample']} already exists")
            return False
        
        # Get treatment_id
        cursor.execute("SELECT treatment_id FROM treatments WHERE treatment = ?", 
                      (sample_data['treatment'],))
        result = cursor.fetchone()
        if not result:
            # Add new treatment if it doesn't exist
            cursor.execute("INSERT INTO treatments (treatment) VALUES (?)", 
                          (sample_data['treatment'],))
            treatment_id = cursor.lastrowid
        else:
            treatment_id = result[0]
        
        # Add project if it doesn't exist
        cursor.execute("INSERT OR IGNORE INTO projects (project) VALUES (?)", 
                      (sample_data['project'],))
        
        # Add subject if it doesn't exist
        cursor.execute("""INSERT OR IGNORE INTO subjects 
                         (subject, age, sex, condition) VALUES (?, ?, ?, ?)""", 
                      (sample_data['subject'], sample_data['age'], 
                       sample_data['sex'], sample_data['condition']))
        
        # Add sample
        cursor.execute("""INSERT INTO samples 
                         (sample, project, subject, treatment_id, sample_type, 
                          time_from_treatment_start, response) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)""",
                      (sample_data['sample'], sample_data['project'], 
                       sample_data['subject'], treatment_id, sample_data['sample_type'],
                       sample_data['time_from_treatment_start'], sample_data['response']))
        
        # Add cell counts
        cursor.execute("""INSERT INTO cell_counts 
                         (sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (sample_data['sample'], sample_data['b_cell'], 
                       sample_data['cd8_t_cell'], sample_data['cd4_t_cell'],
                       sample_data['nk_cell'], sample_data['monocyte']))
        
        conn.commit()
        return True
        
    except sqlite3.Error as e:
        print(f"Error adding sample: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()