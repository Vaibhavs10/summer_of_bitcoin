# Summer of Bitcoin

Submission by [Vaibhav Srivastav](https://de.linkedin.com/in/vaibhavs10 "Vaibhav's LinkedIn")

## Run Guide

To create the block run:
```
python transactions.py
```
To run tests on the newly created block run:
```
python tests.py
```

Note: The code has only been tested on Python 3.8.5 and doesn't require any special packages except the standard library.

## Methodology

The key strategy used is to optimise on transaction fees.
1. Parse mempool.csv
2. Sort the transactions in descending order on fees
3. Find all the parents (& their parents & so on) for all the transactions with parent IDs
4. Slot in all the parent IDs before the child transaction ID
5. Write to block so long as the block weight is less than the MAX_WEIGHT

The focus while building this code was to ensure all the block conditions are met, hence a lot of quadratic lookups have been made to ensure that the transactions are valid.

## Further Improvements

There are a lot quadratic lookups throughout the code to check whether all the parents and their parents (and so on) are slotted in before the child transactions, for a large mempool, this would not scale well.
Possible imporvements could to be to use hashmaps or deques for faster search and access.
