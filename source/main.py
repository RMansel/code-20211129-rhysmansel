from os import path
from pandas import read_json

from source.bmi import BMI


def main(*args: [str], infile: str, outfile: str = None, validate: bool = True) -> dict:
    """
    Loads Json from path or string and calculates BMI and BMI categories. Optionally writes output.

    :param args: BMI categories to be counted.

    :type args: [str]

    :param infile: path to input. json file or json string.

    :type infile: str

    :param outfile: path to output file.

    :type outfile: str

    :param validate: flag for whether input data should be validated as possible human measurements.

    :type validate: bool

    :return: A dict containing provided BMI categories as keys and their respective counts.

    :rtype: dict
    """
    if path.isfile(infile):
        with open(infile, "r") as file:
            df = read_json(file.read())
    else:
        df = read_json(input)
    bmi = BMI(df)
    bmi.bmi_calc(validate)
    if outfile is not None:
        bmi.write(outfile)
    out_dict = {}
    for bmi_cat in args:
        out_dict[bmi_cat] = bmi.range_cnt(bmi_cat)
    return out_dict


if __name__ == '__main__':
    res = main("Overweight",
               infile=f"{path.dirname(__file__)}/../resources/input.json",
               outfile=f"{path.dirname(__file__)}/../output/output.json",
               validate=True)
    for k, v in res.items():
        print(f"There are {v} patients in the {k} category")
