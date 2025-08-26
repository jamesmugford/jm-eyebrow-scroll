#!/usr/bin/env python3
import subprocess
import time

def test_scroll(direction="down", repeat=1, delay=1):
    print(f"Testing scroll {direction} x{repeat} with delay {delay}ms...")
    try:
        result = subprocess.run(
            ["xdotool", "click", "--repeat", str(repeat), "--delay", str(delay), direction],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Success!")
        else:
            print(f"Error (code {result.returncode}):")
            if result.stderr:
                print(result.stderr)
    except Exception as e:
        print(f"Exception: {e}")

print("XDoTool Scroll Test")
print("-" * 40)

# Test 1: Basic scroll down
print("\nTest 1: Single scroll down")
test_scroll("down", 1, 1)
time.sleep(1)

# Test 2: Basic scroll up
print("\nTest 2: Single scroll up")
test_scroll("up", 1, 1)
time.sleep(1)

# Test 3: Multiple scrolls
print("\nTest 3: Multiple scrolls down")
test_scroll("down", 3, 100)
time.sleep(1)

# Test 4: Fast scrolls
print("\nTest 4: Fast multiple scrolls up")
test_scroll("up", 5, 10)
time.sleep(1)

# Test 5: Mouse button numbers
print("\nTest 5: Using button numbers")
for button in [4, 5]:  # 4 = scroll up, 5 = scroll down
    print(f"\nTesting button {button}")
    try:
        subprocess.run(["xdotool", "click", "--repeat", "1", "--delay", "1", str(button)],
                      capture_output=True, text=True, check=True)
        print("Success!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
    time.sleep(0.5)

print("\nTest complete!")
