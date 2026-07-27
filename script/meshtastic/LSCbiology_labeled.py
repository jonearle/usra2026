import csv

TRACEROUTE_FILE = "separated_traceroutes.csv"
STDOUT_FILE = "/Users/Jon/usra2026/data/traceroutes/output.txt"
OUTPUT_FILE = "labeled_traceroutes.csv"

# Repeating destination order
DESTINATION_ORDER = [
    ("dadfb0cc", 1),
    ("dadfb6c8", 2),
    ("6c73daa0", 3),
    ("dadfb03c", 4),
]


def get_successful_destination_ids(stdout_file):
    """
    Read every attempted traceroute from stdout.
    Return destination IDs for successful attempts only.
    """
    successful_ids = []

    with open(stdout_file, "r", encoding="utf-8") as file:
        attempt_number = 0

        for raw_line in file:
            line = raw_line.strip()

            if not line:
                continue

            destination, destination_id = DESTINATION_ORDER[
                attempt_number % len(DESTINATION_ORDER)
            ]

            if line == "Traceroute successful":
                successful_ids.append(destination_id)

            attempt_number += 1

    return successful_ids


def read_traceroute_groups(csv_file):
    """
    Read blank-row-separated traceroute groups.

    Input rows may contain:
        fromNode,toNode
    or:
        fromNode,toNode,SNR
    """
    groups = []
    current_group = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            # Blank row means the current traceroute is complete.
            if not row or all(not cell.strip() for cell in row):
                if current_group:
                    groups.append(current_group)
                    current_group = []
                continue

            if len(row) < 2:
                print(f"Skipping invalid row: {row}")
                continue

            from_node = row[0].strip()
            to_node = row[1].strip()

            current_group.append((from_node, to_node))

    # Handle the final group if there is no trailing blank row.
    if current_group:
        groups.append(current_group)

    return groups


def write_labeled_traceroutes(groups, destination_ids, output_file):
    if len(groups) != len(destination_ids):
        raise ValueError(
            f"Found {len(groups)} traceroute groups, but stdout contains "
            f"{len(destination_ids)} successful traceroutes."
        )

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["destinationID", "fromNode", "toNode"])

        for group, destination_id in zip(groups, destination_ids):
            for from_node, to_node in group:
                writer.writerow([destination_id, from_node, to_node])

            # Blank row between traceroutes
            writer.writerow([])


def main():
    destination_ids = get_successful_destination_ids(STDOUT_FILE)
    traceroute_groups = read_traceroute_groups(TRACEROUTE_FILE)

    write_labeled_traceroutes(
        traceroute_groups,
        destination_ids,
        OUTPUT_FILE
    )

    print(f"Successful destinations found: {len(destination_ids)}")
    print(f"Traceroute groups found: {len(traceroute_groups)}")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
