import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_big_cell_counts_dataset(n_samples=500):
    """Generate a realistic fake dataset with multiple projects, conditions, and treatments"""
    
    # Define realistic parameters
    projects = ['MELANO_001', 'MELANO_002', 'IMMUNO_BOOST', 'ONCOLOGY_PRIME', 'BIOMARKER_STUDY']
    conditions = ['melanoma', 'healthy', 'lung_cancer', 'breast_cancer']
    treatments = ['tr1', 'tr2', 'tr3', 'placebo', 'standard_care']
    sample_types = ['PBMC', 'tumor', 'serum']
    sexes = ['M', 'F']
    responses = ['y', 'n', '']  # '' for cases where response isn't applicable or unknown
    
    # Time points commonly used in clinical trials
    time_points = [0, 7, 14, 28, 56, 84, 168]  # baseline, week 1, 2, 4, 8, 12, 24
    
    data = []
    
    # Generate realistic subject pools for each project
    subjects_per_project = {
        'MELANO_001': 60,
        'MELANO_002': 45,
        'IMMUNO_BOOST': 80,
        'ONCOLOGY_PRIME': 70,
        'BIOMARKER_STUDY': 55
    }
    
    sample_id_counter = 1
    
    for project in projects:
        n_subjects = subjects_per_project[project]
        
        # Generate subjects for this project
        for subject_num in range(1, n_subjects + 1):
            subject_id = f"{project}_S{subject_num:03d}"
            
            # Assign demographic characteristics
            age = np.random.normal(55, 15)  # Mean age 55, std 15
            age = max(18, min(85, int(age)))  # Clamp between 18-85
            
            sex = random.choice(sexes)
            
            # Assign condition based on project (with some overlap for realism)
            if 'MELANO' in project:
                condition = 'melanoma' if random.random() < 0.8 else random.choice(['healthy', 'lung_cancer'])
            elif 'IMMUNO' in project:
                condition = random.choice(['melanoma', 'lung_cancer', 'breast_cancer'])
            elif 'ONCOLOGY' in project:
                condition = random.choice(['lung_cancer', 'breast_cancer', 'melanoma'])
            else:  # BIOMARKER_STUDY
                condition = random.choice(conditions)
            
            # Assign treatment based on condition and project
            if condition == 'healthy':
                treatment = random.choice(['placebo', 'standard_care'])
            else:
                treatment = random.choice(treatments)
            
            # Determine response (only for treatment conditions)
            if condition != 'healthy' and treatment not in ['placebo', 'standard_care']:
                # Response rates vary by treatment and condition
                if treatment == 'tr1' and condition == 'melanoma':
                    response_prob = 0.35  # 35% response rate for tr1 in melanoma
                elif treatment == 'tr1':
                    response_prob = 0.25
                elif treatment == 'tr2':
                    response_prob = 0.20
                elif treatment == 'tr3':
                    response_prob = 0.15
                else:
                    response_prob = 0.10
                
                response = 'y' if random.random() < response_prob else 'n'
            else:
                response = ''  # No response data for healthy subjects or controls
            
            # Generate samples for this subject across different time points
            n_timepoints = random.choice([1, 2, 3, 4])  # Variable number of timepoints per subject
            selected_timepoints = sorted(random.sample(time_points, n_timepoints))
            
            # Ensure baseline (time=0) is often included
            if 0 not in selected_timepoints and random.random() < 0.7:
                selected_timepoints = [0] + selected_timepoints[:-1]
                selected_timepoints.sort()
            
            for time_point in selected_timepoints:
                # Sample type varies by time point and condition
                if condition == 'healthy':
                    sample_type = 'PBMC'
                elif time_point == 0:
                    sample_type = random.choice(['PBMC', 'tumor']) if condition != 'healthy' else 'PBMC'
                else:
                    sample_type = random.choice(['PBMC', 'serum'])
                
                sample_id = f"SAMPLE_{sample_id_counter:05d}"
                sample_id_counter += 1
                
                # Generate realistic cell counts
                # Base counts vary by condition and treatment
                if condition == 'melanoma' and treatment == 'tr1' and response == 'y':
                    # Responders might have different immune profiles
                    base_cd8 = np.random.normal(2800, 600)
                    base_cd4 = np.random.normal(3200, 700)
                    base_b = np.random.normal(800, 200)
                    base_nk = np.random.normal(1200, 300)
                    base_mono = np.random.normal(1800, 400)
                elif condition == 'melanoma':
                    # General melanoma population
                    base_cd8 = np.random.normal(2200, 500)
                    base_cd4 = np.random.normal(2800, 600)
                    base_b = np.random.normal(600, 150)
                    base_nk = np.random.normal(1000, 250)
                    base_mono = np.random.normal(1500, 350)
                elif condition == 'healthy':
                    # Healthy controls
                    base_cd8 = np.random.normal(1800, 400)
                    base_cd4 = np.random.normal(2500, 500)
                    base_b = np.random.normal(700, 180)
                    base_nk = np.random.normal(800, 200)
                    base_mono = np.random.normal(1200, 300)
                else:
                    # Other cancer types
                    base_cd8 = np.random.normal(2000, 450)
                    base_cd4 = np.random.normal(2600, 550)
                    base_b = np.random.normal(650, 160)
                    base_nk = np.random.normal(900, 220)
                    base_mono = np.random.normal(1400, 320)
                
                # Add time-dependent effects
                time_factor = 1.0
                if time_point > 0 and treatment in ['tr1', 'tr2', 'tr3']:
                    if response == 'y':
                        # Responders show treatment effects over time
                        time_factor = 1.0 + (time_point / 168) * random.uniform(0.1, 0.4)
                    else:
                        # Non-responders show minimal or negative effects
                        time_factor = 1.0 + (time_point / 168) * random.uniform(-0.2, 0.1)
                
                # Apply time factor and ensure positive counts
                cd8_count = max(50, int(base_cd8 * time_factor))
                cd4_count = max(100, int(base_cd4 * time_factor))
                b_count = max(20, int(base_b * time_factor))
                nk_count = max(30, int(base_nk * time_factor))
                mono_count = max(40, int(base_mono * time_factor))
                
                # Add some sample-type specific variations
                if sample_type == 'tumor':
                    # Tumor samples might have different immune infiltration
                    cd8_count = int(cd8_count * random.uniform(0.3, 1.5))
                    cd4_count = int(cd4_count * random.uniform(0.4, 1.2))
                elif sample_type == 'serum':
                    # Serum samples might have lower overall counts
                    cd8_count = int(cd8_count * random.uniform(0.1, 0.3))
                    cd4_count = int(cd4_count * random.uniform(0.1, 0.3))
                    b_count = int(b_count * random.uniform(0.1, 0.3))
                    nk_count = int(nk_count * random.uniform(0.1, 0.3))
                    mono_count = int(mono_count * random.uniform(0.1, 0.3))
                
                data.append({
                    'sample': sample_id,
                    'project': project,
                    'subject': subject_id,
                    'age': age,
                    'sex': sex,
                    'condition': condition,
                    'treatment': treatment,
                    'sample_type': sample_type,
                    'time_from_treatment_start': time_point,
                    'response': response,
                    'b_cell': b_count,
                    'cd8_t_cell': cd8_count,
                    'cd4_t_cell': cd4_count,
                    'nk_cell': nk_count,
                    'monocyte': mono_count
                })
    
    # Convert to DataFrame and shuffle
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle rows
    
    # Trim to requested size if needed
    if len(df) > n_samples:
        df = df.head(n_samples)
    
    return df

