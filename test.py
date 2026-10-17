
import subprocess
import sys
import unittest
from pathlib import Path

# Main program file
MAIN_SCRIPT = Path(__file__).with_name("transportation_scheduing.py")

# Sample transportation problem
# Cost matrix: [[4, 8, 6], [7, 5, 9]]
# Demands: [15, 25]
# Supplies: [10, 20, 10]

BASE_INPUTS = [
    "1",  # Transportation
    "2",  # Number of demands
    "3",  # Number of supplies
    "4", "8", "6",
    "7", "5", "9",
    "15", "25",  # Demands
    "10", "20", "10"  # Supplies
]


def print_output(title, result):
    """Print the complete output from the main program."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print("\nSTANDARD OUTPUT:")
    print(result.stdout)

    if result.stderr:
        print("\nERROR / WARNING OUTPUT:")
        print(result.stderr)


def run_program(method):
    """Run the main program for a selected transportation method."""
    inputs = BASE_INPUTS + [str(method)]

    result = subprocess.run(
        [sys.executable, str(MAIN_SCRIPT)],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        timeout=30
    )

    print_output(f"TRANSPORTATION METHOD {method}", result)

    return result


class TestTransportationProgram(unittest.TestCase):

    def test_northwest_method(self):
        result = run_program(1)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "Northwest method solution:",
            result.stdout
        )
        self.assertIn(
            "Total transportation cost (Northwest):",
            result.stdout
        )

    def test_least_cost_method(self):
        result = run_program(2)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "Least cost method solution:",
            result.stdout
        )
        self.assertIn(
            "Total transportation cost (Least Cost):",
            result.stdout
        )

    def test_vogel_method(self):
        result = run_program(3)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "Vogel's approximation method solution:",
            result.stdout
        )
        self.assertIn(
            "Total transportation cost (VAM):",
            result.stdout
        )

    def test_lowest_cost_comparison(self):
        result = run_program(4)

        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertIn(
            "Northwest method total cost:",
            result.stdout
        )
        self.assertIn(
            "Least cost method total cost:",
            result.stdout
        )
        self.assertIn(
            "Vogel's approximation method total cost:",
            result.stdout
        )
        self.assertIn(
            "Lowest-cost method:",
            result.stdout
        )
        self.assertIn(
            "Lowest transportation cost:",
            result.stdout
        )

    def test_unbalanced_problem(self):
        inputs = BASE_INPUTS.copy()

        # Change second demand from 25 to 26.
        # Total demand = 41; total supply = 40.
        inputs[10] = "26"

        result = subprocess.run(
            [sys.executable, str(MAIN_SCRIPT)],
            input="\n".join(inputs) + "\n",
            capture_output=True,
            text=True,
            timeout=30
        )

        print_output("UNBALANCED TRANSPORTATION PROBLEM", result)

        self.assertIn(
            "Total demand and total supply are not equal",
            result.stdout
        )

    def test_hungarian_scheduling(self):
        # Hungarian Method assignment problem
        # Cost matrix:
        # [[9, 2, 7],
        #  [6, 4, 3],
        #  [5, 8, 1]]

        inputs = [
            "2",  # Select scheduling / Hungarian Method
            "3",  # Number of jobs
            "3",  # Number of machines
            "9", "2", "7",
            "6", "4", "3",
            "5", "8", "1"
        ]

        result = subprocess.run(
            [sys.executable, str(MAIN_SCRIPT)],
            input="\n".join(inputs) + "\n",
            capture_output=True,
            text=True,
            timeout=30
        )

        print_output("HUNGARIAN SCHEDULING", result)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Scheduling selected.", result.stdout)
        self.assertIn("After row reduction:", result.stdout)
        self.assertIn("After column reduction:", result.stdout)
        self.assertIn("Optimal assignment:", result.stdout)
        self.assertIn(
            "Minimum total assignment cost:",
            result.stdout
        )

        # Expected optimal assignment cost for the sample matrix is 9.
        self.assertRegex(
            result.stdout,
            r"Minimum total assignment cost:\s*9(?:\.0+)?"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
