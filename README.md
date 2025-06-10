# Clinical Trial Data Management System

A comprehensive Python application for managing and analyzing clinical trial data, specifically designed for Bob Loblaw at Loblaw Bio to explore immune cell population data and predict treatment responses.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone or download the project files**
2. **Navigate to the project directory**
   ```bash
   cd streamlit-csv-db-app
   ```

3. **Install required dependencies**
   ```bash
   pip install streamlit pandas sqlite3 plotly scipy numpy
   ```
   
   Or if you have a requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   cd src
   streamlit run app.py
   ```

5. **Access the application**
   - Open your web browser and go to `http://localhost:8501`
   - The application will start with an empty database

## 📄 CSV Data Format Requirements

### Required Column Headers

Your CSV file **must** contain the following columns with exact header names:

```csv
sample,project,subject,age,sex,condition,treatment,sample_type,time_from_treatment_start,response,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
```

### Column Specifications

| Column | Data Type | Description | Example Values | Required |
|--------|-----------|-------------|----------------|----------|
| `sample` | TEXT | Unique sample identifier | "SAMPLE_00001", "MEL_001_T0" | ✅ |
| `project` | TEXT | Project/study identifier | "MELANO_001", "IMMUNO_BOOST" | ✅ |
| `subject` | TEXT | Unique subject/patient identifier | "SUB_001", "PATIENT_123" | ✅ |
| `age` | INTEGER | Subject age in years | 45, 67, 23 | ✅ |
| `sex` | TEXT | Subject biological sex | "M", "F" | ✅ |
| `condition` | TEXT | Medical condition/diagnosis | "melanoma", "healthy", "lung_cancer" | ✅ |
| `treatment` | TEXT | Treatment received | "tr1", "tr2", "placebo" | ✅ |
| `sample_type` | TEXT | Type of biological sample | "PBMC", "tumor", "serum" | ✅ |
| `time_from_treatment_start` | INTEGER | Days since treatment began | 0, 7, 28, 84 | ✅ |
| `response` | TEXT | Treatment response status | "y" (responder), "n" (non-responder), "" (unknown) | ⚠️ Optional |
| `b_cell` | INTEGER | B cell count | 500, 1200, 800 | ✅ |
| `cd8_t_cell` | INTEGER | CD8+ T cell count | 1500, 2800, 1200 | ✅ |
| `cd4_t_cell` | INTEGER | CD4+ T cell count | 2000, 3500, 1800 | ✅ |
| `nk_cell` | INTEGER | Natural killer cell count | 800, 1500, 600 | ✅ |
| `monocyte` | INTEGER | Monocyte count | 1000, 2000, 1200 | ✅ |

### Sample CSV Format

```csv
sample,project,subject,age,sex,condition,treatment,sample_type,time_from_treatment_start,response,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
SAMPLE_00001,MELANO_001,SUB_001,45,M,melanoma,tr1,PBMC,0,y,800,2200,2800,1000,1500
SAMPLE_00002,MELANO_001,SUB_001,45,M,melanoma,tr1,PBMC,28,y,750,2500,3200,1200,1400
SAMPLE_00003,MELANO_001,SUB_002,52,F,melanoma,tr1,PBMC,0,n,600,1800,2400,800,1300
SAMPLE_00004,IMMUNO_BOOST,SUB_003,38,F,healthy,placebo,PBMC,0,,700,1500,2200,600,1100
```

### Data Validation Rules

#### Required Data Integrity
- **Unique Samples**: Each `sample` value must be unique across the entire dataset
- **Consistent Subjects**: Same `subject` should have consistent `age`, `sex`, and `condition` across all their samples
- **Positive Counts**: All cell count columns must contain non-negative integers
- **Valid Response Values**: `response` column accepts only "y", "n", or empty string ""

#### Recommended Practices
- **Time Points**: Use consistent time intervals (e.g., 0, 7, 14, 28, 56, 84, 168 days)
- **Naming Conventions**: Use consistent, descriptive naming for projects and subjects
- **Baseline Inclusion**: Include baseline samples (`time_from_treatment_start = 0`) for longitudinal analysis

### Example Data Scenarios

#### Longitudinal Study
```csv
sample,project,subject,age,sex,condition,treatment,sample_type,time_from_treatment_start,response,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
BASE_001,MELANO_001,PATIENT_001,45,M,melanoma,tr1,PBMC,0,y,800,2200,2800,1000,1500
WEEK4_001,MELANO_001,PATIENT_001,45,M,melanoma,tr1,PBMC,28,y,750,2500,3200,1200,1400
WEEK12_001,MELANO_001,PATIENT_001,45,M,melanoma,tr1,PBMC,84,y,700,2800,3500,1400,1300
```

