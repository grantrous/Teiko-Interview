# Clinical Trial Data Management System

Hi Bob Loblaw! I hope this Python program helps you and Yah D'yada quickly analyze your clinical trial data and identify those treatment response biomarkers you've been looking for. I built this specifically to answer your three main questions about cell type frequencies, treatment response prediction, and baseline characteristics. Here's how you can get started right away and see your data come to life with interactive visualizations and statistical analysis.

## 🚀 Quick Start for Bob

### Get it Running in 5 Minutes

1. **Download the files** to your computer
2. **Open your terminal** and navigate to the folder
3. **Install the required packages:**
   ```bash
   pip install streamlit pandas plotly scipy numpy
   ```

   Or using requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```


4. **Start the program:**
   ```bash
   streamlit run src/app.py
   ```
5. **Open your browser** - it should automatically open to `http://localhost:8501`
6. **Upload your CSV** and click "Load Data into Database"
7. **Explore the analysis tabs** - each one answers one of your specific research questions!

That's it! Your data will be loaded and you can immediately start exploring the frequency analysis, response prediction, and baseline characteristics.

## 📄 What Your CSV File Should Look Like

Your CSV file needs these exact column headers (copy and paste them if needed):

```csv
sample,project,subject,age,sex,condition,treatment,sample_type,time_from_treatment_start,response,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
```

### Here's What Each Column Should Contain:

| Column | What to Put Here | Examples |
|--------|------------------|----------|
| `sample` | Unique ID for each sample | "SAMPLE_001", "MEL_T0_001" |
| `project` | Your study name | "MELANO_001", "IMMUNOTHERAPY_TRIAL" |
| `subject` | Patient ID | "PATIENT_001", "SUB_123" |
| `age` | Patient age | 45, 67, 28 |
| `sex` | M or F | "M", "F" |
| `condition` | Disease type | "melanoma", "healthy", "lung_cancer" |
| `treatment` | What treatment they got | "tr1", "tr2", "placebo" |
| `sample_type` | Type of sample | "PBMC", "tumor", "serum" |
| `time_from_treatment_start` | Days since treatment | 0, 7, 28, 84 |
| `response` | Did they respond? | "y", "n", or leave empty |
| `b_cell` | B cell count | 800, 1200, 500 |
| `cd8_t_cell` | CD8 T cell count | 2200, 1800, 3000 |
| `cd4_t_cell` | CD4 T cell count | 2800, 2400, 3500 |
| `nk_cell` | NK cell count | 1000, 800, 1500 |
| `monocyte` | Monocyte count | 1500, 1200, 2000 |

### Sample Row:
```csv
SAMPLE_001,MELANO_001,PATIENT_001,45,M,melanoma,tr1,PBMC,0,y,800,2200,2800,1000,1500
```

**Important:** Make sure your response column uses "y" for responders and "n" for non-responders - the program looks for these exact values to do the statistical comparisons for Yah D'yada.

## 🧪 Testing with Bigger Data

Want to test with more data? I included a data generator that creates 500+ realistic samples:
```bash
python generate_big_dataset.py
```
This creates `big-cell-counts.csv` with multiple projects, treatments, and realistic response rates.

## 🗃️ How the Database Works Behind the Scenes

I designed the database to handle your growing study efficiently. Here's the simple explanation:

### 1. Smart Data Organization
Instead of storing everything in one giant table, I split your data into logical pieces. Patient info (age, sex, condition) gets stored once per patient, not repeated for every sample. 

### 2. Easy to Scale Up
As your study grows to hundreds of projects and thousands of samples, the database stays fast. Each table has indexes on the columns you'll search most often (like project, treatment, condition). Think of it like having a really good filing system that doesn't get slower as you add more files.

### 3. Flexible for Analysis
The structure makes it easy to answer questions like "show me all melanoma patients who got tr1 treatment" or "compare baseline vs week-12 samples." The database can quickly find and combine the right pieces of information without having to scan through everything.

### 4. Future-Proof Design
If you need to add new cell types later, just add columns to the cell counts table. New patient characteristics? Add them to the subjects table. The structure grows with your research needs.

## 🏗️ Why I Built It This Way

### 1. Bob-Friendly Interface
You're a scientist, not a programmer. Everything you need is point-and-click. Upload your data once, and all the analyses update automatically as you add new samples. No code writing required.

### 2. Yah D'yada (And Your Reviewers) Will Be Convinced
I included proper statistical testing (t-tests, p-values, effect sizes) to provide solid evidence for your findings. The visualizations are publication-ready, and everything can be downloaded as CSV files for further analysis.

For comparing treatment responders vs non-responders, I use independent t-tests to determine if differences in cell population frequencies are statistically significant. Effect sizes are calculated using Cohen's d so you can quantify not just whether differences exist, but how meaningful they are clinically.

### 3. Handles Real Research Workflows
The program remembers your data between sessions (no re-uploading every time you restart), lets you add individual samples as they come in, and provides flexible filtering for any subset analysis you might need.

### 4. Built for Growing Studies
Started with 20 samples? Great. Now you have 500? No problem. The database structure and analysis functions scale up without slowing down or breaking.

## 🔬 What Each Analysis Tab Does

**Tab 1 - Cell Type Frequencies:** Answers your first question about relative frequencies. Gives you the exact table format you requested with sample, total_count, population, count, and percentage columns.

**Tab 2 - Treatment Response Prediction:** Compares tr1 responders vs non-responders in melanoma PBMC samples. Includes the boxplots and statistical tests you need to convince Yah D'yada.

**Tab 3 - Baseline Analysis:** Filters for those baseline melanoma PBMC samples and gives you the project/responder/gender breakdowns you wanted.

**Tab 4 - Custom Exploration:** Lets you slice and dice the data any way you want as your research questions evolve.

## 🎯 Pro Tips for Bob

1. **Data Persists:** Once you load data, it stays loaded even if you close the program. Use the "Clear Database" button when you want to start fresh.

2. **Add Samples Anytime:** Use the "Add Sample" tab to input new samples as they arrive from the lab.

3. **Download Everything:** Every analysis has a download button so you can save results for presentations or further analysis.

4. **Filter First:** Use the project and condition filters at the top to focus on specific subsets before running analyses.

5. **Check the Baseline Tab:** This is probably the most useful for understanding your tr1 treatment effects early in the study.

Hope this helps accelerate your research and gives you the evidence you need to backup your findings! 