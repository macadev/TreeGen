from math import sin, cos, tan, pi, atan2
import cairo

# starting coords
TREE_ROOT = (0,0)
TREE_TRUNK = (0,1)

# drawing constants
STROKE_COLOR = 0xFFFF00 # yellow
LINE_WIDTH = 1

# canvas constants
IMG_WIDTH = 1024
IMG_HEIGHT= 1024
SCALE = 64
BACKGROUND_COLOR = 0x000250 # black

def color(value):
    r = ((value >> (8 * 2)) & 255) / 255.0
    g = ((value >> (8 * 1)) & 255) / 255.0
    b = ((value >> (8 * 0)) & 255) / 255.0
    return (r, g, b)

class Canvas(object):
	def __init__(self, width=IMG_WIDTH, height=IMG_HEIGHT, scale=SCALE, background_color=BACKGROUND_COLOR, line_width=LINE_WIDTH):
		self.width = width
		self.height = height
		self.scale = scale
		self.surface = cairo.ImageSurface(
            cairo.FORMAT_RGB24, self.width, self.height)
		# context settings
		self.ctx = cairo.Context(self.surface)
		self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
		self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
		self.ctx.set_line_width(line_width)
		self.ctx.set_source_rgb(*color(background_color))
		self.ctx.paint()

def draw_tree(canvas, levels, num_branches):
	# Draw trunk at base of image
	canvas.ctx.set_source_rgb(1,1,1)
	canvas.ctx.move_to(0,0)
	canvas.ctx.line_to(512, 512)
	canvas.ctx.stroke()
	canvas.surface.write_to_png('out.png')

def main():
	canvas = Canvas()
	draw_tree(canvas, 10, 10)

if __name__ == '__main__':
	main()