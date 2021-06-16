import os
import csv
import operator

MAX_WEIGHT = 4000000  # Max weight of a block
OUT_FILE_NAME = "block.txt"  # Output block filename


def get_id(txn):
    """Returns the transaction ID of a given row"""
    return txn[0]


def get_fees(txn):
    """Returns the transaction fees of a given row"""
    return int(txn[1])


def get_weight(txn):
    """Returns the transaction weight of a given row"""
    return int(txn[2])


def get_parent_txns(txn):
    """Returns the parent transactions of a given row pertaining to a transaction ID"""
    return txn[3]


def parse_mempool(file_name):
    """Returns a CSV Reader object after parsing mempool.csv file and skips the header"""
    file_contents = open(file_name)
    next(file_contents, None)
    return csv.reader(file_contents, delimiter=",")


def return_list_csv(csv_reader):
    """Returns a list of list representation of the CSV Reader"""
    return list(csv_reader)


def sort_csv(csv_reader):
    """Returns a sorted list of txns based on descending order of the fees"""
    return sorted(csv_reader, key=lambda row: int(row[1]), reverse=True)


def find_parent_txns(fees_sorted_txns):
    """Returns a dictionary of child Transaction IDs and athe corresponnding parent transactions"""
    child_parent_rel = {}
    for txn in fees_sorted_txns:
        txn_id = get_id(txn)
        p_txns = get_parent_txns(txn)
        if p_txns != "":
            child_parent_rel[txn_id] = p_txns
        else:
            child_parent_rel[txn_id] = None
    return child_parent_rel


def return_txn_weight_dict(fees_sorted_txns):
    """Returns a dictionary of all transactions and their corresponding weights"""
    txn_weights = {}
    for txn in fees_sorted_txns:
        txn_weights[txn[0]] = int(txn[2])
    return txn_weights


def if_p_txn_exists_before(observed_txns, parent_txns):
    """Returns True/False based on whether parent_txns exist in the observed txns so far"""
    return parent_txns.issubset(observed_txns)


def find_all_parent_txns(txn_id, child_parent_rel):
    """Recursive function to find and return all parent txns and return them in order to avoid block violations"""
    if child_parent_rel[txn_id] == None:
        return []
    else:
        parent_txns = []
        for parent_id in child_parent_rel[txn_id].split(";"):
            parent_txns.extend(find_all_parent_txns(parent_id, child_parent_rel))
        parent_txns += child_parent_rel[txn_id].split(";")
        return parent_txns


def find_candidate_txns(
    fees_sorted_txns, txn_weights, child_parent_rel, max_wgt=MAX_WEIGHT
):
    candidate_txns = []
    block_wgt = 0
    for txn in fees_sorted_txns:
        txn_id = get_id(txn)
        if child_parent_rel[txn_id] != "":
            parent_txns = find_all_parent_txns(txn_id, child_parent_rel)
            if block_wgt < max_wgt:
                s = set(candidate_txns)
                diff = [txn for txn in parent_txns if txn not in s]
                for _ in diff:
                    block_wgt += txn_weights[_]
                if block_wgt < max_wgt:
                    candidate_txns = candidate_txns + diff
                else:
                    break
            else:
                break  # Max Weight achieved
        else:
            if block_wgt < max_wgt and int(get_fees(txn)) > 0:
                candidate_txns.append(txn_id)
                block_wgt += get_weight(txn)
            else:
                print("MAX WEIGHT achieved")
                break
    return candidate_txns, block_wgt


def write_txns(candidate_txns, file_name=OUT_FILE_NAME):
    """Writes the candidate transactions into block.txt file"""
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, "w") as f:
        f.write("\n".join(candidate_txns))


if __name__ == "__main__":
    csv_reader = parse_mempool("mempool.csv")
    fees_sorted_txns = sort_csv(csv_reader)
    child_parent_rel = find_parent_txns(fees_sorted_txns)
    txn_weights = return_txn_weight_dict(fees_sorted_txns)
    candidate_txns, block_wgt = find_candidate_txns(
        fees_sorted_txns, txn_weights, child_parent_rel
    )
    print(len(candidate_txns))
    print(block_wgt)
    write_txns(candidate_txns)