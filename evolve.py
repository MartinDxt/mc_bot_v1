import matplotlib.pyplot as plt
import networkx as nx
import json


def addlayer2chunk(chunk, size, inputlayers: list = [int], a: list = [int],
                   b: list = [int], c: int = 0,
                   d: list = [int],
                   ei: list = [bool]):
    if d is None:
        d = [0]
    if len(ei) != len(inputlayers):
        return 1
    layer = {"layer": len(chunk["layers"]),
             "size": size,
             "dynamics": {"a": a, "b": b, "c": c, "d": d},
             "input_layers": inputlayers,
             "exci_inhi": ei
             }
    chunk["layers"].append(layer)
    return chunk


class Genome:
    def __init__(self, file_name):
        self.file_name = file_name
        f = open(self.file_name)
        self.chunks = json.load(f)

    def createnewchunk(self, fromnode, fromlayer, name=""):
        if len(fromnode) != len(fromlayer):
            return 1
        chunk = {'id': len(self.chunks["chunks"]), 'name': name, "input": {
            "from_node": fromnode, "from_layer": fromlayer,
            "local_layer_assigned_id": [*range(-len(fromlayer), 0, 1)]}, "layers": []}
        return chunk

    def addchunk2brain(self, chunk):
        self.chunks["chunks"].append(chunk)

    def save2file(self, new_file):
        json_object = json.dumps(self.chunks, indent=2)
        # Writing to sample.json
        with open(new_file, "w") as outfile:
            outfile.write(json_object)


B1 = Genome("brain-data.json")
chunk = B1.createnewchunk([0, 1], [0, 1], "test1")
chunk = addlayer2chunk(chunk, 64, [-2, 0, 1], [0.02, 0.015], [0.02, 0.015], -55, [4.1, 3.2], [False, True, False])
chunk = addlayer2chunk(chunk, 128, [-1, 0, 1], [0.02, 0.025], [0.01, 0.02], -65, [4, 3.5], [True, False, False])
B1.addchunk2brain(chunk)
B1.save2file("brain2.json")