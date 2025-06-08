import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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