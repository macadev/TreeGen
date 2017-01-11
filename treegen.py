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

	def push_data_to_draw_stack(self, animation_data):
		self.draw_stack.append(animation_data)

	def draw_children(self):
		animation_data = self.draw_stack.pop()
		
		if animation_data.level == 0:
			self.ctx.save()
			self.ctx.translate(animation_data.parent_coord.x, animation_data.parent_coord.y)
			self.ctx.set_source_rgb(*get_random_leaf_color()) # Set leaf color
			self.ctx.move_to(0, 0)
			draw_leaf(self)
			self.ctx.fill()
			self.ctx.restore()
			return

		child_pos = animation_data.children_coords.pop()
		
		self.ctx.set_source_rgb(*color(TREE_COLOUR))
		self.ctx.move_to(animation_data.parent_coord.x, animation_data.parent_coord.y)
		self.ctx.line_to(child_pos.x, child_pos.y)
		self.ctx.stroke()
		
		new_children = []
		if animation_data.level - 1 != 0:
			new_children = get_children_coords(child_pos, animation_data.num_children + 1)
		new_animation_data = AnimationData(child_pos, new_children, animation_data.level - 1, animation_data.num_children + 1)
		
		if len(animation_data.children_coords) != 0:
			self.push_data_to_draw_stack(animation_data)
		self.push_data_to_draw_stack(new_animation_data)

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
		children_coords = get_children_coords(parent_coord, num_children)
		self.push_data_to_draw_stack(AnimationData(parent_coord, children_coords, tree_levels, num_children))

		counter = 1
		while len(self.draw_stack) != 0:
			self.draw_children()
			self.surface.write_to_png('out' + str(counter) + '.png')
			counter = counter + 1

	def draw(self):
		pass

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class AnimationData(object):
	def __init__(self, parent_coord, children_coords, level, num_children):
		self.parent_coord = parent_coord
		self.children_coords = children_coords
		self.level = level
		self.num_children = num_children

def get_random_leaf_color():
	return color(random.choice(LEAF_COLOURS))

def get_random_point(parent_coord):
	return Point(random.uniform(-1,1) * 150 + parent_coord.x, random.random() * 150 + parent_coord.y)

def get_children_coords(parent_coord, num_children):
	children_coords = []
	for i in range(0, num_children):
		children_coords.append(get_random_point(parent_coord))
	return children_coords

def draw_leaf(canvas):
	canvas.ctx.scale(random.uniform(0.3, 0.7), random.uniform(0.3, 0.7))
	canvas.ctx.arc(0, 0, 12, 0, 2 * pi)

def main():
	canvas = Canvas()
	canvas.pre_drawing_initialization()
	canvas.draw_tree_trunk()
	canvas.draw_tree(10, 10)

if __name__ == '__main__':
	main()
