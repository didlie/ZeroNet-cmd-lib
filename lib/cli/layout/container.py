from node import Node

class Container(Node):
	container = True
	text_container = False

	def __init__(self, children=[]):
		super(Container, self).__init__()

		if len(children) != 1:
			raise ValueError("<Container> can contain only one node")

		self.child = children[0]
		self.type = None

	def render(self, layout, dry_run=False):
		self.child.render_offset = self.render_offset
		self.child.render_boundary_left_top = self.render_boundary_left_top
		self.child.render_boundary_right_bottom = self.render_boundary_right_bottom
		self.child.render_stretch = self.render_stretch
		self.child.parent = self

		return self.child.render(layout, dry_run=dry_run)