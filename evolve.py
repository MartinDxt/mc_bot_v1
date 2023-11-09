import matplotlib.pyplot as plt
import networkx as nx
import json
import pprint


def addlayer2chunk(chunk, size, inputlayers: list = [int],  #adds layers to existing chunks
                   a: list = [int],b: list = [int], c: int = 0,d: list = [int],  # a,b,c,d par of Izhikevich model
                   ei: list = [bool]):  # ei => Excitatory /inhibitory
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

    def add_input2chunk(self, node, fromchunk, fromlayer, tolayer): #add connetions to existing nodes
        chunk = self.chunks["chunks"][node]
        current_fn = chunk["input"]["from_node"]
        current_fl = chunk["input"]["from_layer"]
        current_lla_id = chunk["input"]["local_layer_assigned_id"]
        current_from = zip(current_fn, current_fl, current_lla_id)
        from_cl = zip(fromchunk, fromlayer, tolayer)
        for f_cl in from_cl:
            is_same_from = False
            lla_id = 0
            for cf in current_from:
                chunk_eq = cf[0] == f_cl[0]
                layer_eq = cf[1] == f_cl[1]
                if chunk_eq & layer_eq:
                    is_same_from = True
                    lla_id = cf[2]

            if is_same_from:
                pointer_lla_id = lla_id
            else:
                pointer_lla_id = min(current_lla_id) - 1
                chunk["input"]["from_node"].append(f_cl[0])
                chunk["input"]["from_layer"].append(f_cl[1])
                chunk["input"]["local_layer_assigned_id"].append(pointer_lla_id)

            chunk["layers"][f_cl[2]]["input_layers"].append(pointer_lla_id)

    def savetofile(self, new_file):
        #json_object = json.dumps(self.chunks, indent=2)
        pprint.pprint(self.chunks, compact=True)
        json_object = pprint.pformat(self.chunks, compact=True).replace("'",'"').replace("True",'true').replace("False",'false')
        # Writing to file
        with open(new_file, "w") as outfile:
            outfile.write(json_object)


B1 = Genome("brain-data.json")
chunk = B1.createnewchunk([0, 1], [0, 1], "test1")
chunk = addlayer2chunk(chunk, 64, [-2, 0, 1], [0.02, 0.015], [0.02, 0.015], -55, [4.1, 3.2], [False, True, False])
chunk = addlayer2chunk(chunk, 128, [-1, 0, 1], [0.02, 0.025], [0.01, 0.02], -65, [4, 3.5], [True, False, False])
B1.addchunk2brain(chunk)
B1.add_input2chunk(2,[3],[1], [1])
B1.savetofile("brain2.json")
