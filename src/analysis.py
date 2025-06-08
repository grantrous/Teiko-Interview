import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats
import numpy as np


def analyze_baseline_subset(db_data):
    """Analyze baseline melanoma PBMC samples with tr1 treatment"""
    st.header("🔬 Baseline Treatment Effects Analysis")
    st.markdown("### Early Treatment Effects - Baseline Melanoma PBMC Samples (TR1)")
    st.markdown("*Exploring baseline characteristics before treatment effects emerge*")
    
    # Filter for baseline melanoma PBMC samples with tr1 treatment
    baseline_data = db_data[
        (db_data['condition'] == 'melanoma') & 
        (db_data['sample_type'] == 'PBMC') & 
        (db_data['treatment'] == 'tr1') &
        (db_data['time_from_treatment_start'] == 0)
    ].copy()
    
    if baseline_data.empty:
        st.warning("No baseline melanoma PBMC samples with tr1 treatment found in the dataset.")
        return
    
    # Overview metrics
    st.subheader("📊 Baseline Sample Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Baseline Samples", len(baseline_data))
    with col2:
        st.metric("Unique Subjects", baseline_data['subject'].nunique())
    with col3:
        st.metric("Projects", baseline_data['project'].nunique())
    with col4:
        avg_age = baseline_data['age'].mean() if baseline_data['age'].notna().any() else 0
        st.metric("Average Age", f"{avg_age:.1f}" if avg_age > 0 else "N/A")
    
    # Display the filtered dataset
    st.subheader("🔍 Filtered Baseline Dataset")
    st.dataframe(baseline_data, use_container_width=True)
    
    # Download button for baseline data
    csv_baseline = baseline_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Baseline Dataset",
        data=csv_baseline,
        file_name="baseline_melanoma_tr1_pbmc_samples.csv",
        mime="text/csv"
    )
    
    # Analysis 1: Samples per project
    st.subheader("📈 Samples per Project")
    project_counts = baseline_data['project'].value_counts().reset_index()
    project_counts.columns = ['Project', 'Sample Count']
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(project_counts, use_container_width=True)
    with col2:
        fig_project = px.bar(
            project_counts,
            x='Project',
            y='Sample Count',
            title='Baseline Samples Distribution by Project',
            color='Sample Count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_project, use_container_width=True)
    
    # Analysis 2: Response distribution by subject
    st.subheader("🎯 Treatment Response Distribution")
    
    # Get unique subjects and their responses (one response per subject)
    subject_responses = baseline_data.drop_duplicates(subset=['subject'])[['subject', 'response']].copy()
    
    # Filter out subjects without response data
    subject_responses = subject_responses[subject_responses['response'].isin(['y', 'n'])]
    
    if not subject_responses.empty:
        response_counts = subject_responses['response'].value_counts().reset_index()
        response_counts.columns = ['Response', 'Subject Count']
        response_counts['Response'] = response_counts['Response'].map({'y': 'Responders', 'n': 'Non-Responders'})
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(response_counts, use_container_width=True)
            
            # Calculate percentages
            total_subjects = response_counts['Subject Count'].sum()
            for _, row in response_counts.iterrows():
                percentage = (row['Subject Count'] / total_subjects) * 100
                st.write(f"**{row['Response']}**: {row['Subject Count']} subjects ({percentage:.1f}%)")
        
        with col2:
            fig_response = px.pie(
                response_counts,
                values='Subject Count',
                names='Response',
                title='Response Distribution Among Baseline Subjects',
                color_discrete_map={'Responders': '#2E8B57', 'Non-Responders': '#DC143C'}
            )
            st.plotly_chart(fig_response, use_container_width=True)
    else:
        st.info("No response data available for baseline subjects.")
    
    # Analysis 3: Gender distribution
    st.subheader("👥 Gender Distribution")
    
    # Get unique subjects and their gender (one gender per subject)
    subject_gender = baseline_data.drop_duplicates(subset=['subject'])[['subject', 'sex']].copy()
    
    if not subject_gender.empty and subject_gender['sex'].notna().any():
        gender_counts = subject_gender['sex'].value_counts().reset_index()
        gender_counts.columns = ['Sex', 'Subject Count']
        gender_counts['Sex'] = gender_counts['Sex'].map({'M': 'Male', 'F': 'Female'})
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(gender_counts, use_container_width=True)
            
            # Calculate percentages
            total_subjects = gender_counts['Subject Count'].sum()
            for _, row in gender_counts.iterrows():
                percentage = (row['Subject Count'] / total_subjects) * 100
                st.write(f"**{row['Sex']}**: {row['Subject Count']} subjects ({percentage:.1f}%)")
        
        with col2:
            fig_gender = px.bar(
                gender_counts,
                x='Sex',
                y='Subject Count',
                title='Gender Distribution Among Baseline Subjects',
                color='Sex',
                color_discrete_map={'Male': '#4A90E2', 'Female': '#E94B8C'}
            )
            st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No gender data available for baseline subjects.")
    
    # Analysis 4: Cross-tabulation analysis
    st.subheader("📋 Cross-Tabulation Analysis")
    
    # Get unique subjects with all relevant info
    subject_summary = baseline_data.drop_duplicates(subset=['subject'])[
        ['subject', 'project', 'response', 'sex', 'age']
    ].copy()
    
    # Response by Gender
    if not subject_summary.empty and subject_summary['response'].isin(['y', 'n']).any() and subject_summary['sex'].notna().any():
        st.write("**Response by Gender:**")
        response_gender_crosstab = pd.crosstab(
            subject_summary['sex'].map({'M': 'Male', 'F': 'Female'}),
            subject_summary['response'].map({'y': 'Responder', 'n': 'Non-Responder'}),
            margins=True
        )
        st.dataframe(response_gender_crosstab, use_container_width=True)
    
    # Response by Project
    if not subject_summary.empty and subject_summary['response'].isin(['y', 'n']).any():
        st.write("**Response by Project:**")
        response_project_crosstab = pd.crosstab(
            subject_summary['project'],
            subject_summary['response'].map({'y': 'Responder', 'n': 'Non-Responder'}),
            margins=True
        )
        st.dataframe(response_project_crosstab, use_container_width=True)
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    summary_stats = {
        'Metric': [
            'Total Baseline Samples',
            'Unique Subjects',
            'Projects Represented',
            'Samples per Subject (avg)',
            'Age Range',
            'Response Rate (%)'
        ],
        'Value': []
    }
    
    # Calculate values
    summary_stats['Value'].append(len(baseline_data))
    summary_stats['Value'].append(baseline_data['subject'].nunique())
    summary_stats['Value'].append(baseline_data['project'].nunique())
    
    samples_per_subject = len(baseline_data) / baseline_data['subject'].nunique()
    summary_stats['Value'].append(f"{samples_per_subject:.1f}")
    
    if baseline_data['age'].notna().any():
        age_range = f"{baseline_data['age'].min():.0f} - {baseline_data['age'].max():.0f}"
    else:
        age_range = "N/A"
    summary_stats['Value'].append(age_range)
    
    if not subject_responses.empty:
        response_rate = (subject_responses['response'] == 'y').sum() / len(subject_responses) * 100
        summary_stats['Value'].append(f"{response_rate:.1f}%")
    else:
        summary_stats['Value'].append("N/A")
    
    summary_df = pd.DataFrame(summary_stats)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Key findings
    st.subheader("🔍 Key Findings")
    
    findings = []
    findings.append(f"✓ Identified **{len(baseline_data)}** baseline melanoma PBMC samples from **{baseline_data['subject'].nunique()}** subjects receiving tr1 treatment")
    
    if len(project_counts) > 0:
        largest_project = project_counts.iloc[0]
        findings.append(f"✓ **{largest_project['Project']}** has the most samples ({largest_project['Sample Count']} samples)")
    
    if not subject_responses.empty:
        responder_count = (subject_responses['response'] == 'y').sum()
        non_responder_count = (subject_responses['response'] == 'n').sum()
        findings.append(f"✓ **{responder_count}** responders and **{non_responder_count}** non-responders identified")
    
    if not subject_gender.empty and subject_gender['sex'].notna().any():
        male_count = (subject_gender['sex'] == 'M').sum()
        female_count = (subject_gender['sex'] == 'F').sum()
        findings.append(f"✓ Gender distribution: **{male_count}** males and **{female_count}** females")
    
    for finding in findings:
        st.write(finding)
    
    return baseline_data

def create_custom_filter_interface(db_data):
    """Create a flexible filtering interface for Bob to explore any subset"""
    st.header("🔧 Custom Data Filtering & Analysis")
    st.markdown("### Flexible Data Exploration Tool")
    st.markdown("*Filter the data using any combination of criteria and get instant analysis*")
    
    if db_data.empty:
        st.warning("No data available for filtering.")
        return
    
    # Filter interface
    with st.expander("🎛️ Filter Controls", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Condition filter
            conditions = ['All'] + sorted(db_data['condition'].dropna().unique().tolist())
            selected_conditions = st.multiselect("Condition(s):", conditions, default=['All'])
            
            # Treatment filter
            treatments = ['All'] + sorted(db_data['treatment'].dropna().unique().tolist())
            selected_treatments = st.multiselect("Treatment(s):", treatments, default=['All'])
        
        with col2:
            # Sample type filter
            sample_types = ['All'] + sorted(db_data['sample_type'].dropna().unique().tolist())
            selected_sample_types = st.multiselect("Sample Type(s):", sample_types, default=['All'])
            
            # Time point filter
            time_points = sorted(db_data['time_from_treatment_start'].dropna().unique().tolist())
            if time_points:
                selected_times = st.multiselect("Time Points:", time_points, default=time_points)
            else:
                selected_times = []
        
        with col3:
            # Response filter
            responses = ['All'] + sorted(db_data['response'].dropna().unique().tolist())
            selected_responses = st.multiselect("Response(s):", responses, default=['All'])
            
            # Project filter
            projects = ['All'] + sorted(db_data['project'].dropna().unique().tolist())
            selected_projects = st.multiselect("Project(s):", projects, default=['All'])
    
    # Apply filters
    filtered_data = db_data.copy()
    
    if 'All' not in selected_conditions:
        filtered_data = filtered_data[filtered_data['condition'].isin(selected_conditions)]
    
    if 'All' not in selected_treatments:
        filtered_data = filtered_data[filtered_data['treatment'].isin(selected_treatments)]
    
    if 'All' not in selected_sample_types:
        filtered_data = filtered_data[filtered_data['sample_type'].isin(selected_sample_types)]
    
    if selected_times:
        filtered_data = filtered_data[filtered_data['time_from_treatment_start'].isin(selected_times)]
    
    if 'All' not in selected_responses:
        filtered_data = filtered_data[filtered_data['response'].isin(selected_responses)]
    
    if 'All' not in selected_projects:
        filtered_data = filtered_data[filtered_data['project'].isin(selected_projects)]
    
    # Display results
    if filtered_data.empty:
        st.warning("No data matches the selected filters.")
        return
    
    st.success(f"Found **{len(filtered_data)}** samples matching your criteria")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Samples", len(filtered_data))
    with col2:
        st.metric("Subjects", filtered_data['subject'].nunique())
    with col3:
        st.metric("Projects", filtered_data['project'].nunique())
    with col4:
        st.metric("Treatments", filtered_data['treatment'].nunique())
    
    # Display filtered data
    st.subheader("📋 Filtered Dataset")
    st.dataframe(filtered_data, use_container_width=True)
    
    # Download button
    csv_filtered = filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv_filtered,
        file_name="custom_filtered_data.csv",
        mime="text/csv"
    )
    
    # Auto-generate summary analysis
    if len(filtered_data) > 0:
        st.subheader("📊 Automated Analysis")
        
        # Group by analysis
        analysis_tabs = st.tabs(["By Project", "By Treatment", "By Response", "By Demographics"])
        
        with analysis_tabs[0]:
            if filtered_data['project'].nunique() > 1:
                project_summary = filtered_data.groupby('project').agg({
                    'sample': 'count',
                    'subject': 'nunique',
                    'age': 'mean'
                }).round(2)
                project_summary.columns = ['Sample Count', 'Subject Count', 'Avg Age']
                st.dataframe(project_summary, use_container_width=True)
        
        with analysis_tabs[1]:
            if filtered_data['treatment'].nunique() > 1:
                treatment_summary = filtered_data.groupby('treatment').agg({
                    'sample': 'count',
                    'subject': 'nunique',
                    'age': 'mean'
                }).round(2)
                treatment_summary.columns = ['Sample Count', 'Subject Count', 'Avg Age']
                st.dataframe(treatment_summary, use_container_width=True)
        
        with analysis_tabs[2]:
            response_data = filtered_data[filtered_data['response'].isin(['y', 'n'])]
            if not response_data.empty:
                response_summary = response_data.groupby('response').agg({
                    'sample': 'count',
                    'subject': 'nunique'
                }).round(2)
                response_summary.columns = ['Sample Count', 'Subject Count']
                response_summary.index = response_summary.index.map({'y': 'Responders', 'n': 'Non-Responders'})
                st.dataframe(response_summary, use_container_width=True)
        
        with analysis_tabs[3]:
            demo_data = filtered_data.drop_duplicates(subset=['subject'])
            if not demo_data.empty and demo_data['sex'].notna().any():
                gender_summary = demo_data.groupby('sex').agg({
                    'subject': 'count',
                    'age': 'mean'
                }).round(2)
                gender_summary.columns = ['Subject Count', 'Avg Age']
                gender_summary.index = gender_summary.index.map({'M': 'Male', 'F': 'Female'})
                st.dataframe(gender_summary, use_container_width=True)
    
    return filtered_data

# ... rest of existing functions (display_frequency_analysis, analyze_treatment_response_prediction, etc.) ...
def calculate_cell_frequencies(db_data):
    """Calculate relative frequencies of each cell type for each sample"""
    if db_data.empty:
        return pd.DataFrame()
    
    # Cell type columns
    cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    results = []
    
    for _, row in db_data.iterrows():
        sample_id = row['sample']
        
        # Calculate total count for this sample
        total_count = sum(row[cell_type] for cell_type in cell_types if pd.notna(row[cell_type]))
        
        # Calculate frequency for each cell type
        for cell_type in cell_types:
            count = row[cell_type] if pd.notna(row[cell_type]) else 0
            percentage = (count / total_count * 100) if total_count > 0 else 0
            
            results.append({
                'sample': sample_id,
                'total_count': total_count,
                'population': cell_type,
                'count': count,
                'percentage': round(percentage, 2)
            })
    
    return pd.DataFrame(results)

def create_frequency_visualizations(frequency_data):
    """Create visualization charts for cell frequency data"""
    visualizations = {}
    
    # Stacked bar chart showing cell type composition per sample
    visualizations['stacked_bar'] = px.bar(
        frequency_data,
        x='sample',
        y='percentage',
        color='population',
        title='Cell Type Composition by Sample (% of Total)',
        labels={'percentage': 'Percentage (%)', 'sample': 'Sample ID'},
        height=500
    )
    visualizations['stacked_bar'].update_layout(xaxis_tickangle=-45)
    
    # Heatmap showing percentage distribution
    pivot_data = frequency_data.pivot(index='sample', columns='population', values='percentage')
    visualizations['heatmap'] = px.imshow(
        pivot_data,
        title='Cell Type Percentage Heatmap',
        labels=dict(x="Cell Population", y="Sample ID", color="Percentage (%)"),
        aspect="auto",
        color_continuous_scale="Blues"
    )
    
    # Box plot showing distribution of each cell type across samples
    visualizations['box_plot'] = px.box(
        frequency_data,
        x='population',
        y='percentage',
        title='Distribution of Cell Type Percentages Across Samples',
        labels={'percentage': 'Percentage (%)', 'population': 'Cell Population'},
        height=500
    )
    visualizations['box_plot'].update_layout(xaxis_tickangle=-45)
    
    return visualizations

def calculate_summary_statistics(frequency_data):
    """Calculate summary statistics for cell type frequencies"""
    if frequency_data.empty:
        return pd.DataFrame()
    
    summary_stats = frequency_data.groupby('population').agg({
        'percentage': ['mean', 'std', 'min', 'max', 'median']
    }).round(2)
    summary_stats.columns = ['Mean %', 'Std Dev %', 'Min %', 'Max %', 'Median %']
    
    return summary_stats

def display_frequency_analysis(filtered_data):
    """Display the complete cell frequency analysis section"""
    st.header("📈 Data Analysis")
    st.markdown("### Cell Type Frequency Analysis")
    st.markdown("*Answering Bob's question: 'What is the frequency of each cell type in each sample?'*")
    
    # Calculate cell frequencies
    frequency_data = calculate_cell_frequencies(filtered_data)
    
    if not frequency_data.empty:
        # Display summary table
        st.subheader("Cell Type Frequency Summary")
        st.dataframe(
            frequency_data,
            use_container_width=True,
            column_config={
                "sample": "Sample ID",
                "total_count": st.column_config.NumberColumn(
                    "Total Count",
                    format="%d"
                ),
                "population": "Cell Population",
                "count": st.column_config.NumberColumn(
                    "Count",
                    format="%d"
                ),
                "percentage": st.column_config.NumberColumn(
                    "Percentage (%)",
                    format="%.2f%%"
                )
            }
        )
        
        # Download button for frequency data
        csv = frequency_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Cell Frequency Data as CSV",
            data=csv,
            file_name="cell_frequency_analysis.csv",
            mime="text/csv"
        )
        
        # Visualizations
        st.subheader("Cell Type Distribution Visualizations")
        
        # Create visualizations
        viz = create_frequency_visualizations(frequency_data)
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Stacked Bar Chart", "Heatmap", "Box Plot"])
        
        with viz_tab1:
            st.plotly_chart(viz['stacked_bar'], use_container_width=True)
        
        with viz_tab2:
            st.plotly_chart(viz['heatmap'], use_container_width=True)
        
        with viz_tab3:
            st.plotly_chart(viz['box_plot'], use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        summary_stats = calculate_summary_statistics(frequency_data)
        st.dataframe(summary_stats, use_container_width=True)
        
        return frequency_data
    else:
        st.warning("No frequency data available for the selected filters.")
        return pd.DataFrame()

def analyze_treatment_response_prediction(db_data):
    """Analyze differences in cell populations between responders and non-responders for tr1 treatment"""
    st.header("🎯 Treatment Response Prediction Analysis")
    st.markdown("### Melanoma Patients - TR1 Treatment Response Patterns")
    st.markdown("*Identifying biomarkers to predict treatment response for tr1 in melanoma patients*")
    
    # Filter for melanoma patients with tr1 treatment and PBMC samples
    filtered_data = db_data[
        (db_data['condition'] == 'melanoma') & 
        (db_data['treatment'] == 'tr1') & 
        (db_data['sample_type'] == 'PBMC') &
        (db_data['response'].isin(['y', 'n']))
    ].copy()
    
    if filtered_data.empty:
        st.warning("No data found for melanoma patients with tr1 treatment and PBMC samples with response data.")
        return
    
    # Show filtered dataset info
    responder_count = len(filtered_data[filtered_data['response'] == 'y'])
    non_responder_count = len(filtered_data[filtered_data['response'] == 'n'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Samples", len(filtered_data))
    with col2:
        st.metric("Responders", responder_count)
    with col3:
        st.metric("Non-Responders", non_responder_count)
    
    if responder_count == 0 or non_responder_count == 0:
        st.warning("Need both responders and non-responders for comparison analysis.")
        return
    
    # Calculate cell frequencies
    frequency_data = calculate_cell_frequencies(filtered_data)
    
    # Add response information
    response_info = filtered_data[['sample', 'response']].drop_duplicates()
    frequency_with_response = frequency_data.merge(response_info, on='sample')
    
    # Create response labels
    frequency_with_response['response_label'] = frequency_with_response['response'].map({
        'y': 'Responder',
        'n': 'Non-Responder'
    })
    
    # Statistical analysis
    st.subheader("📊 Statistical Analysis Results")
    
    cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    statistical_results = []
    
    for cell_type in cell_types:
        responder_data = frequency_with_response[
            (frequency_with_response['population'] == cell_type) & 
            (frequency_with_response['response'] == 'y')
        ]['percentage']
        
        non_responder_data = frequency_with_response[
            (frequency_with_response['population'] == cell_type) & 
            (frequency_with_response['response'] == 'n')
        ]['percentage']
        
        if len(responder_data) > 0 and len(non_responder_data) > 0:
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(responder_data, non_responder_data)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(((len(responder_data) - 1) * responder_data.var() + 
                                 (len(non_responder_data) - 1) * non_responder_data.var()) / 
                                (len(responder_data) + len(non_responder_data) - 2))
            cohens_d = (responder_data.mean() - non_responder_data.mean()) / pooled_std if pooled_std > 0 else 0
            
            # Determine significance
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
            
            statistical_results.append({
                'Cell_Population': cell_type.replace('_', ' ').title(),
                'Responder_Mean_%': round(responder_data.mean(), 2),
                'Responder_SD_%': round(responder_data.std(), 2),
                'Non_Responder_Mean_%': round(non_responder_data.mean(), 2),
                'Non_Responder_SD_%': round(non_responder_data.std(), 2),
                'Mean_Difference_%': round(responder_data.mean() - non_responder_data.mean(), 2),
                'T_Statistic': round(t_stat, 3),
                'P_Value': f"{p_value:.4f}" if p_value >= 0.0001 else "<0.0001",
                'Effect_Size_Cohens_d': round(cohens_d, 3),
                'Significance': significance
            })
    
    # Display statistical results table
    stats_df = pd.DataFrame(statistical_results)
    st.dataframe(
        stats_df,
        use_container_width=True,
        column_config={
            "Cell_Population": "Cell Population",
            "Responder_Mean_%": st.column_config.NumberColumn("Responder Mean (%)", format="%.2f"),
            "Responder_SD_%": st.column_config.NumberColumn("Responder SD (%)", format="%.2f"),
            "Non_Responder_Mean_%": st.column_config.NumberColumn("Non-Responder Mean (%)", format="%.2f"),
            "Non_Responder_SD_%": st.column_config.NumberColumn("Non-Responder SD (%)", format="%.2f"),
            "Mean_Difference_%": st.column_config.NumberColumn("Mean Difference (%)", format="%.2f"),
            "T_Statistic": st.column_config.NumberColumn("T-Statistic", format="%.3f"),
            "P_Value": "P-Value",
            "Effect_Size_Cohens_d": st.column_config.NumberColumn("Effect Size (Cohen's d)", format="%.3f"),
            "Significance": "Significance"
        }
    )
    
    # Significance legend
    st.markdown("""
    **Significance levels:** 
    - *** p < 0.001 (highly significant)
    - ** p < 0.01 (very significant) 
    - * p < 0.05 (significant)
    - ns = not significant
    
    **Effect size interpretation (Cohen's d):**
    - Small: 0.2, Medium: 0.5, Large: 0.8
    """)
    
    # Box plot visualization
    st.subheader("📈 Response Comparison Visualization")
    
    fig = px.box(
        frequency_with_response,
        x='population',
        y='percentage',
        color='response_label',
        title='Cell Population Frequencies: Responders vs Non-Responders (TR1 Treatment)',
        labels={
            'percentage': 'Percentage (%)',
            'population': 'Cell Population',
            'response_label': 'Response Group'
        },
        height=600,
        color_discrete_map={
            'Responder': '#2E8B57',
            'Non-Responder': '#DC143C'
        }
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        boxmode='group'
    )
    
    # Add significance annotations
    y_max = frequency_with_response['percentage'].max()
    for i, result in enumerate(statistical_results):
        if result['Significance'] != 'ns':
            fig.add_annotation(
                x=i,
                y=y_max * 1.1,
                text=result['Significance'],
                showarrow=False,
                font=dict(size=16, color='red')
            )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary findings
    st.subheader("🔍 Key Findings for Yah D'yada")
    
    # Identify significant differences
    significant_pops = [result for result in statistical_results if result['Significance'] != 'ns']
    
    if significant_pops:
        st.success(f"**Significant biomarkers identified:** {len(significant_pops)} cell population(s) show statistically significant differences between responders and non-responders.")
        
        for pop in significant_pops:
            direction = "higher" if pop['Mean_Difference_%'] > 0 else "lower"
            st.write(f"- **{pop['Cell_Population']}**: Responders have {direction} frequencies ({pop['Mean_Difference_%']}% difference, p={pop['P_Value']})")
    else:
        st.info("No statistically significant differences found between responders and non-responders in this dataset.")
    
    # Download statistical results
    csv_stats = stats_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Statistical Analysis Results",
        data=csv_stats,
        file_name="tr1_response_biomarker_analysis.csv",
        mime="text/csv"
    )
    
    return frequency_with_response, stats_df

def compare_treatments(db_data):
    """Compare cell frequencies between different treatments"""
    if db_data.empty:
        return
    
    st.subheader("Treatment Comparison Analysis")
    
    frequency_data = calculate_cell_frequencies(db_data)
    
    if not frequency_data.empty:
        # Add treatment information to frequency data
        treatment_info = db_data[['sample', 'treatment']].drop_duplicates()
        frequency_with_treatment = frequency_data.merge(treatment_info, on='sample')
        
        # Create comparison visualization
        fig = px.box(
            frequency_with_treatment,
            x='treatment',
            y='percentage',
            color='population',
            title='Cell Type Percentage Distribution by Treatment',
            labels={'percentage': 'Percentage (%)', 'treatment': 'Treatment'},
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical comparison table
        treatment_stats = frequency_with_treatment.groupby(['treatment', 'population']).agg({
            'percentage': ['mean', 'std', 'count']
        }).round(2)
        treatment_stats.columns = ['Mean %', 'Std Dev %', 'Sample Count']
        st.dataframe(treatment_stats, use_container_width=True)

def compare_conditions(db_data):
    """Compare cell frequencies between different conditions"""
    if db_data.empty:
        return
    
    st.subheader("Condition Comparison Analysis")
    
    frequency_data = calculate_cell_frequencies(db_data)
    
    if not frequency_data.empty:
        # Add condition information to frequency data
        condition_info = db_data[['sample', 'condition']].drop_duplicates()
        frequency_with_condition = frequency_data.merge(condition_info, on='sample')
        
        # Create comparison visualization
        fig = px.violin(
            frequency_with_condition,
            x='condition',
            y='percentage',
            color='population',
            title='Cell Type Percentage Distribution by Condition',
            labels={'percentage': 'Percentage (%)', 'condition': 'Condition'},
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical comparison table
        condition_stats = frequency_with_condition.groupby(['condition', 'population']).agg({
            'percentage': ['mean', 'std', 'count']
        }).round(2)
        condition_stats.columns = ['Mean %', 'Std Dev %', 'Sample Count']
        st.dataframe(condition_stats, use_container_width=True)