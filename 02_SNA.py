import pandas as pd
from itertools import combinations

name = '' # Write your professor's name

def prepare_data_for_gephi_and_export(file_path, nodes_output_path_csv, edges_output_path_csv):
    """
    Prepare data for Gephi and export nodes and edges as CSV files.
    
    Args:
    - file_path: Path to the input Excel file containing academic journal data.
    - nodes_output_path_csv: Path to the output CSV file for the nodes.
    - edges_output_path_csv: Path to the output CSV file for the edges.
    """

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Check if the 'Title' column exists
    if 'Title' not in df.columns:
        raise ValueError("The file is missing the 'Title' column")

    # Determine the maximum author column number
    max_author_column = 0
    for col in df.columns:
        if col.startswith('Author') and col.endswith('Number'):
            try:
                author_num = int(col[5:-2])  # Extract the numeric part
                max_author_column = max(max_author_column, author_num)
            except ValueError:
                continue

    required_columns = ['Title'] + [f'Author {i}' for i in range(1, max_author_column + 1)]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"The file is missing the '{column}' column")

    # Initialize empty edge list and node set
    edges = []
    nodes = set()

    # Iterate through each row, extract the author list and generate all possible combinations
    for _, row in df.iterrows():
        authors = [row[f'Author {i}'] for i in range(1, max_author_column + 1) if pd.notna(row[f'Author {i}'])]
        if len(authors) > 1:
            edges.extend(combinations(authors, 2))
        nodes.update(authors)

    # Convert the edge list to a DataFrame
    edges_df = pd.DataFrame(edges, columns=['Source', 'Target'])

    # Convert the node set to a DataFrame
    nodes_df = pd.DataFrame(list(nodes), columns=['Id'])

    # If there is no 'Label' column, add a 'Label' column and copy the values from the 'Id' column
    if 'Label' not in nodes_df.columns:
        nodes_df['Label'] = nodes_df['Id']

    # Export the node data as a CSV file
    nodes_df.to_csv(nodes_output_path_csv, index=False)
    print(f"Node data has been saved to: {nodes_output_path_csv}")

    # Export the edge data as a CSV file
    edges_df.to_csv(edges_output_path_csv, index=False)
    print(f"Edge data has been saved to: {edges_output_path_csv}")


# Define file paths
file_path = 'AcademicData.xlsx'  # Input file path
nodes_output_path_csv = 'nodes_data.csv'  # Output CSV file for nodes
edges_output_path_csv = 'edges_data.csv'  # Output CSV file for edges

# Call the function
prepare_data_for_gephi_and_export(file_path, nodes_output_path_csv, edges_output_path_csv)
