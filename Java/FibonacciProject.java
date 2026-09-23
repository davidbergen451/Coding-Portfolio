import java.util.HashMap;
import java.util.Map;

/**
 * =====================================================================
 *  FIBONACCI ALGORITHMS PROJECT
 *  A Java algorithms / computational-thinking demo project.
 *
 *  Concepts demonstrated:
 *   - Loops              (iterative Fibonacci, sequence building)
 *   - Recursion           (naive recursion, memoized recursion)
 *   - Iteration vs recursion trade-offs (timed comparison)
 *   - Computational thinking (perfect-square identity check,
 *                              Project-Euler-style problem solving)
 * =====================================================================
 */

/**
 * Encapsulates several ways of computing Fibonacci numbers.
 */
class FibonacciCalculator {

    /** Iterative approach: O(n) time, O(1) space. */
    public long fibonacciIterative(int n) {
        if (n <= 1) return n;
        long prev = 0, curr = 1;
        for (int i = 2; i <= n; i++) {
            long next = prev + curr;
            prev = curr;
            curr = next;
        }
        return curr;
    }

    /** Naive recursion: O(2^n) time. Simple but exponentially slow for large n. */
    public long fibonacciRecursive(int n) {
        if (n <= 1) return n;
        return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
    }

    /** Memoized recursion: O(n) time -- caches results to avoid repeated work. */
    public long fibonacciMemoized(int n, Map<Integer, Long> memo) {
        if (n <= 1) return n;
        if (memo.containsKey(n)) return memo.get(n);
        long result = fibonacciMemoized(n - 1, memo) + fibonacciMemoized(n - 2, memo);
        memo.put(n, result);
        return result;
    }

    /** Convenience overload that creates a fresh memo cache. */
    public long fibonacciMemoized(int n) {
        return fibonacciMemoized(n, new HashMap<>());
    }

    /** Builds the first `count` Fibonacci numbers into an array. */
    public long[] fibonacciSequence(int count) {
        long[] sequence = new long[count];
        for (int i = 0; i < count; i++) {
            sequence[i] = fibonacciIterative(i);
        }
        return sequence;
    }

    /**
     * Checks whether n is a Fibonacci number using the classic identity:
     * n is Fibonacci if and only if (5n^2 + 4) or (5n^2 - 4) is a perfect square.
     */
    public boolean isFibonacciNumber(long n) {
        return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4);
    }

    private boolean isPerfectSquare(long x) {
        if (x < 0) return false;
        long s = (long) Math.sqrt(x);
        return s * s == x || (s + 1) * (s + 1) == x;
    }

    /**
     * Sum of all even-valued Fibonacci numbers strictly below `limit`.
     * A classic Project-Euler-style problem-solving exercise.
     */
    public long sumOfEvenFibonacciBelow(long limit) {
        long sum = 0;
        long prev = 0, curr = 1;
        while (curr < limit) {
            if (curr % 2 == 0) {
                sum += curr;
            }
            long next = prev + curr;
            prev = curr;
            curr = next;
        }
        return sum;
    }
}

/**
 * Entry point. Demonstrates sequence building, a timed comparison of
 * the three Fibonacci strategies, and two small algorithmic puzzles.
 */
public class FibonacciProject {
    public static void main(String[] args) {
        FibonacciCalculator calc = new FibonacciCalculator();

        System.out.println("=== First 15 Fibonacci Numbers (iterative, stored in array) ===");
        long[] sequence = calc.fibonacciSequence(15);
        for (long num : sequence) {
            System.out.print(num + " ");
        }
        System.out.println("\n");

        int n = 35;
        System.out.println("=== Comparing approaches for n = " + n + " ===");

        long startIter = System.nanoTime();
        long resultIter = calc.fibonacciIterative(n);
        long endIter = System.nanoTime();
        System.out.println("Iterative:  " + resultIter + "  (" + (endIter - startIter) + " ns)");

        long startMemo = System.nanoTime();
        long resultMemo = calc.fibonacciMemoized(n);
        long endMemo = System.nanoTime();
        System.out.println("Memoized:   " + resultMemo + "  (" + (endMemo - startMemo) + " ns)");

        long startRec = System.nanoTime();
        long resultRec = calc.fibonacciRecursive(n);
        long endRec = System.nanoTime();
        System.out.println("Recursive:  " + resultRec + "  (" + (endRec - startRec) + " ns)");
        System.out.println("(Notice how plain recursion gets dramatically slower as n grows --");
        System.out.println(" this is the classic lesson in exponential vs linear time complexity.)");

        System.out.println("\n=== Is-Fibonacci check ===");
        int[] testNumbers = {13, 15, 21, 100, 144};
        for (int num : testNumbers) {
            System.out.println(num + " is Fibonacci? " + calc.isFibonacciNumber(num));
        }

        System.out.println("\n=== Sum of even Fibonacci numbers below 4,000,000 ===");
        System.out.println(calc.sumOfEvenFibonacciBelow(4_000_000));
    }
}
