"""Separate parser runtime, with no access to benchmark labels."""
import json
import sys
import spacy
from team_memory.records.policy_scope import restriction


def main():
    parser = spacy.load('en_core_web_sm', disable=['ner'])
    assert parser.meta['version'] == '3.7.1'
    rows = [[restriction(pair, parser) for pair in pairs] for pairs in json.load(sys.stdin)]
    print(json.dumps(dict(spacy=spacy.__version__, parser=parser.meta['version'], rows=rows)))


if __name__ == '__main__':
    main()
