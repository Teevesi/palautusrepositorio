import unittest
import os
import sys

# Add the parent directory (src) to the Python path
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.join(dir_path, "..")
sys.path.insert(0, parent_path)

from src.laskin import Laskin



class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self, teksti):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)


class TestLaskin(unittest.TestCase):
    def test_yksi_summa_oikein(self):
        io = StubIO(["1", "3", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        self.assertEqual(io.outputs[0], "Summa: 4")

    def test_kaksi_summaa_oikein(self):
        io = StubIO(["1", "3", "2", "5", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        self.assertEqual(io.outputs[0], "Summa: 4")
        self.assertEqual(io.outputs[1], "Summa: 7")
