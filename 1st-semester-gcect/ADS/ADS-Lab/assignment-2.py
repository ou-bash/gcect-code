import random
import matplotlib.pyplot as plt


# ============================================================
# 1. MERGE SORT WITH COMPARISON COUNTING
# ============================================================

def merge_sort(arr):
    """
    Sorts the array using Merge Sort.

    Returns:
        sorted_array
        number_of_comparisons
    """

    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2

    left, left_comparisons = merge_sort(arr[:mid])
    right, right_comparisons = merge_sort(arr[mid:])

    merged = []
    i = 0
    j = 0
    comparisons = left_comparisons + right_comparisons

    while i < len(left) and j < len(right):

        # One comparison between two array elements
        comparisons += 1

        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, comparisons


# ============================================================
# 2. LINEAR SEARCH WITH COMPARISON COUNTING
# ============================================================

def linear_search(arr, target):
    """
    Performs Linear Search.

    Returns:
        number_of_comparisons
    """

    comparisons = 0

    for element in arr:

        # Compare current element with target
        comparisons += 1

        if element == target:
            return comparisons

    return comparisons


# ============================================================
# 3. BINARY SEARCH WITH COMPARISON COUNTING
# ============================================================

def binary_search(arr, target):
    """
    Performs Binary Search on a sorted array.

    Returns:
        number_of_comparisons
    """

    low = 0
    high = len(arr) - 1
    comparisons = 0

    while low <= high:

        mid = (low + high) // 2

        # Compare middle element with target
        comparisons += 1

        if arr[mid] == target:
            return comparisons

        # Second element comparison
        comparisons += 1

        if target < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return comparisons


# ============================================================
# 4. EXPERIMENT
# ============================================================

N_VALUES = [1000, 5000, 10000]

M_VALUES = [1, 1000, 5000, 8000, 10000]

REPETITIONS = 1000


def run_experiment(n, m):

    linear_total = 0
    binary_total = 0

    for _ in range(REPETITIONS):

        # ----------------------------------------------------
        # Generate random array
        # ----------------------------------------------------

        arr = [random.randint(1, n * 10) for _ in range(n)]

        # ----------------------------------------------------
        # Linear Search
        # ----------------------------------------------------

        linear_comparisons = 0

        for _ in range(m):

            target = random.randint(1, n * 10)

            linear_comparisons += linear_search(arr, target)

        linear_total += linear_comparisons

        # ----------------------------------------------------
        # Binary Search
        # ----------------------------------------------------

        # Sort ONLY ONCE
        sorted_arr, sorting_comparisons = merge_sort(arr)

        binary_comparisons = sorting_comparisons

        # Perform m binary searches
        for _ in range(m):

            target = random.randint(1, n * 10)

            binary_comparisons += binary_search(
                sorted_arr,
                target
            )

        binary_total += binary_comparisons

    # --------------------------------------------------------
    # Calculate average
    # --------------------------------------------------------

    linear_average = linear_total / REPETITIONS
    binary_average = binary_total / REPETITIONS

    return linear_average, binary_average


# ============================================================
# 5. MAIN PROGRAM
# ============================================================

def main():

    results = {}

    for n in N_VALUES:

        print("\n======================================")
        print(f"n = {n}")
        print("======================================")

        linear_results = []
        binary_results = []

        for m in M_VALUES:

            print(
                f"Running n={n}, m={m} "
                f"({REPETITIONS} repetitions)..."
            )

            linear_avg, binary_avg = run_experiment(n, m)

            linear_results.append(linear_avg)
            binary_results.append(binary_avg)

            print(
                f"Linear  : {linear_avg:.2f}"
            )

            print(
                f"Binary  : {binary_avg:.2f}"
            )

        results[n] = {
            "linear": linear_results,
            "binary": binary_results
        }

    # ========================================================
    # 6. PRINT FINAL RESULTS
    # ========================================================

    print("\n\nFINAL RESULTS")
    print("=" * 80)

    for n in N_VALUES:

        print(f"\nn = {n}")

        print(
            f"{'m':>8}"
            f"{'Linear Search':>25}"
            f"{'Binary Search':>25}"
        )

        print("-" * 60)

        for i, m in enumerate(M_VALUES):

            print(
                f"{m:>8}"
                f"{results[n]['linear'][i]:>25.2f}"
                f"{results[n]['binary'][i]:>25.2f}"
            )

    # ========================================================
    # 7. CREATE THREE GRAPHS
    # ========================================================

    for n in N_VALUES:

        plt.figure(figsize=(8, 5))

        plt.plot(
            M_VALUES,
            results[n]["linear"],
            marker="o",
            label="Linear Search"
        )

        plt.plot(
            M_VALUES,
            results[n]["binary"],
            marker="o",
            label="Binary Search + Sorting"
        )

        plt.xlabel("Number of Searches (m)")
        plt.ylabel("Average Number of Comparisons")

        plt.title(
            f"Linear Search vs Binary Search (n = {n})"
        )

        plt.legend()
        plt.grid(True)

        plt.tight_layout()

        # Save graph
        plt.savefig(
            f"search_comparison_n_{n}.png"
        )

        plt.show()


# ============================================================
# 8. RUN
# ============================================================

if __name__ == "__main__":
    main()
