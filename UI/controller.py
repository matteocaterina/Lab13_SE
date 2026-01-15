import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model.crea_grafo()
        num_nodi = self._model.G.number_of_nodes()
        num_archi = self._model.G.number_of_edges()
        minimo, massimo = self._model.get_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di nodi:{num_nodi}\n'
                                                                   f'Numero di archi: {num_archi}\n'
                                                                   f'Minimo: {minimo}, Massimo: {massimo}'))

        self._view.update()

    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        # TODO
        try:
            soglia = int(self._view.txt_name.value)
            if soglia < 3 or soglia > 7:
                self._view.show_alert('Inserire un numero compreso tra 3 e 7')
            else:
                minori, maggiori = self._model.conta_archi(soglia)
                self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Minori: {minori}\n'
                                                                           f'Maggiori: {maggiori}'))
        except ValueError:
            self._view.show_alert('Inserire un numero intero tra 3 e 7')

        self._view.update()



    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO
        try:
            soglia = int(self._view.txt_name.value)
            if soglia < 3 or soglia > 7:
                self._view.show_alert('Inserire un numero compreso tra 3 e 7')
            else:
                percorso, peso_max = self._model.cammino_massimo(soglia)
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f'Lunghezza percorso: {len(percorso)}\n'
                                                                           f'Peso_tot: {peso_max}'))
                for ii in percorso:
                    self._view.lista_visualizzazione_3.controls.append(ft.Text(
                        f'{ii[0]} --> {ii[1]}, Peso: {ii[2]} '))
        except ValueError:
            self._view.show_alert('Inserire un numero intero tra 3 e 7')

        self._view.update()

