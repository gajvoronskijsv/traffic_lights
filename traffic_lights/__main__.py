from asyncio import run
from sys import argv
import argparse
from traffic_lights.crossroad import Crossroad


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ct', '--cars-top', default=5)
    parser.add_argument('-cr', '--cars-right', default=5)
    parser.add_argument('-cb', '--cars-bottom', default=5)
    parser.add_argument('-cl', '--cars-left', default=5)
    parser.add_argument('-pt', '--pedestrians-top', default=5)
    parser.add_argument('-pr', '--pedestrians-right', default=5)
    parser.add_argument('-pb', '--pedestrians-bottom', default=5)
    parser.add_argument('-pl', '--pedestrians-left', default=5)
    return parser


def main(args):
    crossroad = Crossroad()
    run(crossroad.simulate(args))


if __name__ == "__main__":  # Добавьте это условие
    parser = createParser()
    args = parser.parse_args()
    main(args)

