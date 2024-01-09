import serial
import json

# Function to build and send a JSON command
def send_json_command(ser, cmd_num, **kwargs):
    """
    Builds a JSON command with the given command number and named arguments,
    then sends it over the provided serial connection.
    
    :param ser: The serial connection to use for sending the command.
    :param cmd_num: The command number (e.g., 1 for motor control).
    :param kwargs: Named arguments representing the command parameters.
    """
    # Build the JSON command object
    json_command = {"N": cmd_num}
    json_command.update(kwargs)
    
    # Convert JSON to string and encode it to bytes
    command_string = json.dumps(json_command)
    encoded_command = command_string.encode()
    
    # Write the encoded command to the serial connection
    ser.write(encoded_command)
    print(f"Sent command: {command_string}")  # Optional: print the command for debugging

# Example usage:
# Open serial connection (adjust 'COM3' and 9600 to match your settings)
ser = serial.Serial('COM3', 9600, timeout=1)

# Send a motor control command (N 1)
send_json_command(ser, 1, D1=0, D2=255, D3=1)

# Send a car control time-limited command (N 2)
send_json_command(ser, 2, D1=0, D2=128, T=5000)

# Send a lighting control no time-limited command (N 8)
send_json_command(ser, 8, D1=1, D2=255, D3=255, D4=255)

# Close the serial connection
ser.close()