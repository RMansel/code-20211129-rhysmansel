import logging
import warnings
from unittest import TestCase
from pandas import read_json
from unittest.mock import patch, mock_open
from src.bmi.bmi import BMI


class TestBMI(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_df = read_json("./resources/valid.json")
        cls.schema_df = read_json("./resources/invalid_schema.json")
        cls.range_df = read_json("./resources/invalid_range.json")
        cls.types_df = read_json("./resources/invalid_types.json")
        cls.health_lst = ['Malnutrition risk',
                          'Low risk',
                          'Enhanced risk',
                          'Medium risk',
                          'High risk',
                          'Very high risk']
        cls.bmi_lst = ['Underweight',
                       'Normal weight',
                       'Overweight',
                       'Moderately obese',
                       'Severely obese',
                       'Very severely obese']

    def test___init__(self):
        logging.info("Testing that BMI class instantiates with correct schema")
        self.assertIsInstance(BMI(self.valid_df.copy()), BMI)
        logging.info("Testing that BMI class raises exception with incorrect schema")
        self.assertRaises(ValueError, BMI, self.schema_df.copy())

    def test_bmi_calc(self):
        logging.info("Testing that test_range_cnt calculates correctly")
        bmi = BMI(self.valid_df.copy())
        bmi.bmi_calc()
        for idx, row in bmi.df.iterrows():
            self.assertAlmostEqual(row["BMI"], row["WeightKg"] / (row["HeightCm"] / 100) ** 2)
        self.assertEqual(bmi.df['HealthRisk'].tolist(), self.health_lst)
        self.assertEqual(bmi.df['BMICat'].tolist(), self.bmi_lst)

    def test_bmi_val(self):
        logging.info("Testing that test_range_cnt validates dataframe correctly")
        bmi = BMI(self.valid_df.copy())
        bmi.bmi_val()
        self.assertEqual(6, len(bmi.df))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            logging.info("Testing that test_range_cnt correctly filters unrealistic values")
            bmi = BMI(self.range_df.copy())
            bmi.bmi_val()
            self.assertEqual(0, len(bmi.df))
            logging.info("Testing that test_range_cnt correctly filters incorrect data types")
            bmi = BMI(self.types_df.copy())
            bmi.bmi_val()
            self.assertEqual(1, len(bmi.df))
            logging.info("Testing that test_range_cnt correctly raises warning on invalid data")
            bmi = BMI(self.range_df.copy())
            self.assertWarns(UserWarning, bmi.bmi_val)

    def test_range_cnt(self):
        logging.info("Testing that test_range_cnt counts BMI categories correctly")
        bmi = BMI(self.valid_df.copy())
        bmi.bmi_calc()
        self.assertEqual(1, bmi.range_cnt('Underweight'))
        self.assertEqual(1, bmi.range_cnt('Normal weight'))
        self.assertEqual(1, bmi.range_cnt('Overweight'))
        self.assertEqual(1, bmi.range_cnt('Moderately obese'))
        self.assertEqual(1, bmi.range_cnt('Severely obese'))
        self.assertEqual(1, bmi.range_cnt('Very severely obese'))
        self.assertEqual(0, bmi.range_cnt('foo'))
        logging.info("Testing that test_range_cnt raises exception on wrong data type")
        self.assertRaises(TypeError, bmi.range_cnt(0))
        self.assertRaises(TypeError, bmi.range_cnt(True))
        self.assertRaises(TypeError, bmi.range_cnt(None))

    @patch("builtins.open", new_callable=mock_open)
    def test_write(self, mock_io):
        bmi = BMI(self.valid_df.copy())
        bmi.write("./mock.json")
        mock_io.assert_called()
