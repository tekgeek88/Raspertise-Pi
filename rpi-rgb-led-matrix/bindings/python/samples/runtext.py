# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import my_db_utils
import utils
import sys


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text",
                                 help="The text to scroll on the RGB LED panel",
                                 default="Loading...")

    def run(self):

        # Get local ip address on network
        ipaddr = utils.get_local_ip_addr()
        # Generate the message that is displayed in between advertisements
        DEFAULT_MESSAGE = "To sponsor an advertisement on this board login to https://" + ipaddr + ":5001"
        # Set the desired font
        font = graphics.Font()
        font.LoadFont("../../../fonts/10x20.bdf")

        # The list we will use to fetch and pop advertisements from the running web app
        ads = list()
        speed = 3
        while True:
            # If the ad list is empty refill it with new ads from the database
            # Then display the devices ip address to allow users to connect and purchase ads
            if not ads:
                ads = my_db_utils.get_ads()
                text = DEFAULT_MESSAGE
                text_color = graphics.Color(51, 0, 111)  # Default Color is UW purple
                speed = 3
            # If there are ads lets pop one off and display it
            else:
                advertisement = ads.pop(0)
                text = advertisement['message']
                speed = advertisement['speed']
                red, green, blue = tuple(map(int, advertisement['color'].split(",")))
                text_color = graphics.Color(red, green, blue)
            # Draw the text to the matrix panel
            self.draw_ad(font, text_color, text, speed)

    def draw_ad(self, font, text_color, text, speed=3):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        pos = offscreen_canvas.width
        # Scroll speed values are 1 - 5 steps
        base_speed = 0.085
        speed_step = 0.015
        scroll_speed = base_speed - speed * speed_step
        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 22, text_color, text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            # Wait time before shifting pixels and re-drawing
            time.sleep(scroll_speed)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            # If the cursor is at the begging of the line
            if pos == 64:
                break


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
