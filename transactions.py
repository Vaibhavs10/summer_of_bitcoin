import csv
import operator

def parse_mempool(file_name):
	file_contents = open(file_name)
	next(file_contents, None)
	return csv.reader(file_contents, delimiter=',')

def sort_csv(csv_reader):
	return sorted(csv_reader, key=lambda row: row[2], reverse=True)

csv_reader = parse_mempool("mempool.csv")
sorted_list = sort_csv(csv_reader)
print(sorted_list[0])