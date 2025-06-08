import streamlit as st
import pandas as pd
from db import initialize_db, load_data, process_and_load_data, remove_sample, add_sample
from analysis import display_frequency_analysis, compare_treatments, compare_conditions
import os

def main():
    st.title("CSV Database App")
    st.markdown("### Clinical Trial Data Management System")
    
    # Initialize session state
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    DB_NAME = 'samples.db'

    # Initialize database on startup
    if not os.path.exists(DB_NAME):
        initialize_db(DB_NAME, 'src/schema.sql')

    # File upload section
    st.header("📁 Data Loading")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the CSV file
        data = pd.read_csv(uploaded_file)
        st.write("**Data Preview:**")
        st.dataframe(data.head())
        st.write(f"Total rows: {len(data)}")
        
        # Load data button
        if st.button("Load Data into Database", type="primary"):
            with st.spinner('Loading data into database...'):
                if process_and_load_data(DB_NAME, data):
                    st.session_state.data_loaded = True
                    st.success("✅ Data loaded successfully!")
                    st.rerun()
                else:
                    st.error("❌ Error loading data into database.")
    
    # Data viewing section
    st.header("📊 Database Contents")
    
    try:
        db_data = load_data(DB_NAME)
        
        if not db_data.empty:
            st.success(f"Found {len(db_data)} samples in database")
            
            # Display data with filters
            col1, col2 = st.columns(2)
            
            with col1:
                projects = ['All'] + sorted(db_data['project'].unique().tolist())
                selected_project = st.selectbox("Filter by Project:", projects)
            
            with col2:
                conditions = ['All'] + sorted(db_data['condition'].unique().tolist())
                selected_condition = st.selectbox("Filter by Condition:", conditions)
            
            # Apply filters
            filtered_data = db_data.copy()
            if selected_project != 'All':
                filtered_data = filtered_data[filtered_data['project'] == selected_project]
            if selected_condition != 'All':
                filtered_data = filtered_data[filtered_data['condition'] == selected_condition]
            
            st.dataframe(filtered_data, use_container_width=True)
            
            # Data Analysis Section - moved to analysis.py
            display_frequency_analysis(filtered_data)
            
            # Additional Analysis Sections
            if len(db_data['treatment'].unique()) > 1:
                compare_treatments(filtered_data)
            
            if len(db_data['condition'].unique()) > 1:
                compare_conditions(filtered_data)
            
            # Sample management section
            st.header("🔧 Sample Management")
            
            tab1, tab2 = st.tabs(["Remove Sample", "Add Sample"])
            
            with tab1:
                if not filtered_data.empty:
                    sample_to_remove = st.selectbox(
                        "Select Sample to Remove:", 
                        options=filtered_data['sample'].tolist()
                    )
                    
                    if st.button("Remove Sample", type="secondary"):
                        if remove_sample(DB_NAME, 'samples', sample_to_remove):
                            st.success(f"✅ Sample {sample_to_remove} removed successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Error removing sample.")
                else:
                    st.info("No samples available for removal with current filters.")
            
            with tab2:
                st.write("**Add New Sample:**")
                
                with st.form("add_sample_form"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_sample = st.text_input("Sample ID*")
                        new_project = st.text_input("Project*")
                        new_subject = st.text_input("Subject ID*")
                        new_condition = st.text_input("Condition*")
                    
                    with col2:
                        new_age = st.number_input("Age", min_value=0, max_value=120, value=50)
                        new_sex = st.selectbox("Sex", ["M", "F"])
                        new_treatment = st.text_input("Treatment*")
                        new_response = st.selectbox("Response", ["y", "n", ""])
                    
                    with col3:
                        new_sample_type = st.text_input("Sample Type", value="PBMC")
                        new_time = st.number_input("Time from Treatment Start", min_value=0, value=0)
                        new_b_cell = st.number_input("B Cell Count", min_value=0, value=0)
                        new_cd8 = st.number_input("CD8 T Cell Count", min_value=0, value=0)
                    
                    col4, col5 = st.columns(2)
                    with col4:
                        new_cd4 = st.number_input("CD4 T Cell Count", min_value=0, value=0)
                        new_nk = st.number_input("NK Cell Count", min_value=0, value=0)
                    with col5:
                        new_monocyte = st.number_input("Monocyte Count", min_value=0, value=0)
                    
                    submitted = st.form_submit_button("Add Sample", type="primary")
                    
                    if submitted:
                        if new_sample and new_project and new_subject and new_condition and new_treatment:
                            sample_data = {
                                'sample': new_sample,
                                'project': new_project,
                                'subject': new_subject,
                                'condition': new_condition,
                                'age': new_age,
                                'sex': new_sex,
                                'treatment': new_treatment,
                                'response': new_response,
                                'sample_type': new_sample_type,
                                'time_from_treatment_start': new_time,
                                'b_cell': new_b_cell,
                                'cd8_t_cell': new_cd8,
                                'cd4_t_cell': new_cd4,
                                'nk_cell': new_nk,
                                'monocyte': new_monocyte
                            }
                            
                            if add_sample(DB_NAME, sample_data):
                                st.success(f"✅ Sample {new_sample} added successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Error adding sample. Check if sample ID already exists.")
                        else:
                            st.error("Please fill in all required fields (marked with *).")
            
        else:
            st.info("No data in database. Upload a CSV file and click 'Load Data' to get started.")
            
    except Exception as e:
        st.error(f"Error accessing database: {str(e)}")

if __name__ == "__main__":
    main()