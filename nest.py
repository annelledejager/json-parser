import argparse
import json
import sys
from pprint import pprint

from json_parser.views.json_parser import JsonParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs=argparse.REMAINDER, help='dictionary keys indicating the level of nesting')
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='input as json array (each element is a flat dictionary)')
    args = parser.parse_args().args

    if not sys.stdin.isatty():
        stdin = parser.parse_args().stdin.read()

        nest = JsonParser(args, json.loads(stdin))
        pprint(nest.parse())
