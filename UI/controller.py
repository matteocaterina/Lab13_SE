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
        self._view.lista_visualizzazione_1.clean()
        num_vertici = self._model.get_number_of_nodes()
        num_edges = self._model.get_number_of_edges()
        min_peso = self._model.get_min_peso()
        max_peso = self._model.get_max_peso()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {num_vertici}   Numero di archi: {num_edges}\n'
                                                                   f'Informazioni sui pesi degli archi - valore minimo: {min_peso} e valore massimo: {max_peso}'))

        self._view.update()


    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        # TODO
        try:
            soglia = float(self._view.txt_name.value)
            if soglia < 3 or soglia > 7:
                self._view.show_alert('Inserire un numero compreso tra 3 e 7')
                return
            else:
                self._view.lista_visualizzazione_2.clean()
                minori, maggiori = self._model.conta_archi_soglia(soglia)
                self._view.lista_visualizzazione_2.controls.append(ft.Text(
                    f'Numero archi con peso maggiore della soglia: {maggiori}\n'
                    f'Numero archi con peso minore della soglia: {minori}'))
        except ValueError:
            self._view.show_alert('Valore numerico non valido')


        self._view.update()


    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO
        soglia = float(self._view.txt_name.value)
        self._model.grafo_filtrato(soglia)
        self._view.lista_visualizzazione_3.clean()
        percorso, peso = self._model.cammino_massimo()
        lunghezza = len(percorso)
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f'Numero archi percorso più lungo: {lunghezza}'))
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f'Peso cammino massimo: {peso}'))
        for ii in self._model.soluzione_best:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(
                f'{ii[0]} --> {ii[1]}:{str(ii[2]['weight'])}'
            ))


        self._view.update()
