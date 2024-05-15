import serial
import time

# Function to initialize the serial connection
def init_serial_connection(port='/dev/ttyUSB0', baudrate=9600):
    try:
        arduino = serial.Serial(port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Give time for Arduino's reset and bootloader
        return arduino
    except Exception as e:
        print(f"Failed to connect to Arduino on {port} with baudrate {baudrate}: {str(e)}")
        return None

# Function to send roll commands to the Arduino
def send_roll_command(arduino, command):
    if not arduino:
        print("Serial connection not established.")
        return

    try:
        print(f"Sending command: {command}")  # Debug print
        arduino.write(f"{command}\n".encode())
        time.sleep(0.5)  # Give time for Arduino to process the command

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Main function
def main():
    arduino = init_serial_connection('/dev/ttyUSB0', 9600)  # Adjust your port here
    if arduino:
        print("Starting servo control...")
        try:
            while True:
                command = input("Enter command ('l' for LEFTROLL, 'r' for RIGHTROLL, 's' for STOP, 'q' to quit): ")
                if command == 'l':
                    print("Rolling Left...")
                    send_roll_command(arduino, 1)  # Send LEFTROLL command (1)
                elif command == 'r':
                    print("Rolling Right...")
                    send_roll_command(arduino, 2)  # Send RIGHTROLL command (2)
                elif command == 's':
                    print("Stopping...")
                    send_roll_command(arduino, 0)  # Send STOP command (0)
                elif command == 'q':
                    print("Exiting...")
                    break
                else:
                    print("Invalid command.")
        finally:
            arduino.close()
            print("Servo control ended.")

if __name__ == "__main__":
    main()
