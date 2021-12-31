import networkx as nx
import numpy as np

import json
import io
from pathlib import Path

_USING_REMOTE_DB = False


class Config:
    def get_lineage_graph():
        lin = nx.json_graph.tree_graph(json.load(Config.LINEAGE_JSON_PATH.open()))
        # Relabel the nodes with the `name` attribute:
        return nx.relabel_nodes(lin, {n: a["name"] for n, a in lin.nodes(data=True)})

    def get_connectome(debug: bool = False):
        if _USING_REMOTE_DB:
            fh = io.BytesIO(
                MossDBClient("http://mossdb").get_file(
                    Config.CONNECTOME_GRAPHML_MOSS_URI
                )
            )
            c = nx.read_graphml(fh)
        else:
            c = nx.read_graphml(Config.CONNECTOME_GRAPHML_PATH)
        locations = Config.get_cell_locations_map()
        for n in c.nodes:
            try:
                c.nodes[n]["location"] = locations[n]
            except KeyError:
                if debug:
                    print(f"Could not find location for neuron [{n}].")
        return c

    def get_cell_locations_map():
        return json.load(open(Config.CELL_LOCATION_JSON_PATH, "r"))

    def distance_shortest_path(lineage: nx.DiGraph, source: str, target: str):
        """
        Return the shortest path distance between two nodes in a lineage graph.

        Arguments:
            lineage (nx.DiGraph): The target graph
            source (str): The source node
            target (str): The target node

        Returns:
            int: The shortest path distance between the source and target nodes

        """
        try:
            return nx.shortest_path_length(nx.Graph(lineage), source, target)
        except:
            return np.nan

    def distance_common_successors(connectome: nx.DiGraph, source: str, target: str):
        """
        Return the number of common successors between two nodes in a connectome graph.

        Arguments:
            connectome (nx.DiGraph): The target graph
            source (str): The source node
            target (str): The target node

        Returns:
            int: The number of common successors between the source and target nodes

        """
        try:
            return len(
                set(connectome.successors(source)).intersection(
                    connectome.successors(target)
                )
            )
        except Exception as e:
            return np.nan

    def distance_common_predecessors(connectome: nx.DiGraph, source: str, target: str):
        """
        Return the number of common predecessors between two nodes in a connectome graph.

        Arguments:
            connectome (nx.DiGraph): The target graph
            source (str): The source node
            target (str): The target node

        Returns:
            int: The number of common predecessors between the source and target nodes

        """
        try:
            return len(
                set(connectome.predecessors(source)).intersection(
                    connectome.predecessors(target)
                )
            )
        except Exception as e:
            return np.nan

    def distance_euclidean(
        connectome: nx.DiGraph, source: str, target: str, location_key: str = "location"
    ):
        """
        Return the euclidean distance between two neurons.

        Arguments:
            connectome (nx.DiGraph): The target graph
            source (str): The source node
            target (str): The target node

        Returns:
            float: The euclidean distance between the source and target nodes

        """
        try:
            return np.linalg.norm(
                np.array(connectome.nodes[source][location_key])
                - np.array(connectome.nodes[target][location_key])
            )
        except:
            return np.nan

    LINEAGE_JSON_PATH = Path("./data/bhatla-lineage.json")
    CONNECTOME_GRAPHML_MOSS_URI = (
        "file://graphs/witvliet2020/witvliet_2020_7_node_attributes"
    )
    CONNECTOME_GRAPHML_PATH = Path("./data/witvliet2021-Dataset8.graphml")
    CELL_LOCATION_JSON_PATH = Path("./data/locations.openworm2012.blender.json")

    FOLD_CONNECTOME = True

    LINEAGE_DISTANCE_METRIC = distance_shortest_path
    CONNECTOME_SIMILARITY_METRIC = distance_common_successors
    CONNECTOME_DISTANCE_METRIC = distance_euclidean

    COMPUTE_LINEAGE_DISTANCE_PARALLEL = True
    COMPUTE_CONNECTOME_SIMILARITY_PARALLEL = False
    COMPUTE_CONNECTOME_DISTANCE_PARALLEL = False


def fold_connectome(connectome: nx.DiGraph, prefer_side: str = "R") -> nx.DiGraph:
    """
    Merges all neurons in the connectome that have left (-L) and right (-R)
    counterparts into a single node.

    Arguments:
        connectome (nx.DiGraph): The connectome to fold.
        prefer_side (str: "R"): The side to prefer when folding.

    Returns:
        nx.DiGraph: The connectome with the neurons merged.

    """
    # Copy the connectome:
    connectome = connectome.copy()

    # Nodes either end in -L or -R:
    # We can collapse all *L into a *R.
    # If the user prefers "L", then collapse all *R into *L.

    non_preferred_side = "L" if prefer_side == "R" else "R"
    for node in connectome.nodes():
        if (
            node.endswith(prefer_side)
            and f"{node[:-1]}{non_preferred_side}" in connectome
        ):
            # Collapse the two nodes:
            connectome = nx.contracted_nodes(
                connectome, node, f"{node[:-1]}{non_preferred_side}"
            )
    return connectome


def shuffle_connectome_renamed(connectome: nx.DiGraph) -> nx.DiGraph:
    """
    Shuffle the nodes of the connectome by randomly renaming them.

    Arguments:
        connectome (nx.DiGraph): The connectome to shuffle.

    Returns:
        nx.DiGraph: The shuffled connectome.

    """
    # Copy the connectome:
    connectome = connectome.copy()

    # Shuffle the nodes:
    nodes = list(connectome.nodes())
    np.random.shuffle(nodes)
    connectome = nx.relabel_nodes(
        connectome, dict(zip(list(connectome.nodes()), nodes))
    )

    return connectome
