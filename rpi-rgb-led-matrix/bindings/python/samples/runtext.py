#!/usr/bin python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import math
import my_db_utils
import utils
import sys


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text",
                                 help="The text to scroll on the RGB LED panel",
                                 default="Loading...")
        self.parser.add_argument("-i", "--image", help="The image to display",
                                 default="uw_logo_final.ppm")

    def run(self):
        # Get local ip address on network
        ipaddr = utils.get_local_ip_addr()
        # Generate the message that is displayed in between advertisements
        DEFAULT_MESSAGE = "To sponsor a message on this board login to https://" + ipaddr + ":5001"
        font = graphics.Font()

        x = 2
        y = 20
        total_time = 10000
        period = 1000

        # The list we will use to fetch and pop advertisements from the running web app
        ads = list()
        while True:

            while not utils.is_server_listening():
                font.LoadFont("../../../fonts/tom-thumb.bdf")
                text_color = graphics.Color(0, 0, 255)  # Default Color is UW purple
                text = "Starting Server"
                self.dw(font, text_color, text, x, y, total_time, period)

            # Set the desired font
            font.LoadFont("../../../fonts/10x20.bdf")
            # If the ad list is empty refill it with new ads from the database
            # Then display the devices ip address to allow users to connect and purchase ads
            if not ads:
                ads = my_db_utils.get_ads()
                text = DEFAULT_MESSAGE
                text_color = graphics.Color(51, 0, 111)  # Default Color is UW purple
                speed = 3
                self.draw_uw_logo()
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

    def draw_text(self, font, text_color, text, x, y):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawText(offscreen_canvas, font, x, y, text_color, text)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def dw(self, font, text_color, text, x, y, total_time, period):
        start = period_start = int(round(time.time() * 1000))
        runtime = runtime_period = 0
        while runtime < total_time:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
            self.draw_text(font, text_color, text, x, y)
            end = int(round(time.time() * 1000))
            runtime = end - start
            runtime_period = end - period_start
            if runtime_period > period:
                offscreen_canvas.Clear()
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(period / 1000)
                period_start = int(round(time.time() * 1000))
                runtime_period = 0

    def draw_uw_logo(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size

        # let's scroll
        xpos = 0
        while True:
            xpos += 1
            if (xpos > img_width):
                break
            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + img_width)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.025)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
