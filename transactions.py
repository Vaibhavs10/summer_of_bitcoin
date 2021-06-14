import os
import csv
import operator

MAX_WEIGHT = 4000000
OUT_FILE_NAME = "block.txt"

def get_id(txn):
	return txn[0]

def get_fees(txn):
	return int(txn[1])

def get_weight(txn):
	return int(txn[2])

def get_parent_txns(txn):
	return txn[3]

def get_parent_txns(txn):
	return txn[3]

def parse_mempool(file_name):
	file_contents = open(file_name)
	next(file_contents, None)
	return csv.reader(file_contents, delimiter=',')

def return_list_csv(csv_reader):
	return list(csv_reader)

def sort_csv(csv_reader):
	return sorted(csv_reader, key=lambda row: int(row[1]), reverse=True)

def find_parent_txns(fees_sorted_txns):
	child_parent_rel = {}
	for txn in fees_sorted_txns:
		txn_id = get_id(txn)
		p_txns = get_parent_txns(txn)
		if p_txns != '':
			child_parent_rel[txn_id] = p_txns
		else:
			child_parent_rel[txn_id] = None
	return child_parent_rel

def find_parent_txn_loc(fees_sorted_txns, child_parent_rel):
	observed_txns = set()
	candidate_txns = []
	for txn in fees_sorted_txns:
		txn_id =  get_id(txn)
		observed_txns.add(txn_id)
		parent_txns = child_parent_rel[txn_id]
		if parent_txns != None:
			count = 0
			for p_txn in parent_txns.split(";"):
				if p_txn in observed_txns:
					continue
				else:
					count = 1
					break
			if count == 0:
				candidate_txns.append(txn_id)
	return candidate_txns


def find_candidate_txns(fees_sorted_txns, candidate_txn_w_p, child_parent_rel, max_wgt=MAX_WEIGHT):
	candidate_txns = []
	block_wgt = 0
	candidate_txn_w_p = set(candidate_txn_w_p)
	for txn in fees_sorted_txns:
		txn_id = get_id(txn)
		if child_parent_rel[txn_id] != '':
			if txn_id in candidate_txn_w_p:
				if block_wgt < MAX_WEIGHT:
					candidate_txns.append(txn_id)
					block_wgt+=get_weight(txn)
				else:
					break #Max Weight achieved		
		else:
			if block_wgt < max_wgt and int(txn[1]) > 0:
				candidate_txns.append(txn[0])
				block_wgt+=get_weight(txn)
			else:
				print("MAX WEIGHT achieved")
				break
	return candidate_txns, block_wgt

def write_txns(candidate_txns, file_name=OUT_FILE_NAME):
	if os.path.exists(file_name):
		os.remove(file_name)
	with open(file_name, 'w') as f:
		f.write('\n'.join(candidate_txns))

csv_reader = parse_mempool("mempool.csv")
fees_sorted_txns = sort_csv(csv_reader)
child_parent_rel = find_parent_txns(fees_sorted_txns)
candidate_txn_w_p = find_parent_txn_loc(fees_sorted_txns, child_parent_rel)
candidate_txns, block_wgt = find_candidate_txns(fees_sorted_txns, candidate_txn_w_p, child_parent_rel)
write_txns(candidate_txns)