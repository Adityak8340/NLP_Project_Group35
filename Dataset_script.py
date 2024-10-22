from groq import Groq
from dotenv import load_dotenv
import os
import json
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

load_dotenv()



def get_columns(description, client):
    """
    Extract specific information from CVE description using Groq API
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
    
    Example good response for "Buffer overflow in Apache HTTP Server 2.4.2 allows remote attackers to execute arbitrary code":
    {{
        "Operating_System": "NA",
        "Software_Component": "Apache HTTP Server",
        "Version": "2.4.2",
        "Impact": "arbitrary code execution",
        "Affected_Hardware": "NA",
        "Network_Requirements": "remote",
        "Affected_Protocols": "HTTP",
        "Authentication_Required": "NA",
        "Privileges_Required": "NA",
        "User_Interaction_Required": "NA",
        "Vendor": "Apache"
    }}
    """
    
    try:
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
        

        json_str = response_text.strip()
        if json_str.startswith('```json'):
            json_str = json_str[7:-3]  
        
        extracted_info = json.loads(json_str)
        
    
        valid_fields = [
            "Operating_System", "Software_Component", "Version", "Impact",
            "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
            "Authentication_Required", "Privileges_Required", 
            "User_Interaction_Required", "Vendor"
        ]
        
        
        for field in valid_fields:
            if field not in extracted_info or not extracted_info[field]:
                extracted_info[field] = "NA"
            elif isinstance(extracted_info[field], str) and extracted_info[field].lower() == "none":
                extracted_info[field] = "NA"
                
        return extracted_info
        
    except Exception as e:
        print(f"Error processing description: {e}")
        return {field: "NA" for field in [
            "Operating_System", "Software_Component", "Version", "Impact",
            "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
            "Authentication_Required", "Privileges_Required", 
            "User_Interaction_Required", "Vendor"
        ]}

def process_dataset(data, client, batch_size=5):
    """
    Process the dataset in batches and add new columns
    """

    new_columns = [
        "Operating_System", "Software_Component", "Version", "Impact",
        "Affected_Hardware", "Network_Requirements", "Affected_Protocols",
        "Authentication_Required", "Privileges_Required", 
        "User_Interaction_Required", "Vendor"
    ]
    
    for col in new_columns:
        data[col] = "NA"
    

    print("Processing descriptions...")
    for idx in tqdm(data.index):
        try:
            description = data.loc[idx, 'DESCRIPTION']
            
        
            extracted_info = get_columns(description, client)
            
            
            for col in new_columns:
                data.loc[idx, col] = extracted_info.get(col, "NA")
            

            if idx > 0 and idx % 100 == 0:
                data.to_excel("Global_Dataset_Updated.xlsx", index=False)
                print(f"\nSaved progress at row {idx}")
                
        except Exception as e:
            print(f"\nError processing row {idx}: {e}")
            continue
    
    
    data.to_excel("Global_Dataset_Updated.xlsx", index=False)
    return data

def main():
    
    load_dotenv()
    # groq_api = os.getenv("GROQ_API_KEY")
    # client = Groq(api_key="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")
    client=OpenAI(api_key="sk-7zWCl-ab2-or6uvZmeEB2pjT8COrAu0Q6JJrQJE76TT3BlbkFJz8V3yBaXiLNwSl5TbyQAzot9N_apWTAMbwiWwDim4A")
    
    try:
        # Read the dataset
        data = pd.read_csv("Training_data.csv")
        data=data[4800:]
        print(f"Loaded dataset with {len(data)} rows")
        
        # Process the dataset
        updated_data = process_dataset(data, client)
        
        print("\nProcessing completed!")
        print(f"Updated dataset saved to 'Global_Dataset_Updated.xlsx'")
        
        # Display sample of processed data
        print("\nSample of processed data:")
        print(updated_data.head(2))
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()