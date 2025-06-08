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

### Running the Analysis

1. **Load Data**: Upload the `cell-count.csv` file using the file uploader
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
│   └── schema.sql          # Database schema definition
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