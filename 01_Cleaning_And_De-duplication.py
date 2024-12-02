import pandas as pd

name = ''  # Write your professor's name

def process_and_clean_data(input_file1, input_file2, output_file):
    # Read the first Excel file
    df1 = pd.read_excel(input_file1)

    # Define a function to split authors
    def split_authors(authors):
        separators = [';', ',']
        for sep in separators:
            authors = ' '.join(authors.split(sep))
        return [name.strip() for name in authors.split()]

    # Process the 'authors' column
    df1['Authors'] = df1['Authors'].apply(split_authors)

    # Calculate the longest author list length
    max_length = df1['Authors'].apply(len).max()

    # Fill the new columns with the split author data
    for i in range(max_length):
        df1[f'Author {i+1}'] = df1['Authors'].apply(lambda x: x[i] if i < len(x) else None)

    df1.drop(columns=['Authors'], inplace=True)

    # Read the second Excel file
    df2 = pd.read_excel(input_file2)

    # Process the 'Keywords' column
    df2['Keywords'] = df2['Keywords'].str.replace('Keywords:', '', regex=False)

    def split_keywords(keywords):
        if pd.isna(keywords) or keywords.strip() == '':
            return []
        return [keyword.strip() for keyword in keywords.split(';')]

    df2['Keywords'] = df2['Keywords'].apply(split_keywords)

    # Calculate the maximum number of keywords
    max_keywords = df2['Keywords'].apply(len).max()

    # Fill the new keyword columns with split keyword data
    for i in range(max_keywords):
        df2[f'Keyword {i+1}'] = df2['Keywords'].apply(lambda x: x[i] if i < len(x) else None)

    # Drop the original 'Keywords' column
    df2.drop(columns=['Keywords'], inplace=True)

    # Clean the 'Publication Date' column
    def remove_time(date_str):
        try:
            dt = pd.to_datetime(date_str)
            return dt.date()  # Only keep the date part
        except ValueError:
            return date_str

    if 'Publication Date' in df1.columns:
        df1['Publication Date'] = df1['Publication Date'].apply(remove_time)
    if 'Publication Date' in df2.columns:
        df2['Publication Date'] = df2['Publication Date'].apply(remove_time)

    # Remove duplicates
    required_columns = ['Title', 'Journal', 'Publication Date', 'Downloads']
    df1 = df1.drop_duplicates(subset=required_columns, keep='first')
    df2 = df2.drop_duplicates(subset=required_columns, keep='first')

    # Check if 'Title' column exists
    if 'Title' not in df1.columns or 'Title' not in df2.columns:
        raise ValueError("One or both files are missing the 'Title' column")

    # Merge the data
    keyword_columns = [f'Keyword {i}' for i in range(1, max_keywords + 1)]
    df2_filtered = df2.dropna(subset=['Title'])

    columns_to_merge = ['Title', 'Abstract'] + keyword_columns
    merged_df = pd.merge(df1, df2_filtered[columns_to_merge], on='Title', how='left')

    # Ensure output file path has a valid extension
    if not output_file.endswith('.xlsx'):
        output_file += '.xlsx'

    # Save the merged DataFrame to a new Excel file
    merged_df.to_excel(output_file, index=False)
    print(f"Processed file has been saved to: {output_file}")

# Define file paths
input_file1 = f'{name}.xlsx'  # Input file path
input_file2 = f'{name} - Abstract.xlsx'  # Input file path
output_file = f'{name}(Processed).xlsx'  # Output file path

# Call the function
process_and_clean_data(input_file1, input_file2, output_file)
