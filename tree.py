from math import sin, cos, tan, pi, atan2
import cairo
import random

class Tree(object):
	def __init__(self, tree_levels, starting_pos, init_children, max_branch_length):
		self.tree_levels = tree_levels
		self.starting_pos = starting_pos
		self.max_branch_length = max_branch_length
		self.init_children = init_children
		self.root_node = None
		self.build_tree()

	def get_child_pos(self, origin_pos):
		return Point(random.uniform(-1,1) * self.max_branch_length + origin_pos.x, 
			random.random() * self.max_branch_length + origin_pos.y)

	def build_tree(self):
		if self.tree_levels == 0:
			return TreeNode(self.starting_pos, True, [])

		children = []
		for i in range(0, self.init_children):
			child_pos = self.get_child_pos(self.starting_pos)
			# TODO: add function as argument to define child growth
			node = self.build_tree_helper(child_pos, self.tree_levels - 1, self.init_children + 1)
			children.append(node)

		self.root_node = TreeNode(self.starting_pos, False, children)

	def build_tree_helper(self, position, tree_levels, num_children):
		if tree_levels == 0:
			return TreeNode(position, True, [])

		children = []
		for i in range(0, num_children):
			child_pos = self.get_child_pos(position)
			node = self.build_tree_helper(child_pos, tree_levels - 1, num_children + 1)
			children.append(node)

		return TreeNode(position, False, children)

	def print_tree(self):
		self.print_tree_helper(self.root_node)

	def print_tree_helper(self, node):
		print "Node. X: ", node.pos.x, " Y: ", node.pos.y, " is leaf: ", node.is_leaf
		for child_node in node.children:
			self.print_tree_helper(child_node)

	def apply_transform(self):
		self.apply_transform_helper(self.root_node)

	def apply_transform_helper(self, node):
		new_pos = Point(random.uniform(-1,1) * 3 + node.pos.x, 
			random.uniform(-1,1) * 3 + node.pos.y)
		node.pos = new_pos
		for child in node.children:
			self.apply_transform_helper(child)

class TreeNode(object):
	def __init__(self, pos, is_leaf, children):
		self.pos = pos
		self.is_leaf = is_leaf
		self.children = children

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

# if __name__ == '__main__':
# 	tree_levels = 2
# 	starting_pos = Point(0,0)
# 	init_children = 2
# 	max_branch_length = 150
# 	tree = Tree(tree_levels, starting_pos, init_children, max_branch_length)
# 	tree.print_tree()