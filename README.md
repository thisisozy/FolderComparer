# FolderComparer

FolderComparer is a Python script that compares the contents of two folders, providing a detailed report of all differences. It automatically detects files that are identical, files that have been moved or renamed, and files that are missing in either folder. This makes it ideal for verifying backups, synchronizing directories, or tracking changes in large file collections.

## Features
- **Content-based comparison:** Files are compared by their content using SHA256 hashes, not just by name or location.
- **Detects moved/renamed files:** If a file exists in both folders but with a different path or name, it is reported as moved or renamed.
- **Reports missing files:** Any files present in one folder but not the other are listed.
- **Clear output:** Results are saved to `folder_compare_results.txt` in the script's directory.

## Usage
1. Place your folders to compare anywhere on your system.
2. Run the script from the command line:

```
powershell
python main.py -f1 <path_to_first_folder> -f2 <path_to_second_folder>
```

Replace `<path_to_first_folder>` and `<path_to_second_folder>` with the paths to your folders.

## Output
- The script will create a file named `folder_compare_results.txt` in the current working directory.
- This file will contain:
  - Unchanged files (same content and path)
  - Moved or renamed files (same content, different path)
  - Files missing in either folder

## Requirements
- Python 3.6+
- tqdm (`pip install tqdm`)

## Example
```
powershell
python main.py -f1 test/flat_folder -f2 test/flat_missing_pic_folder
```

## Notes
- The script compares all files recursively in both folders.
- Large folders may take some time to process due to hashing.
- Only file content is used for matching; file metadata (like modification time) is ignored.

---

Feel free to modify or extend the script for your specific needs!
