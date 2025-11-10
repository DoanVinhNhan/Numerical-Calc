from pprint import pprint
import unittest
import os
import sys
import io
import pandas as pd

from backend.numerical_methods.interpolation.central import bessel_interpolation

def test_bessel():
    x_nodes = [2.265, 2.38, 2.495, 2.61, 2.725, 2.84]
    y_nodes = [1.0018, 0.8401, 0.7006, 0.5865, 0.4809, 0.3958]

    result = bessel_interpolation(x_nodes, y_nodes)
    pprint(result)

if __name__ == "__main__":
    test_bessel()
