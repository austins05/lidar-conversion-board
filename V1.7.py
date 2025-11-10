# This script reads Uart RS485 at 115200 Baud from a Lidar unit on pins 0 and 1 and 
# coverts it into RS232 9600 Baud and writes it to pins 4 and 5. The output is configured
# for use with Trackmap. Currently configured to use a Benawake TF03 Lidar unit.

import machine
import time

# Create a UART object for reading LIDAR on UART0 (GPIO0, GPIO1)
uart_lidar = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# Create a UART object for RS232 communication on UART1 (GPIO4, GPIO5) which goes to trackmap.
uart_rs232 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5),
                          bits=8, parity=None, stop=1)
                          
# The distance data from the lidar is contained in bits 2 and 3 of the 9 bit frame. 
# 2 is low and 3 is high, to calculate the distance you need to multiply the high x 256 
# and that offsets the bits to the left by 8, which is equal to (<<8). After that you 
# add the low to the high to get the full 16 bit distance reading. 

def get_distance(data):
    """Extract and calculate distance from the 9-byte data frame."""
    if data[0:2] == b'\x59\x59' and len(data) == 9:
        high_byte = data[3]
        low_byte = data[2]
        distance = (high_byte << 8) | low_byte
        return distance
    return None
    
# The TrackMap software wants the data in this format: 00005.56m <cr>.    

def format_distance(distance_cm):
    """Format the distance to the required string format with 2 decimal places."""
    if distance_cm is None:
        distance_cm = 99999  # Default error distance

    distance_m = distance_cm * 0.01  # Convert cm to meters
    distance_str = "{:08.2f}m\r".format(distance_m)  # Format to '00000.00m'
    return distance_str

# Target loop time in milliseconds for 9 Hz (111 ms) because TrackMap wants a 9HZ input signal
target_loop_time_ms = 20

while True:
    start_time = time.ticks_ms()  # Record the start time of the loop
    
    if uart_lidar.any():
        data = uart_lidar.read(9)
        distance_cm = get_distance(data)

        # Format and send the distance over UART1 (RS232)
        formatted_distance = format_distance(distance_cm)

        # Debug output to check what is being sent
        print(f"Sent (with carriage return): {formatted_distance + '\r'}")

        # Write formatted distance to UART1 (RS232)
        uart_rs232.write(formatted_distance)

    # Calculate elapsed time for the loop
    elapsed_time_ms = time.ticks_ms() - start_time

    # Sleep for the remainder of the target loop time (111 ms)
    if elapsed_time_ms < target_loop_time_ms:
       time.sleep_ms(target_loop_time_ms - elapsed_time_ms)

    # Optionally, you could print the loop time for debugging
    # print(f"Loop time: {elapsed_time_ms} ms")
