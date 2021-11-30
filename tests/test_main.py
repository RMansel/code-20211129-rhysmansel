from unittest import TestCase
from src.main import main


class Test(TestCase):
    def test_main(self):
        res = main("Overweight",
                   "Moderately obese",
                   "Normal weight",
                   infile=f"./resources/valid.json",
                   validate=True)
        self.assertEqual(1, res["Overweight"])
        self.assertEqual(1, res["Moderately obese"])
        self.assertEqual(1, res["Normal weight"])

