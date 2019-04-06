# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, SmoothLinePlot, DotPlot
from .cottrel_graph_base import CottrelGraphBase
import math

class CottrelGraph(CottrelGraphBase):
    """Cette classe crée le graphique contenant les courbes de Cottrel en 
    utilisant kivy.garden.graph.
    """
    def __init__(self, t=[], I=[]):
        """
        """
        super(CottrelGraph, self).__init__(t, I)
        graph_theme = {
                'label_options': {
                    'color': [0, 0, 0, 1],  # color of tick labels and titles
                    'bold': False},
                'background_color': [1, 1, 1, 1],  # back ground color of canvas
                'tick_color': [0, 0, 0, 1],  # ticks and grid
                'border_color': [0, 0, 0, 1]}  # border drawn around each graph
                
        self.graph = Graph(title = 'Courbes de Cottrel',
                           xlabel='Temps (s)',
                           ylabel='Intensité (A)',
                           x_ticks_minor=5,
                           x_ticks_major=5,
                           y_ticks_major=0.2,
                           y_ticks_minor=4,
                           y_grid_label=True,
                           x_grid_label=True,
                           padding=5,
                           x_grid=False,
                           y_grid=False, 
                           xmin=float(self.tleft),
                           xmax=float(self.tright), 
                           ymin=float(self.Ibottom),
                           ymax=float(self.Itop),
                           **graph_theme)
        
        self.thplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.thplot.label = "Théorique"
        
        self.expplot = SmoothLinePlot(color=[1, 0, 0, 1])
        self.expplot.label = "Expérimentale"
        
#        self.testplot = SmoothLinePlot(color=[0, 1, 0, 1])
#        self.testplot.points = [(5,0), (5,1.2)]
#        self.graph.add_plot(self.testplot)
        
        self.graph.legend = True
            
    def update(self): 
        """Met à jour le graphique en redessinant les courbes.
        """
        if self._display_theoric:
            self.thplot.points = list(zip(self.t,self.I))
            if self.thplot not in self.graph.plots:
                self.graph.add_plot(self.thplot)
        else:
            if self.thplot in self.graph.plots:
                self.graph.remove_plot(self.thplot)
                
        if self._display_experimental:                
            self.expplot.points = list(zip(self.expt,self.expI))
            if self.expD != None:
                self.expplot.label = 'Expérimentale\nD = {}'.format(self.expD)
            else:
                self.expplot.label = 'Expérimentale'
            
            if self.expplot not in self.graph.plots:
                self.graph.add_plot(self.expplot)
        else:
            if self.expplot in self.graph.plots:
                self.graph.remove_plot(self.expplot)
                
        self.graph.xmin = float(self.tleft)
        self.graph.xmax = float(self.tright)
        
        self.graph.ymin = float(self.Ibottom)
        self.graph.ymax = float(self.Itop) if self.Ibottom!=self.Itop else 1.0
            
    def get_canvas(self):
        return self.graph
    
    def to_widget(self, x, y, relative=False):
        return self.graph.to_widget(x, y, relative)
    
    def zoom(self, dx, dy, cx, cy):
        """
        Zoom dans le graphique par un facteur.
        
        Une valeur de `dx` ou de `dy` supérieure à 1 effectue un zoom,
        inferieure à 1 effectue un dézoom.
        Par défaut `dx=1`, `dy=1`.
        
        Paramètres
        ----------
        dx : float
            Facteur de zoom horizontal.
        dy : float
            Facteur de zoom vertical.
        cx : float
            Abscisse du point sur lequel on zoom. Doit être exprimé dans les coordonnées
            du widget.
        cy : float
            Ordonnée du point sur lequel on zoom. Doit être exprimé dans les coordonnées
            du widget.
            
        Pour convertir le point depuis les coordonées de la fenêtre dans les
        coordonnées du widget:
            `cx, cy = self.graph.to_widget(cx, cy, relative=True)`
        """
        if dx <= 0 or dy <= 0:
            return
        if self.Itop==self.Ibottom or self.tleft==self.tright:
            return
        dcx, dcy = self.graph.to_data(cx, cy)
        xratio = (dcx - self.tleft)/(self.tright - self.tleft)
        yratio = (dcy - self.Ibottom)/(self.Itop - self.Ibottom)
        
        xrange = (self.tright - self.tleft)/dx
        yrange = (self.Itop - self.Ibottom)/dy
        
        tleft = dcx - xratio*xrange
        tright = tleft + xrange
        
        Ibottom = dcy - yratio*yrange
        Itop = Ibottom + yrange
        
        self.set_limit_interval(tleft, tright, Ibottom, Itop)
        self.update()
        
    def set_limit_interval(self, tleft=None, tright=None, Ibottom=None, Itop=None):
        super(CottrelGraph, self).set_limit_interval(tleft, tright, Ibottom, Itop)
        
        width, height = self.graph.get_plot_area_size()
        self.graph.x_ticks_major = (self.tright-self.tleft)/(width/100)
        self.graph.x_ticks_minor = 10
        self.graph.y_ticks_major = (self.Itop-self.Ibottom)/(height/50)
        self.graph.y_ticks_minor = 5