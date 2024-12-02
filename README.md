# Academic Journal Data Crawling and Social Network Analysis

This project involves three main steps: data crawling, data cleaning, and social network analysis using Python.

## Step 1: Data Crawling with Octopus Crawler

In this step, Octopus Crawler software is used to extract information from China National Knowledge Infrastructure (CNKI). The required information includes:

- **Title**
- **Author(s)**
- **Publication Time**
- **Abstract**
- **Keywords**
- **Journal Name**
- **Downloads** and more.

Since Octopus uses XPath for crawling, the process is not implemented directly with Python code. However, I plan to update the crawler's Python code in future updates to streamline this process.

## Step 2: Data Cleaning and De-duplication

After obtaining the raw data, the next step is to clean and de-duplicate it using Python. The key steps include:

1. **Data Cleaning**:
   - **Author Information**: Split the authors listed in one column into separate columns.
   - **Publication Time**: Convert the publication time into a standard date format for easier manipulation.
   - **Keywords and Abstracts**: Clean empty spaces and split the keywords into separate columns (similar to authors).

2. **De-duplication**:
   - Use four columns (title, authors, time, and journal) to remove duplicates.

After cleaning and de-duplication, the two datasets are merged into a single, structured file.

## Step 3: Social Network Analysis and Visualization

In this step, social network analysis is performed on the author data:

1. **Edge and Node Data Creation**:
   - Use the `combinations` function from the `itertools` module to generate all possible combinations (edges) between authors.

2. **Network Visualization**:
   - Compute **degree centrality**, **closeness centrality**, and **betweenness centrality** for each node.
   - Use `nx.spring_layout` from **NetworkX** to determine node positions using a force-directed algorithm, ensuring uniform distances between connected nodes.
   - Create an interactive visualization using **Plotly** and save it as an HTML file.

## Libraries Used:
- `pandas`: For data cleaning and manipulation.
- `itertools`: For generating combinations of authors (edges).
- `NetworkX`: For network analysis and centrality calculations.
- `Plotly`: For interactive visualizations.

### Future Updates:
I will update the crawling process and provide Python code for extracting data from CNKI in future versions of the project.
