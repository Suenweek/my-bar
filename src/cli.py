import sys
import argparse
from . import config
from .mybar import MyBar


def add_ingredients_parser(subparsers):
    parser = subparsers.add_parser("ingredients")
    parser.add_argument("-a", "--add")
    parser.add_argument("-l", "--list")
    parser.add_argument("-d", "--delete")


def add_cocktails_parser(subparsers):
    parser = subparsers.add_parser("cocktails")
    parser.add_argument("-a", "--add")
    parser.add_argument("-l", "--list")
    parser.add_argument("-d", "--delete")


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="obj")

    add_ingredients_parser(subparsers)
    add_cocktails_parser(subparsers)

    return parser


def main(args=sys.argv[1:]):
    parser = create_parser()
    ns = parser.parse_args(args)
    bar = MyBar(config=config)
    print(ns)
