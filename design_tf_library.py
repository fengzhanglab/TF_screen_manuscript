import csv
import argparse

def get_tfs(tf_out_file, marker_out_file, library_file, genes_file, ndatasets):
	"""
	creates a list of tfs and marker genes for targeted TF screening
	tf_out_file: subset of tfs that overlap datasets listed in genes_file
	marker_out_file: marker genes that overlap datasets listed in genes_file
	library_file: genome-scale tf library
	genes_file: lists of genes specifically expressed in target cell type from different datasets
	ndatasets: minimum number of datasets with tf or marker gene
	"""

	# open gene file for lists of genes specifically expressed in target cell type
	with open(genes_file, 'rb') as infile:
		data = [list(set(row[1:])) for row in csv.reader(infile.read().splitlines())]

	# get set of genes that are found in at least ndatasets
	gene_list = sum(data, [])
	gene_list = [gene.upper() for gene in gene_list if len(gene) > 0]
	gene_set = list(set(gene_list))
	gene_overlap = [gene for gene in gene_set if gene_list.count(gene) >= ndatasets]

	# open tf library file for list of tfs in library
	with open(library_file, 'rb') as infile:
		data = [row for row in csv.reader(infile.read().splitlines())]
		tf_list = list(set([row[2] for row in data[1:]]))

	# retrieve list of tfs from tf library that are in gene_overlap
	tf_out = [data[0]+['nDatasets']]
	for row in data[1:]:
		gene = row[2]
		if gene in gene_overlap:
			tf_out.append(row + [gene_list.count(gene)])
	tf_out = sorted(tf_out, key=lambda x:x[-1], reverse=True)

	# get list of marker genes in gene_overlap that are not TFs
	marker_out = [['Gene', 'nDatasets']]
	for gene in gene_overlap:
		if gene not in tf_list:
			marker_out.append([gene, gene_list.count(gene)])
	marker_out = sorted(marker_out, key=lambda x:x[-1], reverse=True)

	# write subset of tfs to output file
	with open(tf_out_file, 'wb') as csvfile:
		csvwriter = csv.writer(csvfile)
		for row in tf_out:
			csvwriter.writerow([str(x) for x in row])

	# write marker genes to output file
	with open(marker_out_file, 'wb') as csvfile:
		csvwriter = csv.writer(csvfile)
		for row in marker_out:
			csvwriter.writerow([str(x) for x in row])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Design targeted tf library and marker genes for tf screening')
	parser.add_argument('-t', '--tfout', type=str, dest='tf_out_file',
		help='tf output file name', default='targeted_tf_library.csv')
	parser.add_argument('-m', '--markerout', type=str, dest='marker_out_file',
		help='marker output file name', default='marker_genes.csv')
	parser.add_argument('-l', '--library', type=str, dest='library_file',
		help='tf library file name', default='tf_library.csv')
	parser.add_argument('-g', '--genes', type=str, dest='genes_file',
		help='lists of genes specifically expressed in target cell type', default='candidate_genes.csv')
	parser.add_argument('-n', '--ndatasets', type=int, dest='ndatasets',
		help='minimum number of datasets with candidate gene', default=2)
	args = parser.parse_args()

	get_tfs(args.tf_out_file, args.marker_out_file, args.library_file, args.genes_file, args.ndatasets)
