# -*- coding: utf-8 -*-
"""Pour la compatibilité avec python2"""
from __future__ import division
from math import sqrt, erfc, erf

def cox_curve(D, t, x):
    """Crée les valeurs de la courbe Cox pour `t` et `D` donnés.
    Paramètres
    ----------
    D : réel
        Valeur de `D` ( != 0).
    t : réel
        Valeur de `t` ( != 0).
    x : list
        Liste de valeurs de `x` (en cm).
    Retour
    ------
        Renvoie la liste de valeurs prises par `Cox`
    """
    constant = 2*sqrt(D*t)
    return [ (erf(pos/constant)) for pos in x ]
