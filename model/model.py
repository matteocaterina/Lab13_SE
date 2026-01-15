import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.DiGraph()

        self.lista_cromosomi = []
        self.lista_geni = []
        self.connessioni = {}

        self._nodes = []
        self._edges = []
        self.id_map = {}

        self.peso_ottimo = float('-inf')
        self.percorso = []


    def crea_grafo(self):
        self.lista_cromosomi = DAO.get_cromosomi()
        for cromosoma in self.lista_cromosomi:
            self._nodes.append(cromosoma)

        self.G.add_nodes_from(self._nodes)

        self.lista_geni = DAO.get_geni()
        for gene in self.lista_geni:
            self.id_map[gene.id] = gene.cromosoma

        self.connessioni = DAO.get_connessioni()
        edges = {}
        for g1, g2, peso in self.connessioni:
            if (self.id_map[g1], self.id_map[g2]) not in edges:
                edges[(self.id_map[g1], self.id_map[g2])] = float(peso)
            else:
                edges[(self.id_map[g1], self.id_map[g2])] += float(peso)

        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))

        self.G.add_weighted_edges_from(self._edges)


    def get_min_max(self):
        minimo = min(d['weight'] for _,_,d in self.G.edges(data=True))
        massimo = max(d['weight'] for _,_,d in self.G.edges(data=True))
        return minimo, massimo

    def conta_archi(self, soglia):
        minori = sum(1 for _,_,d in self.G.edges(data=True) if d['weight'] < soglia)
        maggiori = sum(1 for _,_,d in self.G.edges(data=True) if d['weight'] > soglia)
        return minori, maggiori


    def cammino_massimo(self, soglia):
        self.peso_ottimo = float('-inf')
        self.percorso = []
        for nodo in self.G.nodes():
            self._ricorsione([nodo], soglia, [], 0)

        return self.percorso, self.peso_ottimo


    def _ricorsione(self, parziale, soglia, edge_parziale, peso_corrente):
        ultimo_nodo = parziale[-1]
        vicini = self.get_vicini(ultimo_nodo,soglia, edge_parziale)

        if len(vicini)  == 0:
            if peso_corrente > self.peso_ottimo:
                self.peso_ottimo = peso_corrente
                self.percorso = edge_parziale.copy()
            return

        for v, w in vicini:
            edge_parziale.append((ultimo_nodo, v, self.G[ultimo_nodo][v]['weight']))
            parziale.append(v)
            self._ricorsione(parziale, soglia, edge_parziale, peso_corrente+ w)
            edge_parziale.pop()
            parziale.pop()

    def get_vicini(self, nodo, soglia, edge_parziale):
        result = []
        for v in self.G.successors(nodo):
            if (nodo, v) not in [(x[0], x[1]) for x in edge_parziale]:
                w = self.G[nodo][v]['weight']
                if w > soglia:
                    result.append((v, w))

        return result




