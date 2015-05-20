import pygraphviz as pgv
import xml.etree.ElementTree as ET

class node:
	
	def __init__(self, name):
		self.id_num = count
		self.name = name
		self.input_tags = []
		self.output_tags = []
	
	def add_input_tags(self, input_tags):
		for tag in input_tags:
			self.input_tags.append(tag)

	def add_output_tags(self, output_tags):
		for tag in output_tags:
			self.output_tags.append(tag)

G=pgv.AGraph()
tree = ET.parse('config.xml')

root = tree.getroot()
nodes = []
tags = []
count = 0

G.edge_attr['dir'] = 'forward'

#get name, inputTags, and outputTags of each loaded module
for child in root:
	count += 1

	#add new node to nodelist and graph
	n = node(child.attrib['type'])
	G.add_node( n.name +' '+ str(count), id=count)

	print(child.attrib['type'])

	for gc in child:
		if 'inputTags' in gc.attrib['name']:
			in_tags = gc.attrib['value']
			in_tags = in_tags.split(',')
			n.add_input_tags(in_tags)
			print('inputTags: ', gc.attrib['value'])

			for tag in in_tags:
				if not tag in tags:
					tags.append(tag)

		if 'outputTags' in gc.attrib['name']:
			out_tags = gc.attrib['value']
			out_tags = out_tags.split(',')
			n.add_output_tags(out_tags)
			print('outputTags: ', gc.attrib['value'])

			for tag in out_tags:
				if not tag in tags:
					tags.append(tag)
	nodes.append(n)

for a in nodes:
	print(a.name)
	print(a.input_tags)
	print(a.output_tags)

#generates a list of edges
for a in nodes:
	for b in nodes:
		for tag in a.output_tags:
			if tag in b.input_tags:
				print(tag, ' from ', a.name, '(', a.id_num, ') to ', b.name, '(', b.id_num,')')
				G.add_edge(a.name +' '+ str(a.id_num), b.name +' '+ str(b.id_num), label=tag)

G.draw('graph.png', prog='dot')
		
