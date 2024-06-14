### Katharina Wolff & Melina Sophie Nowak ###

import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def generate_heatmap(input_file, output_file, tab_separated=False):
    # Determine the delimiter based on the tab_separated flag
    delimiter = '\t' if tab_separated else ';'

    # Read the CSV table into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter=delimiter)

    # Extract the TPMS values
    tpms_data = data.drop('GeneID', axis=1)  # Extract the TPMS values (excluding the last column)
    tpms_data = tpms_data.iloc[:, :-1]  # Remove the 'Gene' column if necessary
    average_tpms = tpms_data.mean(axis=1)  # Calculate average TPM for each gene
    tpms_data['average_TPM'] = average_tpms  # Add a new column for average TPM
    filtered_tpms = tpms_data [tpms_data['average_TPM'] > 0]
    tpms_data = filtered_tpms.iloc[:, :-1]

    # Extract sequence descriptions from the last column
    filtered_tpms['GeneID']=data['GeneID']
    filtered_tpms['SeqRef']=data.iloc[:, -1]
    print(filtered_tpms)
    sequence_descriptions = filtered_tpms.iloc[:, -1]
    #print(sequence_descriptions)
    #print(tpms_data)

    # Extract condition names from the headers (Culture_Condition_Replicate format)
    conditions_replicates = [col.split('_')[1:] for col in tpms_data.columns]
    conditions, replicates = zip(*conditions_replicates)

    # Extract culture names from the headers
    cultures = [col.split('_')[0] for col in tpms_data.columns]

    # Create a list of gene names
    gene_names = filtered_tpms['GeneID']
    
        # Calculate the Z-score normalization for each row
    z_data = (tpms_data - tpms_data.mean(axis=1).values[:, None]) / tpms_data.std(axis=1).values[:, None]

    # Calculate the maximum absolute Z-score for color scale    
    max_abs_z = max(abs(z_data.min().min()), abs(z_data.max().max()))


    # Calculate the figure size based on the number of genes
    num_genes = tpms_data.shape[0]
    #figure_height = max(0.4, num_genes * 0.01) + 1  # Increase height by 1.0 for summary brackets
    figure_height = max(0.4, num_genes * 0.01) + 0.5  # Increase height by 1.0 for summary brackets


    # Create a heatmap using Seaborn
    plt.figure(figsize=(25, figure_height))  # Set initial figure size
    ax = sns.heatmap(z_data, cmap='bwr', annot=tpms_data, fmt=".2f", linewidths=0.5,
    yticklabels=gene_names + '\n' + sequence_descriptions, center=0, cbar=True, vmin=-max_abs_z, vmax=max_abs_z, annot_kws={"fontsize": 30})  # Set vmin and vmax
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=30)

    # Customize x-axis labels
    ax.set_xticks([])  # Hide x-axis ticks
    ax.set_xticklabels([])  # Hide x-axis labels



    # Customize y-axis labels
    for i, (gene, sequence) in enumerate(zip(gene_names, sequence_descriptions)):
        #print(sequence)
        # Set gene name in italic and larger font size
        font_properties = FontProperties(style='italic', size=35, weight='bold')

        # Set sequence description below the gene name
        ax.text(-0.005, i + 0.7, gene, ha='right', va='center', fontsize=30, transform=ax.get_yaxis_transform())


        ax.text(-0.005, i + 0.3, sequence, ha='right', va='center', fontproperties=font_properties, transform=ax.get_yaxis_transform())
        

   # ax.set_ylim(0, len(gene_names))
    ax.tick_params(axis='y', left=False) 
    ax.set_yticks(range(len(gene_names)))

    # Add boxes around replicates for each condition with labels
    current_condition = conditions[0]
    current_culture = cultures[0]
    box_start = 0
    box_end = 0

    for i, (condition, replicate, culture) in enumerate(zip(conditions, replicates, cultures)):
        if condition != current_condition or culture != current_culture:
            # Draw a box around replicates of the same condition
            #ax.add_patch(plt.Rectangle((box_start, num_genes - 0.08), box_end - box_start, num_genes + 2, fill=False, linewidth=2, edgecolor='red'))
            ax.text((box_start + box_end) / 2, num_genes + 0.7, f"Condition: {current_condition}", ha='center', va='center', fontsize=20)
            
            # Update box start and end positions for the next condition
            box_start = i
            box_end = i

            current_condition = condition
            current_culture = culture
        else:
            box_end = i+1  # Expand the box for the current condition
        
        ax.text(i + 0.5, num_genes + 0.3, f"{replicate}", ha='center', va='center', fontsize=35)

    # Draw the last box
    #ax.add_patch(plt.Rectangle((box_start, num_genes - 0.08), box_end - box_start, num_genes + 2, fill=False, linewidth=2, edgecolor='red'))
    ax.text((box_start + box_end) / 2, num_genes + 0.9, f"Condition: {current_condition}", ha='center', va='center', fontsize=20)

    # Add boxes around conditions with the same culture and label them with the culture name
    current_culture = cultures[0]
    box_start = 0
    box_end = 0

    for i, (condition, culture) in enumerate(zip(conditions, cultures)):
        if culture != current_culture:
            # Draw a box around conditions with the same culture
            #ax.add_patch(plt.Rectangle((box_start, num_genes - 0.08), box_end - box_start, num_genes + 2, fill=False, linewidth=2, edgecolor='blue'))
            ax.text((box_start + box_end) / 1.7, num_genes + 1.7, f"Sample: {current_culture}", ha='center', va='center', fontsize=20)
            
            # Update box start and end positions for the next culture
            box_start = i
            box_end = i

            current_culture = culture
        else:
            box_end = i+1  # Expand the box for the current condition

    # Draw the last box
    #ax.add_patch(plt.Rectangle((box_start, num_genes - 0.08), box_end - box_start, num_genes + 2, fill=False, linewidth=2, edgecolor='blue'))
    ax.text((box_start + box_end) / 2, num_genes + 1.7, f"Sample: {current_culture}", ha='center', va='center', fontsize=20)

    # Adjust figure size to maintain aspect ratio
    fig = ax.get_figure()
    current_size = fig.get_size_inches()
    fig.set_size_inches(current_size[0], current_size[0] * figure_height)

    # Save the heatmap plot as a PNG file with the same name as the input file
    output_folder = os.path.dirname(output_file)
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(output_file, bbox_inches='tight', dpi=300)

# Wrapper script: Usage, und aufruf der gesamten scripts, wenn ich nur python3 aufrufe mit script name wird folgendes ausgegeben: Nutzung usw.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate heatmap from CSV files.')
    parser.add_argument('--in_file', help='Path to the input CSV file')
    parser.add_argument('--in_folder', help='Path to the input folder with multiple CSV files')
    parser.add_argument('--tab_separated', action='store_true', help='Specify if input CSV files are tab-separated')
    args = parser.parse_args()

    if args.in_file:
        input_file = args.in_file
        output_file = os.path.splitext(input_file)[0] + '_z_score_4.png'
        generate_heatmap(input_file, output_file, args.tab_separated)
    elif args.in_folder: #kann auch alle .csv files aus dem folder nehmen und zu jedem eine heatmap erstellen
        folder_path = args.in_folder
        # Get all CSV files in the folder
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

        # Generate heatmaps for each CSV file in the folder
        for file in csv_files:
            input_file = os.path.join(folder_path, file)
            output_file = os.path.splitext(input_file)[0] + '_z_score_4.png'
            generate_heatmap(input_file, output_file, args.tab_separated)
    else:
        parser.error('Either --in_file or --in_folder argument must be provided.')
