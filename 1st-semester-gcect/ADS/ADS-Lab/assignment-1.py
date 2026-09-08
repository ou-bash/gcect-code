import random
import time
import matplotlib.pyplot as plt


# ============================================================
# 1. LINKED LIST REPRESENTATION
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.representative = data


class LinkedListDSU:

    def __init__(self, n):
        self.n = n
        self.nodes = [Node(i) for i in range(n)]

    def make_set(self, x):
        self.nodes[x] = Node(x)

    def find_set(self, x):
        return self.nodes[x].representative

    def union(self, x, y):

        root_x = self.find_set(x)
        root_y = self.find_set(y)

        if root_x == root_y:
            return False

        # Traverse the second list and update representatives
        current = self.nodes[root_y]

        while current is not None:
            current.representative = root_x
            current = current.next

        # Find the end of first list
        tail = self.nodes[root_x]

        while tail.next is not None:
            tail = tail.next

        # Join second list to first list
        tail.next = self.nodes[root_y]

        return True


# ============================================================
# 2. RANKED LINKED LIST REPRESENTATION
#    (Weighted union: smaller list is attached to larger list)
# ============================================================

class RankedLinkedListDSU:

    def __init__(self, n):
        self.n = n
        self.nodes = [Node(i) for i in range(n)]
        self.size = [1] * n

    def make_set(self, x):
        self.nodes[x] = Node(x)
        self.size[x] = 1

    def find_set(self, x):
        return self.nodes[x].representative

    def union(self, x, y):

        root_x = self.find_set(x)
        root_y = self.find_set(y)

        if root_x == root_y:
            return False

        # Attach smaller list to larger list
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        # Update representatives of smaller list
        current = self.nodes[root_y]

        while current is not None:
            current.representative = root_x
            current = current.next

        # Find end of larger list
        tail = self.nodes[root_x]

        while tail.next is not None:
            tail = tail.next

        # Join lists
        tail.next = self.nodes[root_y]

        # Update size
        self.size[root_x] += self.size[root_y]

        return True


# ============================================================
# 3. TREE REPRESENTATION
#    Parent-pointer forest + union by rank + path compression
# ============================================================

class TreeDSU:

    def __init__(self, n):
        self.n = n
        self.parent = list(range(n))
        self.rank = [0] * n

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find_set(self, x):

        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find_set(self.parent[x])

        return self.parent[x]

    def union(self, x, y):

        root_x = self.find_set(x)
        root_y = self.find_set(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:

            self.parent[root_x] = root_y

        elif self.rank[root_x] > self.rank[root_y]:

            self.parent[root_y] = root_x

        else:

            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


# ============================================================
# GENERATE OPERATIONS
# ============================================================

def generate_operations(n, m, seed=42):

    random.seed(seed)

    operations = []

    # First n operations MUST be make-set
    for i in range(n):
        operations.append(("make", i))

    number_of_sets = n

    # Remaining operations
    while len(operations) < m:

        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)

        # If more than one set exists, allow union/find
        if number_of_sets > 1:

            if random.random() < 0.5:
                operations.append(("find", x))
            else:
                operations.append(("union", x, y))

        else:
            # Once only one set remains,
            # all remaining operations MUST be find operations.
            operations.append(("find", x))

    return operations


# ============================================================
# EXECUTE OPERATIONS AND MEASURE TIME
# ============================================================

def run_linked_list(n, operations):

    ds = LinkedListDSU(n)

    start = time.perf_counter()

    number_of_sets = n

    for operation in operations:

        if operation[0] == "make":

            ds.make_set(operation[1])

        elif operation[0] == "find":

            ds.find_set(operation[1])

        elif operation[0] == "union":

            x = operation[1]
            y = operation[2]

            if ds.union(x, y):
                number_of_sets -= 1

    end = time.perf_counter()

    return end - start


def run_ranked_linked_list(n, operations):

    ds = RankedLinkedListDSU(n)

    start = time.perf_counter()

    number_of_sets = n

    for operation in operations:

        if operation[0] == "make":

            ds.make_set(operation[1])

        elif operation[0] == "find":

            ds.find_set(operation[1])

        elif operation[0] == "union":

            x = operation[1]
            y = operation[2]

            if ds.union(x, y):
                number_of_sets -= 1

    end = time.perf_counter()

    return end - start


def run_tree(n, operations):

    ds = TreeDSU(n)

    start = time.perf_counter()

    number_of_sets = n

    for operation in operations:

        if operation[0] == "make":

            ds.make_set(operation[1])

        elif operation[0] == "find":

            ds.find_set(operation[1])

        elif operation[0] == "union":

            x = operation[1]
            y = operation[2]

            if ds.union(x, y):
                number_of_sets -= 1

    end = time.perf_counter()

    return end - start


# ============================================================
# EXPERIMENT
# ============================================================

n = 100

m_values = [
    200,
    300,
    500,
    1000,
    1200,
    1500,
    1800,
    2000,
    2400,
    2800,
    3000
]


linked_list_times = []
ranked_linked_list_times = []
tree_times = []


for m in m_values:

    operations = generate_operations(n, m)

    t1 = run_linked_list(n, operations)
    t2 = run_ranked_linked_list(n, operations)
    t3 = run_tree(n, operations)

    linked_list_times.append(t1)
    ranked_linked_list_times.append(t2)
    tree_times.append(t3)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nPerformance Comparison")
print("-" * 70)

print(
    f"{'m':<10}"
    f"{'Linked List':<20}"
    f"{'Ranked Linked List':<25}"
    f"{'Tree':<20}"
)

print("-" * 70)

for i in range(len(m_values)):

    print(
        f"{m_values[i]:<10}"
        f"{linked_list_times[i]:<20.8f}"
        f"{ranked_linked_list_times[i]:<25.8f}"
        f"{tree_times[i]:<20.8f}"
    )


# ============================================================
# PLOT: TIME TAKEN VS m
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    m_values,
    linked_list_times,
    marker="o",
    label="Linked List"
)

plt.plot(
    m_values,
    ranked_linked_list_times,
    marker="s",
    label="Ranked Linked List"
)

plt.plot(
    m_values,
    tree_times,
    marker="^",
    label="Tree"
)

plt.xlabel("Number of Operations (m)")
plt.ylabel("Time Taken (seconds)")

plt.title(
    "Union-Find Performance: Time Taken vs Number of Operations"
)

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
