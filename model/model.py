import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.G_filtrato = nx.DiGraph()

        self._nodes = []
        self._edges = []

        self._lista_geni = []
        self._lista_cromosomi = []
        self._lista_geni_connessi = []

        self.id_map = {}

        self.load_geni()
        self.load_cromosomi()
        self.load_geni_connessi()

        self.peso_ottimo = float('-inf')
        self.soluzione_best = []

    def load_geni(self):
        self._lista_geni = DAO.get_geni()
        for g in self._lista_geni:
            self.id_map[g.id] = g.cromosoma


    def load_cromosomi(self):
        self._lista_cromosomi = DAO.get_cromosomi()

    def load_geni_connessi(self):
        self._lista_geni_connessi = DAO.get_geni_connessi()

    def crea_grafo(self):
        for c in self._lista_cromosomi:
            self._nodes.append(c)

        self.G.add_nodes_from(self._nodes)

        edges = {}
        for g1,g2, corr in self._lista_geni_connessi:
            if (self.id_map[g1], self.id_map[g2]) not in edges:
                edges[(self.id_map[g1], self.id_map[g2])] = float(corr)
            else:
                edges[(self.id_map[g1], self.id_map[g2])] += float(corr)

        for key, value in edges.items():
            self._edges.append((key[0], key[1], value))

        self.G.add_weighted_edges_from(self._edges)


    def get_number_of_nodes(self):
        return self.G.number_of_nodes()
    def get_number_of_edges(self):
        return self.G.number_of_edges()
    def get_min_peso(self):
        return min(data['weight'] for _,_,data in self.G.edges(data=True))
    def get_max_peso(self):
        return max(data['weight'] for _,_,data in self.G.edges(data=True))

    """
    def get_min_peso(self):
        return min(x[2] for x in self._edges)

    def get_max_peso(self):
        return max(x[2] for x in self._edges)
        
    viene in entrambi i modi
    """

    def conta_archi_soglia(self, soglia):
        minori = sum(1 for _,_,data in self.G.edges(data=True) if data['weight'] < soglia)
        maggiori = sum(1 for _,_,data in self.G.edges(data = True) if data['weight'] > soglia)
        return minori, maggiori


    def grafo_filtrato(self,soglia):
        self.G_filtrato.clear()
        for u,v,data in self.G.edges(data=True):
            if data['weight'] > soglia:
                self.G_filtrato.add_edge(u,v, weight=data['weight'])


    def cammino_massimo(self):

        self.peso_ottimo = float('-inf')
        self.soluzione_best = []

        for partenza in self.G_filtrato.nodes():
            nodi_parziali = [partenza]
            edges_parziali = []
            self._ricorsione(nodi_parziali, edges_parziali)

        return self.soluzione_best, self.peso_ottimo

    def _ricorsione(self, nodi_parziali, edges_parziali):

        ultimo_nodo = nodi_parziali[-1]
        vicini = self.get_admissible_neigbors(ultimo_nodo, edges_parziali)
        #print(vicini)

        if len(vicini) == 0:
            peso = self.calcolaPeso(edges_parziali)
            self.peso_ottimo = self.calcolaPeso(self.soluzione_best)
            if peso > self.peso_ottimo:
                self.soluzione_best = edges_parziali.copy()
            return

        for v in vicini:
            nodi_parziali.append(v)
            edges_parziali.append((ultimo_nodo, v, self.G_filtrato.get_edge_data(ultimo_nodo, v)))
            self._ricorsione(nodi_parziali,edges_parziali)
            nodi_parziali.pop()
            edges_parziali.pop()


    def get_admissible_neigbors(self, nodo, edges_parziali):
        result = []
        for u,v,data in self.G_filtrato.out_edges(nodo, data=True):
            if (u,v) not in [(x[0], x[1]) for x in edges_parziali]:
                result.append(v)
        return result

    def calcolaPeso(self, edges_parziali):
        pesoTotale = 0
        for e in edges_parziali:
            pesoTotale += e[2]['weight']
        return pesoTotale








