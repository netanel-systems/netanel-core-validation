"""Coding task dataset for validation scenarios.

50+ diverse coding tasks across varying complexity and domains.
Used to test netanel-core's learning algorithm with real-world tasks.
"""

CODING_TASKS = [
    # Easy tasks (10)
    "Write a Python function that checks if a number is prime.",
    "Create a function to reverse a string without using built-in reverse methods.",
    "Implement a function to find the factorial of a number using recursion.",
    "Write a function that returns the nth Fibonacci number.",
    "Create a function to check if a string is a palindrome.",
    "Implement a function to find the maximum element in a list.",
    "Write a function to count vowels in a string.",
    "Create a function that removes duplicates from a list.",
    "Implement a function to merge two sorted lists.",
    "Write a function to calculate the sum of digits in a number.",
    # Medium tasks (20)
    "Implement a binary search algorithm.",
    "Create a function to find all prime numbers up to n using Sieve of Eratosthenes.",
    "Write a function to implement quicksort algorithm.",
    "Implement a function to detect cycle in a linked list.",
    "Create a function to find the longest common subsequence of two strings.",
    "Write a function to validate a sudoku board.",
    "Implement a function to perform matrix multiplication.",
    "Create a function to find all permutations of a string.",
    "Write a function to implement a basic LRU cache.",
    "Implement a function to parse and evaluate mathematical expressions.",
    "Create a function to find the shortest path in a graph using Dijkstra's algorithm.",
    "Write a function to implement a trie data structure.",
    "Implement a function to validate balanced parentheses.",
    "Create a function to find the median of two sorted arrays.",
    "Write a function to implement merge sort algorithm.",
    "Implement a function to rotate a matrix 90 degrees.",
    "Create a function to find all anagrams in a list of words.",
    "Write a function to implement a basic regex matcher.",
    "Implement a function to serialize and deserialize a binary tree.",
    "Create a function to find the kth largest element in an array.",
    # Hard tasks (15)
    "Implement a function to solve the N-Queens problem.",
    "Create a function to find the longest palindromic substring.",
    "Write a function to implement the A* pathfinding algorithm.",
    "Implement a function to solve Sudoku using backtracking.",
    "Create a function to find the minimum window substring.",
    "Write a function to implement a Red-Black tree.",
    "Implement a function to solve the traveling salesman problem.",
    "Create a function to find the longest increasing path in a matrix.",
    "Write a function to implement a bloom filter.",
    "Implement a function to solve the word ladder problem.",
    "Create a function to find all solutions to N-Queens problem.",
    "Write a function to implement consistent hashing.",
    "Implement a function to detect arbitrage opportunities in currency exchange.",
    "Create a function to solve the job scheduling problem with deadlines.",
    "Write a function to implement a skip list data structure.",
    # Web/API tasks (5)
    "Write a Python function to parse HTML and extract all links.",
    "Create a function to validate email addresses using regex.",
    "Implement a function to calculate rate limiting for an API.",
    "Write a function to parse JSON and handle nested structures.",
    "Create a function to generate a secure random password.",
    # Data tasks (5)
    "Write a function to calculate moving average of a time series.",
    "Create a function to normalize data using min-max scaling.",
    "Implement a function to detect outliers using IQR method.",
    "Write a function to calculate correlation between two datasets.",
    "Create a function to perform one-hot encoding on categorical data.",
]

# Verify we have 50+ tasks
assert len(CODING_TASKS) >= 50, f"Expected >= 50 tasks, got {len(CODING_TASKS)}"
