import csv

def parse_mempool(file_name):
	with open('mempool.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		return csv_reader

parse_mempool("mempool.csv")