#### Multi-Project Study
```csv
sample,project,subject,age,sex,condition,treatment,sample_type,time_from_treatment_start,response,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
MEL001_S001,MELANO_001,SUB_001,45,M,melanoma,tr1,PBMC,0,y,800,2200,2800,1000,1500
IMM001_S001,IMMUNO_BOOST,SUB_002,52,F,lung_cancer,tr2,PBMC,0,n,600,1800,2400,800,1300
BIO001_S001,BIOMARKER_STUDY,SUB_003,38,F,healthy,placebo,PBMC,0,,700,1500,2200,600,1100
```

### Common CSV Issues to Avoid

❌ **Don't do this:**
- Missing required columns
- Inconsistent column names (e.g., "cd8_tcell" instead of "cd8_t_cell")
- Negative cell counts
- Invalid response values (e.g., "yes" instead of "y")
- Duplicate sample IDs
- Missing data in required fields

✅ **Do this:**
- Follow exact column naming conventions
- Ensure all required columns are present
- Use consistent data formats
- Include baseline samples for treatment studies
- Validate data before upload

### Testing Your CSV

Before uploading, verify your CSV:

1. **Column Check**: Ensure all 15 required columns are present with exact names
2. **Data Types**: Verify integers for age, time, and cell counts
3. **Required Fields**: Check no empty values in required columns
4. **Unique Samples**: Confirm each sample ID appears only once
5. **Response Values**: Verify only "y", "n", or "" in response column

### Generating Test Data

Use the included data generator for testing:
```bash
python generate_big_dataset.py
```
This creates `big-cell-counts.csv` with 500+ realistic samples for testing application performance and features.

## 🔬 Scientific Analysis Features

### Running the Analysis

1. **Load Data**: Upload your CSV file using the file uploader
2. **Initialize Database**: Click "Load Data into Database" 
3. **Explore Analysis Tabs**:
   - **Frequency Analysis**: Answers "What is the frequency of each cell type in each sample?"
   - **Treatment Response**: Compares responders vs non-responders for tr1 treatment
   - **Baseline Analysis**: Filters melanoma PBMC samples at baseline
   - **Custom Filtering**: Flexible data exploration tool

### Reproducing Key Outputs

#### Cell Type Frequency Analysis
- Navigate to "Frequency Analysis" tab
- View the summary table with sample, total_count, population, count, and percentage columns
- Download results as CSV using the download button

#### Treatment Response Prediction
- Go to "Treatment Response" tab
- Statistical analysis automatically filters for melanoma patients with tr1 treatment and PBMC samples
- Results include t-tests, p-values, and effect sizes for each cell population
- Box plots show visual comparisons between responders and non-responders

#### Baseline Subset Analysis
- Use "Baseline Analysis" tab for automatic filtering of baseline (time=0) samples
- Get instant summaries of:
  - Samples per project
  - Responder/non-responder counts
  - Male/female distribution
  - Cross-tabulation analyses

## 🗃️ Database Schema Design

### Schema Overview

The relational database uses a normalized design with five interconnected tables:

```sql
projects (project: TEXT PRIMARY KEY)
subjects (subject: TEXT PRIMARY KEY, age: INTEGER, sex: TEXT, condition: TEXT)
treatments (treatment_id: INTEGER PRIMARY KEY, treatment: TEXT UNIQUE)
samples (sample: TEXT PRIMARY KEY, project: TEXT, subject: TEXT, treatment_id: INTEGER, 
         sample_type: TEXT, time_from_treatment_start: INTEGER, response: TEXT)
cell_counts (sample: TEXT, b_cell: INTEGER, cd8_t_cell: INTEGER, cd4_t_cell: INTEGER, 
             nk_cell: INTEGER, monocyte: INTEGER)
```

### Design Rationale

#### 1. **Normalization Benefits**
- **Eliminates Data Redundancy**: Subject demographics stored once, referenced by samples
- **Maintains Data Integrity**: Foreign key constraints prevent orphaned records
- **Enables Efficient Updates**: Change a treatment name once, affects all related samples

#### 2. **Scalability Considerations**

**For Hundreds of Projects:**
- `projects` table scales linearly with minimal overhead
- Indexed foreign keys in `samples` table ensure fast project-based queries
- Partitioning strategies could be implemented by project for very large datasets

**For Thousands of Samples:**
- Primary key on `sample` ensures O(log n) lookup time
- Composite indexes on frequently queried combinations (e.g., project + treatment + time)
- `cell_counts` as separate table prevents wide table issues and enables optimized storage

**For Various Analytics:**
- **Flexible Filtering**: Normalized structure supports complex WHERE clauses
- **Aggregation Efficiency**: Separate tables allow targeted queries without loading unnecessary data
- **Time Series Analysis**: `time_from_treatment_start` enables longitudinal studies
- **Statistical Analysis**: Clean data types support mathematical operations

#### 3. **Query Optimization Examples**

