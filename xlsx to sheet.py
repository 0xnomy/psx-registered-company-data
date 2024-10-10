import pandas as pd
import os

# Directory containing your Excel files
directory = 'D:\GPDA\Scrapper\PSX Final Dataset'

# Output file where all sheets will be saved
output_file = 'combined_excel_file.xlsx'

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Loop through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.xlsx'):  # Check if the file is an Excel file
            file_path = os.path.join(directory, file_name)
            
            # Load each Excel file into a DataFrame
            df = pd.read_excel(file_path)
            
            # Use the file name as the sheet name (without the .xlsx extension)
            sheet_name = os.path.splitext(file_name)[0]
            
            # Write the DataFrame to a new sheet in the output Excel file
            df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Files combined into {output_file}")
