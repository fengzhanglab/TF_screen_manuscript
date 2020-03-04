# TF_screen_manuscript
Code for Joung et al, manuscript. A Multiplexed Transcription Factor Screening Platform for Directed Differentiation.

Once a target cell type has been selected, prepare the candidate genes .csv file, which contains lists of genes from published RNA-seq datasets that are specifically expressed in the target cell type. Genes from each dataset are listed such that each row contains genes from one dataset. The first column contains the description for the particular dataset, followed by the list of genes. Refer to the cardiomyocyte_candidate_genes.csv file for a sample input file.

To design a targeted TF library, run Python design_tf_library.py with the following optional parameters:

'-t'	targeted TF library output file name

'-m'	marker gene output file name

'-l'	input TF library (Supplementary Table S1 from manuscript)

'-g'	lists of candidate genes specifically expressed in target cell type from different datasets

'-n'	minimum number of datasets with candidate gene

The script will out put lists of marker genes and TFs from the genome-scale TF library to screen for differentiation of the target cell type. Both lists are ranked based on the number of datasets listing the gene, or the last column of the output file.
