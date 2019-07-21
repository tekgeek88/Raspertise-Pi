# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text",
            help="The text to scroll on the RGB LED panel",
            default="Loading...")


    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/10x20.bdf")
        my_red = self.args.red
        my_green = self.args.green
        my_blue = self.args.blue
        textColor = graphics.Color(my_red, my_green, my_blue)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:

            # If list is empty display the devices ip address

            # Fetch a list of advertisements to display

            # While there are still advertisements to display

                # Pop the next ad and display it

            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
