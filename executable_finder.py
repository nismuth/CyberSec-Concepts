# This program scans a subdirectory or scans a parent directory recursively for .exe files (with keyword option)

from pathlib import Path  # Specifically imports process for library paths

choice_path = input("\nEnter the folder path you'd like to scan: ")  # Asks for target directory
print("\nThanks, this might take a bit...")
directory = Path(choice_path)  # Takes the choice path and runs it through the imported pathfinder function

exe_files = []  # Creates a list to keep track of all the .exe file(s) from your target directory/subdirectory

for file in directory.rglob("*.exe"):  # Collecting all files with the .exe suffix -> * = all names with it
    if file.is_file():  # Takes all existing .exe files
        exe_files.append(file)  # Adds all those .exe files to the list that was just made

print(f"\nFound {len(exe_files)} executable(s).")  # The {len()} provides the statement with the number of found files

scan_key_option = input(
    "\nIs there any specific keyword you want to find? (Y/N): "
).strip().upper()  # Takes keyword Y/N input and automatically strips any whitespace AND uppercase's it

while scan_key_option not in ("Y", "N"):  # Error process for whenever the user doesn't enter Y or N
    print("\nError: Please enter either Y or N.")  # Repeats until the Y or N is received
    scan_key_option = input("(Y/N): ").strip().upper()  # Again to make sure the taken string is Y or N exactly

if scan_key_option == "Y":  # This if statement runs when the user wants to find files using a keyword
    keyword = input("\nEnter a keyword to search for: ").lower()  # Takes keyword and lowercase's it

    matches = []  # Creates list for files that contain the keyword

    for exe in exe_files:  # Creates var for every element in the exe_files list
        if keyword in exe.name.lower():  # Searches just the filename
            matches.append(exe)  # Adds filenames with keyword to matches list

    if matches:  # If matches are found then they're shown to the user
        print("\nMatches:")
        for exe in matches:
            print(exe)
    else:  # If no matches are found then the following error is displayed
        print("No matching executables found.")

if scan_key_option == "N":  # Exits the program if the user does not want to search by keyword
    print("\nGoodbye.")