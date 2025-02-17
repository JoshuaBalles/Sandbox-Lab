from pyngrok import ngrok
import subprocess
import time
import ctypes

# Windows constants for power management
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

def prevent_sleep():
    # Call SetThreadExecutionState to prevent sleep
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

def allow_sleep():
    # Restore default power management
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS)

# Start Jupyter Lab in the background
jupyter_process = subprocess.Popen(['jupyter', 'lab', '--no-browser', '--ip', '0.0.0.0'])

# Wait a few seconds for Jupyter to start
time.sleep(5)

try:
    # Prevent system from sleeping
    prevent_sleep()

    # Connect ngrok to port 8888 (default Jupyter port)
    url = ngrok.connect(8888)
    print(f'\nJupyter Lab is accessible at: {url}\n')
    print('Press Ctrl+C to stop the server')

    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up when Ctrl+C is pressed
    print('\nShutting down...')
    ngrok.disconnect(url)
    jupyter_process.terminate()

finally:
    # Restore default power management
    allow_sleep()