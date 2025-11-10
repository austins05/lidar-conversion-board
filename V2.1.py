# --------------------------------------------------
#  Project: Lidar to tracmap
#  Version: V2.1
#  Author: Austin
#  Status: Working... until someone touches it. Most recent
#  This code has been changed! It has a loop that checks if the hieght is about 580 ft and if it is it sends the last data under 580 ft.
# --------------------------------------------------


import machine
import time

# UART0 for TF03 LiDAR (115200 baud)
uart_lidar = machine.UART(0, baudrate=115200, tx=0, rx=1, bits=8, parity=None, stop=1)
# UART1 for RS232 to TrackMap (9600 baud, 8N1)
uart_rs232 = machine.UART(1, baudrate=9600, tx=4, rx=5, bits=8, parity=None, stop=1)

def get_distance(data):
    """Extract distance from a 9-byte TF03 frame."""
    if data and len(data) >= 9 and data[0:2] == b'\x59\x59':
        high_byte = data[3]
        low_byte = data[2]
        distance = (high_byte << 8) | low_byte
        return distance
    return None

def format_distance(distance_cm):
    """Format to exactly '00005.45m\r' (10 bytes) for TrackMap."""
    if distance_cm is None or distance_cm > 99999:  # Cap at 999.99m
        distance_cm = 99999
    distance_m = distance_cm * 0.01  # cm to m
    formatted = "{:08.2f}m\r".format(distance_m)  # Always 00005.45m\r
    if len(formatted) != 10:  # Double-check length
        return "99999.99m\r"  # Fallback if malformed
    return formatted

target_loop_time_ms = 111  # 9 Hz for TrackMap
last_distance_cm = 99999  # Default in case of read failure
start_program = time.ticks_ms()  # For absolute timestamps
frame_count = 0  # Track TF03 frames
sent_count = 0  # Track sent frames

# Reset TF03 to 100 Hz (just in case)
uart_lidar.write(b'\x59\x59\x06\x01\x00\x00\x00\x00\x5F')  # 100 Hz
time.sleep(1)

while True:
    start_time = time.ticks_ms()
    
    # Read the freshest TF03 frame
    raw_distance_cm = None
    if uart_lidar.any():
        uart_lidar.read()  # Discard old data
        time.sleep_ms(10)
        data = uart_lidar.read(9)
        if data:
            frame_count += 1
            print(f"[{time.ticks_ms() - start_program} ms] Frame {frame_count} | Raw TF03: {data}")
            raw_distance_cm = get_distance(data)

    # Start with last known good value
    distance_cm = last_distance_cm

    # If a new reading came in, sanity-check it
    if raw_distance_cm is not None:
        distance_m = raw_distance_cm * 0.01
        if distance_m <= 176.784:
            distance_cm = raw_distance_cm
            last_distance_cm = raw_distance_cm  # Only update if good

    # Format and send
    formatted_distance = format_distance(distance_cm)
    uart_rs232.write(formatted_distance)
    uart_rs232.flush()
    sent_count += 1

    elapsed_time_ms = time.ticks_ms() - start_time
    total_time_ms = time.ticks_ms() - start_program
    print(f"[{total_time_ms} ms] Sent {sent_count}: {formatted_distance.strip()} | Loop time: {elapsed_time_ms} ms")

    if elapsed_time_ms < target_loop_time_ms:
        time.sleep_ms(target_loop_time_ms - elapsed_time_ms)
    else:
        print(f"Warning: Loop overrun by {elapsed_time_ms - target_loop_time_ms} ms")
