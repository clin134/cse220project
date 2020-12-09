# cse220project
I put the lgdb forder as a result of synthesizing boombase.v at https://drive.google.com/drive/folders/1a0jFo_JJHtHbbpLaLS7uEog36n2DnEgm?usp=sharing \
boombase.v is from https://github.com/masc-ucsc/livehd/tree/master/tests/benchmarks/boom \
the graph benchmark mico.lg is from https://graphbenchmark.com/ \
usage of graph_traverse.py :
```
    python graph_traverse.py [-f <graph file path>] [-ex] [-d <the traversal depth. Default 3>] [-t <the number of the most frequent patterns to show. Default 5>]
```
the -ex option means the experiment mode where the program anlyze the example graph
```
example_graph = {'A': ['+', ['B', 'C'] ], 'B': ['*', ['A', 'C', 'D'] ], 'C': ['and', ['A','B','D'] ], 'D': ['+', ['B','C'] ], 'E': ['and', ['F'] ], 'F': ['or', ['E', 'C'] ]}
```
sample usage :
```
    python graph_traverse.py -ex -d 4 -t 3
```
output:
```
for depth  1
pattern:  {"0": ["+", []]}
frequency:  2
pattern:  {"0": ["and", []]}
frequency:  2
pattern:  {"0": ["*", []]}
frequency:  1
for depth  2
pattern:  {"0": ["*", [1]], "1": ["+", [0]]}
frequency:  2
pattern:  {"0": ["and", [1]], "1": ["+", [0]]}
frequency:  2
pattern:  {"0": ["and", [1]], "1": ["*", [0]]}
frequency:  1
for depth  3
pattern:  {"0": ["and", [1, 2]], "1": ["*", [0, 2]], "2": ["+", [0, 1]]}
frequency:  2
pattern:  {"0": ["and", [1]], "1": ["+", [0]], "2": ["or", [0]]}
frequency:  2
pattern:  {"0": ["*", [1, 2]], "1": ["+", [0]], "2": ["+", [0]]}
frequency:  1
for depth  4
pattern:  {"0": ["and", [1]], "1": ["+", [0]], "2": ["or", [0, 3]], "3": ["and", [2]]}
frequency:  2
pattern:  {"0": ["and", [1, 2]], "1": ["*", [0, 2]], "2": ["+", [0, 1]], "3": ["or", [0]]}
frequency:  2
pattern:  {"0": ["and", [1, 2, 3]], "1": ["*", [0, 2, 3]], "2": ["+", [0, 1]], "3": ["+", [0, 1]]}
frequency:  1
```