# Generate the dataset
print("Generating big cell counts dataset...")
big_dataset = generate_big_cell_counts_dataset(n_samples=500)

# Display summary statistics
print(f"\nDataset Summary:")
print(f"Total samples: {len(big_dataset)}")
print(f"Unique subjects: {big_dataset['subject'].nunique()}")
print(f"Projects: {big_dataset['project'].nunique()}")
print(f"Conditions: {', '.join(big_dataset['condition'].unique())}")
print(f"Treatments: {', '.join(big_dataset['treatment'].unique())}")
print(f"Sample types: {', '.join(big_dataset['sample_type'].unique())}")
print(f"Time points: {sorted(big_dataset['time_from_treatment_start'].unique())}")

# Show breakdown by key categories
print(f"\nBreakdown by project:")
print(big_dataset['project'].value_counts())

print(f"\nBreakdown by condition:")
print(big_dataset['condition'].value_counts())

print(f"\nBreakdown by treatment:")
print(big_dataset['treatment'].value_counts())

print(f"\nResponse rates (excluding empty responses):")
response_data = big_dataset[big_dataset['response'].isin(['y', 'n'])]
if len(response_data) > 0:
    response_rate = (response_data['response'] == 'y').sum() / len(response_data) * 100
    print(f"Overall response rate: {response_rate:.1f}%")
    
    # Response by treatment
    print("\nResponse rates by treatment:")
    for treatment in response_data['treatment'].unique():
        treat_data = response_data[response_data['treatment'] == treatment]
        if len(treat_data) > 0:
            treat_response_rate = (treat_data['response'] == 'y').sum() / len(treat_data) * 100
            print(f"  {treatment}: {treat_response_rate:.1f}% ({(treat_data['response'] == 'y').sum()}/{len(treat_data)})")

# Save to CSV
output_file = 'big-cell-counts.csv'
big_dataset.to_csv(output_file, index=False)
print(f"\nDataset saved to '{output_file}'")

# Display first few rows
print(f"\nFirst 5 rows:")
print(big_dataset.head())

# Show some statistics about the melanoma tr1 subset (for testing your response analysis)
melanoma_tr1 = big_dataset[
    (big_dataset['condition'] == 'melanoma') & 
    (big_dataset['treatment'] == 'tr1') & 
    (big_dataset['sample_type'] == 'PBMC')
]
print(f"\nMelanoma TR1 PBMC samples: {len(melanoma_tr1)}")
if len(melanoma_tr1) > 0:
    baseline_melanoma_tr1 = melanoma_tr1[melanoma_tr1['time_from_treatment_start'] == 0]
    print(f"Baseline melanoma TR1 PBMC samples: {len(baseline_melanoma_tr1)}")
    
    melanoma_tr1_with_response = melanoma_tr1[melanoma_tr1['response'].isin(['y', 'n'])]
    if len(melanoma_tr1_with_response) > 0:
        responders = (melanoma_tr1_with_response['response'] == 'y').sum()
        print(f"TR1 melanoma responders: {responders}/{len(melanoma_tr1_with_response)}")

        