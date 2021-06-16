import csv

mempool_file_name = "mempool.csv"
block_file_name = "block.txt"

MAX_WEIGHT = 4000000


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


def sort_csv(csv_reader):
    """Returns a sorted list of txns based on descending order of the fees"""
    return sorted(csv_reader, key=lambda row: int(row[1]), reverse=True)


def return_txn_weight_dict(fees_sorted_txns):
    """Returns a dictionary of all transactions and their corresponding weights"""
    txn_weights = {}
    for txn in fees_sorted_txns:
        txn_weights[txn[0]] = int(txn[2])
    return txn_weights


def parse_block(file_name):
    """Returns a list of all the transactions from the block file"""
    txns = [txn.rstrip() for txn in open(file_name)]
    return txns


def check_total_weight(txn_weights, block_list):
    """Test case to check for total weight < MAX_WEIGHT condition"""
    block_wgt = 0
    for txn in block_list:
        block_wgt += txn_weights[txn]
    if block_wgt < MAX_WEIGHT:
        return True, block_wgt
    else:
        return False, block_wgt


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


def check_order_of_transactions(child_parent_rel, block_list):
    """Test case to check if the transactions are in the order compliant with the block or not"""
    observed_txns = set()
    for txn in block_list:
        observed_txns.add(txn)
        parent_ids = child_parent_rel[txn]
        if parent_ids != None:
            for parent_id in parent_ids.split(";"):
                if parent_id in observed_txns:
                    continue
                else:
                    print("parent_id not found for txn" + txn)
                    return False
        else:
            continue

    return True


def check_duplicate_transactions(block_list):
    block_list_set = set(block_list)
    if len(block_list_set) == len(block_list):
        return True
    else:
        return False


if __name__ == "__main__":
    csv_reader = parse_mempool(mempool_file_name)
    block_txns = parse_block(block_file_name)
    fees_sorted_txns = sort_csv(csv_reader)
    txn_weights = return_txn_weight_dict(fees_sorted_txns)
    child_parent_rel = find_parent_txns(fees_sorted_txns)

    res, block_wgt = check_total_weight(txn_weights, block_txns)

    if res == True:
        print("Weight is less than Max Weight, Test case passed")
    else:
        print(
            "Faulty block, block weight is more than the MAX_WEIGHT, please investigate the discrepancies"
        )

    res = check_order_of_transactions(child_parent_rel, block_txns)

    if res == True:
        print("Order of transactions is valid, Test case passed")
    else:
        print(
            "Faulty block, order of transactions does not match, please investigate the discrepancies"
        )

    res = check_duplicate_transactions(block_txns)

    if res == True:
        print("No duplicates found, Test case passed")
    else:
        print(
            "Faulty block, duplicate transactions found, please investigate the discrepancies"
        )
