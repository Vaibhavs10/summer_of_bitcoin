import csv
import operator

MAX_WEIGHT = 4000000
OUT_FILE_NAME = "block.txt"

def parse_mempool(file_name):
	file_contents = open(file_name)
	next(file_contents, None)
	return csv.reader(file_contents, delimiter=',')

def sort_csv(csv_reader):
	return sorted(csv_reader, key=lambda row: row[1], reverse=True)

def find_parent_txns(fees_sorted_txns):
	child_parent_rel = {}
	for txn in fees_sorted_txns:
		if txn[3] != '':
			child_parent_rel[txn[0]] = txn[3]
		else:
			child_parent_rel[txn[0]] = None
	return child_parent_rel

def get_fees(txn):
	return int(txn[1])

def get_weight(txn):
	return int(txn[2])

def find_candidate_txns(fees_sorted_txns, child_parent_rel, max_wgt=MAX_WEIGHT):
	candidate_txns = []
	block_wgt = 0
	for txn in fees_sorted_txns:
		if txn[3] != '':
			continue
		else:
			if block_wgt < max_wgt and int(txn[1]) > 0:
				candidate_txns.append(txn[0])
				block_wgt+=get_weight(txn)
			else:
				print("MAX WEIGHT achieved")
				break
	return candidate_txns

def write_txns(candidate_txns, file_name=OUT_FILE_NAME):
	with open(file_name, 'w') as f:
		f.write('\n'.join(candidate_txns))

csv_reader = parse_mempool("mempool.csv")
fees_sorted_txns = sort_csv(csv_reader)
child_parent_rel = find_parent_txns(fees_sorted_txns)
candidate_txns = find_candidate_txns(fees_sorted_txns, child_parent_rel)
write_txns(candidate_txns)