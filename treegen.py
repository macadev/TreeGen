from math import sin, cos, tan, pi, atan2
import cairo
import random
# imports for animating
import pygtk
import gtk, gobject, cairo
from gtk import gdk

# starting coords
TREE_ROOT = (0,0)
TREE_TRUNK = (0,1)

# drawing constants
LINE_WIDTH = 0.8

# canvas constants
IMG_WIDTH = 1024
IMG_HEIGHT= 1024
SCALE = 64

# Colors
BACKGROUND_COLOUR = 0x000250 # Blue
TREE_COLOUR = 0xFFFFFF # White
LEAF_COLOURS = [0xF03A47, 0xD8343F, 0xC02E38] # Pastel red

def color(value):
    r = ((value >> (8 * 2)) & 255) / 255.0
    g = ((value >> (8 * 1)) & 255) / 255.0
    b = ((value >> (8 * 0)) & 255) / 255.0
    return (r, g, b)

class Canvas(object):
	def __init__(self, width=IMG_WIDTH, height=IMG_HEIGHT, scale=SCALE, background_colour=BACKGROUND_COLOUR, line_width=LINE_WIDTH):
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
		self.ctx.set_source_rgb(*color(background_colour))
		self.ctx.paint()

		# temporary data storage in between frames
		self.draw_stack = []

	def draw_children(self, parent_pos, num_children, level):
		self.ctx.save() # Save the current snapshot of transformations
		self.ctx.translate(parent_pos.x, parent_pos.y)
		if level == 0:
			self.ctx.stroke() # Draw the branch in white
			self.ctx.set_source_rgb(*get_random_leaf_color()) # Set leaf color
			draw_leaf(self)
			self.ctx.fill()
			self.ctx.set_source_rgb(*color(TREE_COLOUR))
			self.ctx.restore()
			# TICK()
			return
		children_coords = get_children_coords(num_children)
		for child_pos in children_coords:
			self.ctx.move_to(0, 0)
			self.ctx.line_to(child_pos.x, child_pos.y)
			# Recursively build the other branches
			# TICK()
			self.draw_children(child_pos, num_children + 1, level - 1)
		self.ctx.restore() # Restore the original coordinate system

	def pre_drawing_initialization(self):
		# Transform the coordinate system so that it's normal
		self.ctx.translate(0, 1024)
		self.ctx.scale(1, -1)

	def draw_tree_trunk(self):
		# Draw the tree trunk
		self.ctx.set_source_rgb(*color(TREE_COLOUR)) # Sets the line color to white
		self.ctx.move_to(512,0)
		self.ctx.line_to(512, 256)

	def draw_tree(self, levels, num_branches):
		parent_coord = Point(512, 256)
		tree_levels = 5
		num_children = 2
		self.draw_children(parent_coord, num_children, tree_levels)
		self.ctx.stroke()
		self.surface.write_to_png('out.png')

	def draw(self):
		pass

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class AnimationData(object):
	def __init__(self, children_coords, level):
		self.children_coords = children_coords
		self.level = level

def get_random_leaf_color():
	return color(random.choice(LEAF_COLOURS))

def get_random_point():
	return Point(random.uniform(-1,1) * 150, random.random() * 150)

def get_children_coords(num_children):
	children_coords = []
	for i in range(0, num_children):
		children_coords.append(get_random_point())
	return children_coords

def draw_leaf(canvas):
	# canvas.ctx.transform(get_shear_transform())
	canvas.ctx.scale(random.uniform(0.3, 0.7), random.uniform(0.3, 0.7))
	canvas.ctx.arc(0, 0, 12, 0, 2 * pi)

def main():
	canvas = Canvas()
	canvas.pre_drawing_initialization()
	canvas.draw_tree_trunk()
	canvas.draw_tree(10, 10)

if __name__ == '__main__':
	main()
