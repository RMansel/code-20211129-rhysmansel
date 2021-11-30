from os import path
from typing import Tuple
from pandas import DataFrame, to_numeric
from warnings import warn


class BMI:
    """
    A class to calculate BMI/BMI ranges

    Attributes
    ----------
    df (str): the pandas dataframe being processed.
    """

    def __init__(self, df: DataFrame):
        """
        Init

        :param df: Input dataframe.

        :type df: DataFrame
        """
        self.cols = ["Gender", "HeightCm", "WeightKg"]
        if not all(item in df.columns for item in self.cols):
            raise ValueError("Not all required columns are in input DataFrame")
        self.df = df

    @staticmethod
    def _bmi_cat(df: DataFrame) -> Tuple[str, str]:
        """
        Apply categories to BMI scores.

        :param df: Input dataframe

        :return: Tuple[str, str]
        """
        if df['BMI'] < 18.5:
            return 'Underweight', 'Malnutrition risk'
        elif 18.5 <= df['BMI'] < 25:
            return 'Normal weight', 'Low risk'
        elif 25 <= df['BMI'] < 30:
            return 'Overweight', 'Enhanced risk'
        elif 30 <= df['BMI'] < 35:
            return 'Moderately obese', 'Medium risk'
        elif 35 <= df['BMI'] < 40:
            return 'Severely obese', 'High risk'
        elif 40 <= df['BMI']:
            return 'Very severely obese', 'Very high risk'

    def range_cnt(self, bmi_cat: str) -> int:
        """
        Counts number of records that match the BMI category passed.

        :param bmi_cat: name of BMI category to be counted.

        :type bmi_cat: str

        :return: number of records matching the bmi_cat category in the dataframe.

        :rtype: int
        """
        return len(self.df.loc[self.df['BMICat'] == bmi_cat])

    def bmi_val(self):
        """
        Validates that input data matches possible human measurements and has correct dtypes.
        Warns and removes those that do not. Coerces where possible.
        """
        in_len = len(self.df)
        self.df['Gender'] = self.df['Gender'].astype(str)
        self.df['WeightKg'] = to_numeric(self.df['WeightKg'], errors='coerce')
        self.df['HeightCm'] = to_numeric(self.df['HeightCm'], errors='coerce')
        self.df = self.df.dropna()
        self.df = self.df.loc[(self.df['WeightKg'] < 800) &
                              (self.df['WeightKg'] > 0) &
                              (self.df['HeightCm'] < 300) &
                              (self.df['HeightCm'] > 0)]
        df_diff = in_len - len(self.df)
        if df_diff != 0:
            warn(f"{df_diff} rows from input were invalid and have been removed.")

    def bmi_calc(self, validate: bool = True):
        """
        Calculates BMI and BMI categories

        :param validate: Whether the input data should be validated.

        :type validate: bool
        """
        if validate:
            self.bmi_val()
        self.df['BMI'] = (self.df['WeightKg'] / self.df['HeightCm'].div(100).pow(2))
        self.df[['BMICat', 'HealthRisk']] = self.df.apply(self._bmi_cat, axis=1, result_type='expand')

    def write(self, loc: str, indent: int = 0):
        """
        Writes dataframe to json at provided location

        :param indent: Pretty print indentation spaces

        :type indent: int

        :param loc: path to write file

        :type loc: str
        """
        self.df.to_json(loc, orient='records', indent=indent)
