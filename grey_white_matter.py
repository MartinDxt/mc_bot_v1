import time
import numpy
import matplotlib.pyplot as plt
import networkx as nx
import json


class GreyMatter:  # weights dynamics size dimensions state/output imput step curr_iteration WIP
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.iteration = 0

    def step(self):  # placeholder for iteration details
        self.iteration += 1
        return 0

    def get_iteration(self):
        return self.iteration


class WhiteMatter:  # contains the connectome and manages the data transfer between the regions (GreyMatter) as well
    # as time stepping
    def __init__(self, json_brainfile):
        self.grey_matter = []
        bf = open(json_brainfile)
        self.brain_data = json.load(bf)
        self.connectome = nx.MultiDiGraph()
        for chunks in self.brain_data['chunks']:
            self.grey_matter.append(GreyMatter(chunks['name'], chunks['id']))
            for i in chunks['input']['from_node']:
                self.connectome.add_edge(i, chunks['id'])
                # print(chunks['id'], i)

    def get_region_list(self):
        return self.grey_matter

    def get_connectome(self):
        return self.connectome

    def step_all(self):
        for region in self.grey_matter:
            region.step()


filename = "brain2.json"
brain1 = WhiteMatter(filename)
grey_mater = brain1.get_region_list()
brain1.step_all()
for i in grey_mater:
    print(i.get_iteration())

brain_graph = brain1.get_connectome()
fig = plt.figure()
nx.draw(brain_graph, with_labels=True)
plt.show()
