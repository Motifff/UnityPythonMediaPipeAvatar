import threading
from body import BodyThread
import global_vars
import time
import cv2
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    global_vars.KILL_THREADS = True
    sys.exit(0)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize global variables
    global_vars.KILL_THREADS = False
    global_vars.DEBUG = True
    global_vars.CAM_INDEX = 0
    global_vars.USE_CUSTOM_CAM_SETTINGS = False
    global_vars.MODEL_COMPLEXITY = 1
    global_vars.USE_LEGACY_PIPES = False
    global_vars.HOST = "127.0.0.1"
    global_vars.PORT = 52733

    # Create and start body tracking thread
    body_thread = BodyThread()
    body_thread.daemon = True
    body_thread.start()

    # Main display loop
    try:
        while not global_vars.KILL_THREADS:
            if global_vars.DEBUG:
                image = body_thread.get_latest_image()
                if image is not None:
                    # Calculate new width while maintaining aspect ratio
                    height = 480
                    aspect_ratio = image.shape[1] / image.shape[0]
                    width = int(height * aspect_ratio)
                    
                    # Resize image
                    display_image = cv2.resize(image, (width, height))
                    #cv2.imshow('Body Tracking', display_image)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                global_vars.KILL_THREADS = True
                break
                
            time.sleep(0.01)  # Small delay to prevent CPU overload
            
    except KeyboardInterrupt:
        global_vars.KILL_THREADS = True
        
    # Cleanup
    cv2.destroyAllWindows()
    body_thread.join(timeout=1.0)

if __name__ == "__main__":
    main()