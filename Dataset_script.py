from groq import Groq  # Import Groq library for interacting with the Groq API
from dotenv import load_dotenv  # Import dotenv to load environment variables
import os
import json
import pandas as pd  # Import pandas for handling data
from tqdm import tqdm  # Import tqdm for progress bar
from openai import OpenAI  # Import OpenAI library for chat completions

load_dotenv()  # Load environment variables from a .env file

def get_columns(description, client):
    """
    Extract specific information from a vulnerability description using the Groq API.

    Parameters:
    - description: str, the vulnerability description text
    - client: OpenAI client object to send the prompt to the OpenAI API

    Returns:
    - extracted_info: dict, extracted fields as per the specified JSON format
    """
    
    prompt = f"""
    Analyze the following vulnerability description and extract specific information.
    For each field, extract information ONLY if it's explicitly mentioned or can be clearly inferred from the description.
    If information for a field cannot be determined from the description, use "NA".
    Be precise and conservative in extraction - only include information that's clearly present.

    Description: {description}

    Extract the information as JSON format with these rules:
    - Operating_System: Extract if OS is mentioned (Windows, Linux, etc.) or NA if not specified
    - Software_Component: Extract the specific software/component affected
    - Version: Extract version numbers if mentioned, NA if not specified
    - Impact: Extract the impact (like code execution, denial of service, etc.)
    - Affected_Hardware: Extract hardware info if mentioned, NA if not specified
    - Network_Requirements: Extract if network access is needed (remote/local/none)
    - Affected_Protocols: Extract protocols mentioned (HTTP, FTP, etc.), NA if none
    - Authentication_Required: Extract if authentication is needed (Yes/No), NA if unclear
    - Privileges_Required: Extract privilege level needed, NA if not mentioned
    - User_Interaction_Required: Extract if user interaction is needed (Yes/No), NA if unclear
    - Vendor: Extract the vendor name if mentioned, NA if not specified

    Return ONLY the JSON object, nothing else.
    """

    try:
        # Send the prompt to the OpenAI API and get the response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=150
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Parse the response as JSON if it contains JSON format
        json_str = response_text.strip()
        if json_str.startswith('```json'):
            json_str = json_str[7:-3]  # Remove markdown format indicators
        
        extracted_info = json.loads(json_str)  # Load JSON string to a dictionary

        # Define required fields for extracted information
        valid_fields = [
            "Operating_System", "Software_Component", "Version", "Impact",
            "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
            "Authentication_Required", "Privileges_Required", 
            "User_Interaction_Required", "Vendor"
        ]
        
        # Fill missing fields with "NA"
        for field in valid_fields:
            if field not in extracted_info or not extracted_info[field]:
                extracted_info[field] = "NA"
            elif isinstance(extracted_info[field], str) and extracted_info[field].lower() == "none":
                extracted_info[field] = "NA"
                
        return extracted_info
        
    except Exception as e:
        # Print error and return default "NA" values if processing fails
        print(f"Error processing description: {e}")
        return {field: "NA" for field in [
            "Operating_System", "Software_Component", "Version", "Impact",
            "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
            "Authentication_Required", "Privileges_Required", 
            "User_Interaction_Required", "Vendor"
        ]}

def process_dataset(data, client, batch_size=5):
    """
    Process the dataset in batches and add new columns with extracted information.

    Parameters:
    - data: DataFrame containing the dataset with 'DESCRIPTION' column
    - client: OpenAI client object
    - batch_size: int, size of each batch (default: 5)

    Returns:
    - data: DataFrame with added columns for extracted information
    """

    # Define new columns to store extracted information
    new_columns = [
        "Operating_System", "Software_Component", "Version", "Impact",
        "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
        "Authentication_Required", "Privileges_Required", 
        "User_Interaction_Required", "Vendor"
    ]
    
    # Initialize new columns with "NA" as default values
    for col in new_columns:
        data[col] = "NA"
    
    print("Processing descriptions...")
    for idx in tqdm(data.index):
        try:
            description = data.loc[idx, 'DESCRIPTION']  # Get description text
            
            # Extract information from description
            extracted_info = get_columns(description, client)
            
            # Update DataFrame with extracted information
            for col in new_columns:
                data.loc[idx, col] = extracted_info.get(col, "NA")
            
            # Save progress to an Excel file every 100 rows
            if idx > 0 and idx % 100 == 0:
                data.to_excel("Global_Dataset_Updated.xlsx", index=False)
                print(f"\nSaved progress at row {idx}")
                
        except Exception as e:
            # Log any errors during row processing
            print(f"\nError processing row {idx}: {e}")
            continue
    
    # Save final processed dataset to an Excel file
    data.to_excel("Global_Dataset_Updated.xlsx", index=False)
    return data

def main():
    """
    Main function to load the dataset, process it, and save results to an Excel file.
    """
    
    load_dotenv()  # Load environment variables from .env file
    client = OpenAI(api_key="")  # Initialize OpenAI client with API key
    
    try:
        # Read the dataset from a CSV file
        data = pd.read_csv("Training_data.csv")
        data = data[4800:] 
        print(f"Loaded dataset with {len(data)} rows")
        
        # Process the dataset and extract information
        updated_data = process_dataset(data, client)
        
        print("\nProcessing completed!")
        print(f"Updated dataset saved to 'Global_Dataset_Updated.xlsx'")
        
        # Display a sample of processed data
        print("\nSample of processed data:")
        print(updated_data.head(2))
        
    except Exception as e:
        # Catch and print any errors during processing
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  # Run the main function
