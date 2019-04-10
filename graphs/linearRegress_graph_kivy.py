# -*- coding: utf-8 -*-

from linear_regression import LinearRegression
from kivy.graphics import Callback
from kivy.garden.graph import Graph, SmoothLinePlot

class GraphLinearRegression(LinearRegression):
    """Cette classe crée l'affichage du graphique des courbes de régression linéaire.
    """
    
    def __init__(self, n, S, C, t, I):
        """
        Paramètres
        ----------
        n : int
            Nombre d'électrons échangés au cours de la réaction.
        S : float
            Surface d'échange.
        C : float
            Concentration de l'espèce.
        t : list
            Tableau de valeurs des temps expérimentaux.
        I : list
            Tableau de valeurs des Intensités mesurées expérimentalement.
        """
        super(GraphLinearRegression, self).__init__(t, I)
        self.n=n 
        self.S=S
        self.C=C

        graph_theme = {
            'label_options': {
                'color': [0, 0, 0, 1],  # color of tick labels and titles
                'bold': False},
            'background_color': [1, 1, 1, 1],  # back ground color of canvas
            'tick_color': [0, 0, 0, 1],  # ticks and grid
            'border_color': [0, 0, 0, 1]}  # border drawn around each graph
            
        self.graph = Graph(title = 'Courbes de Regression lineaire',
           xlabel='log Temps (s)',
           ylabel='log Intensité (A)',
           x_ticks_minor=5,
           x_ticks_major=5,
           y_ticks_major=0.2,
           y_ticks_minor=4,
           y_grid_label=True,
           x_grid_label=True,
           padding=5,
           x_grid=False,
           y_grid=False,
           **graph_theme)
    
        self.logexpplot = SmoothLinePlot(color=[1, 0, 0, 1])
        self.logexpplot.label = "Expérimentale"
        
        self.linlogexpplot = SmoothLinePlot(color=[1, 0, 1, 1])

        self.graph.legend = True
    
        self.graph.add_plot(self.logexpplot) 
        self.graph.add_plot(self.linlogexpplot)
        self._update_ticks_counts = 0 # Pour éviter un clignotement
        with self.graph.canvas:
            self.cb_update = Callback(self.update_ticks)
    
    def update(self, *args):
        """Cette fonction met à jour l'affichage des courbes de régression 
        linéaire et le calcul du coefficient de diffusion expérimentale. 
        """
        self.logexp_and_linear_curves_tab(self.t, self.I)
        _, intercept= self.linregress()
        self.Dexp=self.calculate_D ( intercept, self.n, self.S, self.C)
        
        self.linlogexpplot.label = "Régression linéaire\nD="+str(self.Dexp)
        
        self.logexpplot.points = list(zip(self.logexpt, self.logexpI))
        self.linlogexpplot.points = list (zip(self.logexpt, self.linlogexpI))
        
        self.graph.xmin=float(min(self.logexpt))
        self.graph.xmax=float(max(self.logexpt))
        self.graph.ymin=float(min(self.logexpI))
        self.graph.ymax=float(max(self.logexpI))
        self._update_ticks_counts = 0
        self.update_ticks()
    
    def update_ticks(self, *args):
        if self._update_ticks_counts < 10:
            self._update_ticks_counts+=1
            width, height = self.graph.get_plot_area_size()
            self.graph.x_ticks_major = (self.graph.xmax-self.graph.xmin)/(width/100)
            self.graph.x_ticks_minor = 10
            self.graph.y_ticks_major = (self.graph.ymax-self.graph.ymin)/(height/50)
            self.graph.y_ticks_minor = 5
        
    def get_canvas(self):
        return self.graph
