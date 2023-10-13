import time
import numpy
import matplotlib.pyplot as plt
import networkx as nx
import json


class GrayMatter:  # weights dynamics size dimensions state/output imput step curr_iteration
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.iteration = 0

    def step(self): #placeholder for iteration details
        self.iteration +=1
        return 0

    def getiteration(self):
        return self.iteration



class WhiteMatter:
    def __init__(self, json_brainfile):
        self.gray_matter  = []
        bf = open(json_brainfile)
        self.brain_data = json.load(bf)
        self.connectome = nx.MultiDiGraph()
        for chunks in self.brain_data['chunks']:
            self.gray_matter.append(GrayMatter(chunks['name'], chunks['id']))
            self.connectome.add_node(chunks['id'])
            for i in chunks['input']['from_node']:
                self.connectome.add_edge(chunks['id'], i)
                #print(chunks['id'], i)

    def getregionlist(self):
        return self.gray_matter

    def getconnectome(self):
        return self.connectome

    def stepall(self):
        for region in self.gray_matter:
            region.step()


filename = "brain-data.json"
brain1 = WhiteMatter(filename)

graymater = brain1.getregionlist()
brain1.stepall()
for i in graymater:
    print(i.getiteration())

brain_graph = brain1.getconnectome()
fig = plt.figure()
nx.draw(brain_graph, with_labels=True)
plt.show()
