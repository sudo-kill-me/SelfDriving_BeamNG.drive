import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui

# User imported modules
from direct_keys import UP, DOWN, LEFT, RIGHT
from find_lanes import process_screen_canny_edge


def main():
    while True:
        screen = np.array(ImageGrab.grab(bbox=(3, 42, 958, 737)))
        '''
        Returns detected lanes.
        - print_slope is a boolean variable
            If true, slope will be printed in console.
            If false, slope won't be printed.
        - show_raw_processing
            If true, screen will be shown as raw canny image.
            If false, screen will just overlay lanes on original screen.
        - detected_lane_color
            Color of overlay lane color. raw canny image defaults to white.
            0 - white, 1 - blue, 2 - red, 3 - green
        - debug_mode
            If true, will print any debug messages.
            If false, will keep console clean.
        '''
        canny_screen = process_screen_canny_edge(screen,
                                                 print_slope=False,
                                                 show_raw_image=False,
                                                 detected_lane_color=3,
                                                 debug_mode=True)
        # TODO - Add logic to self drive by staying within lane

        cv2.imshow('BeamNG_Drive_Window Lane Detection', canny_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
