import pandas as pd

def filter_first_500_per_year(input_file):
    """
    Filter first 500 entries of each year while maintaining original columns
    """
    try:
        # Read the CSV file
        df = pd.read_excel(input_file)
        
        # Initialize empty list to store filtered data
        filtered_data = []
        
        # Process each year from 1999 to 2021
        for year in range(1999, 2022):
            # Create the year pattern to match
            year_pattern = f'CVE-{year}-'
            
            # Get entries for this year
            year_data = df[df['CVE-ID'].str.startswith(year_pattern)].head(500)
            filtered_data.append(year_data)
        
        # Combine all filtered data
        result_df = pd.concat(filtered_data)
        
        # Save filtered dataset
        output_file = 'first_500_per_year.csv'
        result_df.to_csv(output_file, index=False)
        
        print(f"Dataset successfully filtered and saved to {output_file}")
        print(f"Total entries in filtered dataset: {len(result_df)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Replace 'your_dataset.csv' with your actual dataset filename
    input_file = r'C:\Users\91978\Desktop\nlp-project-grp_35\NLP_Project_Group35\Kaggle_Dataset\Global_Dataset.xlsx'
    filter_first_500_per_year(input_file)