```sql
-- Efficient project-specific analysis
SELECT * FROM samples s 
JOIN cell_counts c ON s.sample = c.sample 
WHERE s.project = 'project_alpha'
INDEX: (project, sample)

-- Treatment comparison across timepoints
SELECT s.treatment_id, s.time_from_treatment_start, AVG(c.cd8_t_cell)
FROM samples s JOIN cell_counts c ON s.sample = c.sample
GROUP BY s.treatment_id, s.time_from_treatment_start
INDEX: (treatment_id, time_from_treatment_start)

-- Response prediction analysis
SELECT sub.condition, s.response, c.*
FROM samples s 
JOIN subjects sub ON s.subject = sub.subject
JOIN cell_counts c ON s.sample = c.sample
WHERE sub.condition = 'melanoma' AND s.sample_type = 'PBMC'
INDEX: (condition, sample_type, response)
```

#### 4. **Advanced Scalability Features**

**Horizontal Scaling:**
- Projects could be distributed across databases
- Read replicas for analytics workloads
- Separate OLTP/OLAP systems

**Performance Optimization:**
- Materialized views for common aggregations
- Columnar storage for analytical queries
- Data archiving strategies for old samples

**Extensibility:**
- Additional cell types: Add columns to `cell_counts`
- New metadata: Add columns to respective tables
- Complex relationships: Additional junction tables

## 🏗️ Code Structure & Design Philosophy

### Directory Structure
```
streamlit-csv-db-app/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── db.py               # Database operations and schema management
│   ├── analysis.py         # All analytical functions and visualizations
│   ├── schema.sql          # Database schema definition
│   └── generate_big_dataset.py  # Test data generator
└── README.md
```

### Design Principles

#### 1. **Separation of Concerns**
- **`app.py`**: User interface and application flow
- **`db.py`**: Data persistence and database operations
- **`analysis.py`**: Scientific analysis and visualizations
- **`schema.sql`**: Database structure definition

#### 2. **Modular Architecture**

**Database Layer (`db.py`)**
```python
# Clean, focused functions for specific operations
initialize_db()        # Schema setup
process_and_load_data() # Bulk data loading
load_data()            # Data retrieval with joins
add_sample()           # Individual record insertion
remove_sample()        # Record deletion
```

**Analysis Layer (`analysis.py`)**
```python
# Reusable analytical components
calculate_cell_frequencies()           # Core calculation
display_frequency_analysis()           # Bob's first question
analyze_treatment_response_prediction() # Biomarker identification
analyze_baseline_subset()              # Subset analysis
create_custom_filter_interface()       # Flexible exploration
```

**Presentation Layer (`app.py`)**
```python
# User-friendly interface with scientific workflow
File Upload → Database Loading → Analysis Tabs → Sample Management
```

#### 3. **Scientist-Friendly Design**

**No-Code Analysis:**
- All analyses update automatically when new data is added
- Point-and-click interface for complex statistical operations
- Instant visualizations and downloadable results

**Reproducible Research:**
- Consistent analysis methods across datasets
- Statistical rigor with p-values and effect sizes
- Exportable results for collaboration

**Scalable Workflow:**
- Tabbed interface organizes different research questions
- Filtering capabilities for subset analysis
- Custom analysis builder for ad-hoc exploration

#### 4. **Technical Robustness**

**Error Handling:**
- Database transaction management with rollback
- Input validation and user feedback
- Graceful handling of missing data

**Performance Optimization:**
- Efficient SQL queries with proper JOINs
- Lazy loading of visualizations
- Minimal data transfer between functions

**Maintainability:**
- Clear function documentation
- Consistent naming conventions
- Modular imports for easy testing

### Why This Design?

#### 1. **Bob's Requirements**
- **Interactive Exploration**: Streamlit provides immediate feedback
- **Statistical Rigor**: Scipy integration for proper hypothesis testing
- **Visualization**: Plotly creates publication-ready figures
- **No Programming Required**: Point-and-click interface

#### 2. **Yah D'yada's Needs**
- **Credible Results**: Statistical significance testing
- **Clear Presentation**: Professional visualizations
- **Exportable Data**: CSV downloads for further analysis

#### 3. **Future Extensibility**
- **New Analysis Types**: Add functions to `analysis.py`
- **Different Data Sources**: Extend `db.py` operations
- **Enhanced UI**: Modify `app.py` without affecting analysis logic

#### 4. **Enterprise Readiness**
- **Database Agnostic**: SQLite for development, easily switch to PostgreSQL/MySQL
- **API Ready**: Functions designed for potential REST API exposure
- **Multi-user Support**: Session state management for concurrent users

## 🔬 Scientific Validation

The application provides statistically rigorous analysis including:
- **T-tests** for group comparisons
- **Effect size calculations** (Cohen's d)
- **Multiple comparison corrections** (ready for implementation)
- **Confidence intervals** for all estimates
- **Data quality checks** and validation

This ensures that Bob's findings will meet peer-review standards and convince colleagues like Yah D'yada with solid statistical evidence.

## 🚀 Future Enhancements

The modular design supports easy addition of:
- Machine learning models for response prediction
- Time series analysis for treatment progression
- Multi-omics data integration
- Advanced statistical methods (survival analysis, mixed-effects models)
- Real-time data streaming capabilities
- Multi-center study management