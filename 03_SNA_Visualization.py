import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from plotly.colors import make_colorscale

# Read the edge and node data, and clean up IDs
edges_df = pd.read_csv('edges_data.csv', encoding='utf-8')
nodes_df = pd.read_csv('nodes_data.csv', encoding='utf-8')

edges_df['Source'] = edges_df['Source'].astype(str).str.strip()
edges_df['Target'] = edges_df['Target'].astype(str).str.strip()
nodes_df['Id'] = nodes_df['Id'].astype(str).str.strip()

# Create a NetworkX graph object
G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target', create_using=nx.Graph())

# Add nodes to the graph and set their labels
for idx, node in nodes_df.iterrows():
    node_id = node['Id']
    if node_id not in G.nodes:
        G.add_node(node_id)
    G.nodes[node_id]['Label'] = str(node.get('Label', ''))

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# Set centrality as node attributes
nx.set_node_attributes(G, degree_centrality, 'degree')
nx.set_node_attributes(G, closeness_centrality, 'closeness')
nx.set_node_attributes(G, betweenness_centrality, 'betweenness')

# Set positions for nodes using the spring layout
pos = nx.spring_layout(G)

# Prepare edge data for visualization
edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

# Create edge trace for Plotly
edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

# Prepare node data for visualization
node_x, node_y, node_labels, node_hover_texts, node_info_texts, node_sizes = [], [], [], [], [], []

for node in G.nodes(data=True):
    x, y = pos[node[0]]
    node_x.append(x)
    node_y.append(y)
    label = node[1].get('Label', '')
    node_labels.append(label)

    hover_text = f"Node: {label}<br>Degree Centrality: {node[1].get('degree', 0):.3f}<br>Closeness Centrality: {node[1].get('closeness', 0):.3f}<br>Betweenness Centrality: {node[1].get('betweenness', 0):.3f}"
    node_hover_texts.append(hover_text)

    info_text = f"{label}<br>Degree Centrality: {node[1].get('degree', 0):.3f}<br>Closeness Centrality: {node[1].get('closeness', 0):.3f}<br>Betweenness Centrality: {node[1].get('betweenness', 0):.3f}"
    node_info_texts.append(info_text)

    node_sizes.append(10 + node[1].get('degree', 0) * 30)

# Prepare node adjacency data
node_adjacencies = [G.degree[n] for n in G.nodes()]

# Create a color scale from dark red to light red
colorscale = [
    [0, 'rgb(255, 160, 169)'],   # Dark red
    [0.5, 'rgb(255, 69, 0)'],     # Orange-red
    [1, 'rgb(139, 0, 0)']         # Light red (pink)
]

# Collect all node information and sort by degree centrality
node_data = []
for node in G.nodes(data=True):
    x, y = pos[node[0]]
    label = node[1].get('Label', '')
    degree = node[1].get('degree', 0)
    hover_text = f"Node: {label}<br>Degree Centrality: {degree:.3f}<br>Closeness Centrality: {node[1].get('closeness', 0):.3f}<br>Betweenness Centrality: {node[1].get('betweenness', 0):.3f}"
    info_text = f"{label}<br>Degree Centrality: {degree:.3f}<br>Closeness Centrality: {node[1].get('closeness', 0):.3f}<br>Betweenness Centrality: {node[1].get('betweenness', 0):.3f}"
    size = 10 + degree * 30

    node_data.append((x, y, label, hover_text, info_text, size, degree))

# Sort nodes by degree centrality (ascending order)
node_data_sorted = sorted(node_data, key=lambda item: item[6])

# Unpack the sorted node data
node_x, node_y, node_labels, node_hover_texts, node_info_texts, node_sizes, node_adjacencies = zip(*node_data_sorted)

# Create node trace for Plotly
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[],
    textposition="top center",
    hoverinfo='text',
    hovertext=node_hover_texts,
    marker=dict(
        showscale=True,
        colorscale=colorscale,
        reversescale=False,
        color=node_adjacencies,
        size=node_sizes,
        colorbar=dict(
            thickness=15,
            title='Node Degree',
            xanchor='left',
            titleside='right'
        ),
        line_width=2),
    textfont=dict(size=10, family="SimHei")
)

# Create annotations for the figure
annotations = [
    dict(
        text="""<b>Social Network Analysis Centrality Measures:</b><br>
                - Degree Centrality: Represents the number of other nodes connected to this node.<br>
                - Closeness Centrality: Represents the inverse of the average shortest path length from this node to all other nodes.<br>
                - Betweenness Centrality: Represents the importance of this node as a bridge between other nodes in the network.""",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.01, y=0.01,
        align="left",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="rgba(255,255,255,0.8)",
        font=dict(family="SimHei", size=10, color="#000000"),
    )
]

# Create the figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Interactive Social Network Analysis Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=annotations,
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    font=dict(family="SimHei", size=10),
                    template="plotly_white"
                ))

# Save the figure to an HTML file
fig.write_html("network_graph.html",
               config={'scrollZoom': True},
               include_plotlyjs="cdn",
               post_script=["""
                   var fig = document.getElementById('network_graph');
                   fig.on('plotly_relayout', function(eventData) {
                       var trace = fig.data[1];
                       if (eventData['xaxis.range[0]'] !== undefined && eventData['xaxis.range[1]'] !== undefined) {
                           // Show labels and detailed info when zoomed in, disable hover info
                           trace.text = %s;
                           trace.hoverinfo = 'skip';
                       } else {
                           // Don't show labels when the full network is visible, only on hover
                           trace.text = Array(%d).fill('');
                           trace.hoverinfo = 'text';
                       }
                       Plotly.restyle(fig, {'text': [trace.text], 'hoverinfo': [trace.hoverinfo]}, [1]);
                   });
               """ % (node_info_texts, len(node_labels))
               ])

print("The graph has been saved as network_graph.html")
