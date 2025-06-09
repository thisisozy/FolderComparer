import os
import argparse
from tqdm import tqdm # type: ignore
import hashlib


def main():
    args = parse_args()
    folder_one = args.folder_one
    folder_two = args.folder_two

    # Hash all files in both folders
    files_one = get_all_file_paths(folder_one)
    files_two = get_all_file_paths(folder_two)
    hashes_one = get_file_hashes(files_one, folder_one)
    hashes_two = get_file_hashes(files_two, folder_two)

    output_lines = []
    matched = set(hashes_one.keys()) & set(hashes_two.keys())
    only_in_one = set(hashes_one.keys()) - set(hashes_two.keys())
    only_in_two = set(hashes_two.keys()) - set(hashes_one.keys())

    # Check for unchanged and moved/renamed files
    unchanged = []
    moved_or_renamed = []
    for h in matched:
        paths_one = set(hashes_one[h])
        paths_two = set(hashes_two[h])
        for p1 in paths_one:
            if p1 in paths_two:
                unchanged.append((p1, p1))
            else:
                for p2 in paths_two:
                    moved_or_renamed.append((p1, p2))

    if unchanged:
        output_lines.append("Unchanged files:")
        output_lines.extend(f"  {p1}" for p1, _ in unchanged)
    if moved_or_renamed:
        output_lines.append("Moved or renamed files:")
        output_lines.extend(f"  {p1} -> {p2}" for p1, p2 in moved_or_renamed)
    if only_in_one:
        output_lines.append(f"Files only in {folder_one} (missing in {folder_two}):")
        for h in only_in_one:
            output_lines.extend(f"  {f}" for f in hashes_one[h])
    if only_in_two:
        output_lines.append(f"Files only in {folder_two} (missing in {folder_one}):")
        for h in only_in_two:
            output_lines.extend(f"  {f}" for f in hashes_two[h])
    if not output_lines:
        output_lines.append("All files are identical!")

    print_results(output_lines)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--folder_one", help="First parent folder.", required=True)
    parser.add_argument("-f2", "--folder_two", help="Second parent folder.", required=True)
    return parser.parse_args()


def get_all_file_paths(root_folder):
    file_paths = []
    for dirpath, _, files in os.walk(root_folder):
        for filename in files:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root_folder)
            file_paths.append(rel_path)
    return file_paths


def get_file_hashes(rel_paths, root_folder):
    hash_map = {}
    for rel_path in tqdm(rel_paths, desc=f"Hashing files in {root_folder}"):
        abs_path = os.path.join(root_folder, rel_path)
        h = hash_file(abs_path)
        if h not in hash_map:
            hash_map[h] = []
        hash_map[h].append(rel_path)
    return hash_map


def hash_file(path, block_size=65536):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def print_results(output_lines):
    output_path = os.path.join(os.getcwd(), "folder_compare_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
