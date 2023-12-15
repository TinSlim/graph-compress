# graph~~com~~press


graph~~com~~press is a Python library designed to compress graphs from NTRIPLES.

## Formats

### Compressed Graph

The resultant format writes the info of a node in a line. First the *NODE ID*, next, groups of connections, every connection has the *EDGE ID* and *NODES CONNECTED USING THE EDGE*. Considers a negative *EDGE ID* as a connection in opposite direction.

> Example:
> ```
> 14 5.3.7 -3.2
> ```
> The line says:
> - Node 14 connects to Node 3 using Edge 5.
> - Node 14 connects to Node 7 using Edge 5.
> - Node 2 connects to Node 14 using Edge 3.

### Indexed Graph

The resultant format writes the info of a node in a line. First the *NODE ID*, next, indexes of edges where the node participates

> Example:
> ```
> 14 3 5 7
> ```
> The line says:
> - Node 14 appears in the edge with the index 3.
> - Node 14 appears in the edge with the index 5.
> - Node 14 appears in the edge with the index 7.

## Install

```sh
pip install graph-compress
```

## Usage

> Input file: `graph.nt.gz`
>
> ```
> <http://www.wikidata.org/entity/Q1> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q5> .
> <http://www.wikidata.org/entity/Q1> <http://www.wikidata.org/prop/direct/P3> <http://www.wikidata.org/entity/Q6> .
> <http://www.wikidata.org/entity/Q6> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q5> .
> <http://www.wikidata.org/entity/Q6> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q2> .
> ```
> (The lines above are the uncompressed file)

### Compressed Graph

```python
from graphcompress.readers import Reader_NT, Reader_NTgz, Reader_CGgz
from graphcompress.parsers import WikidataParser, CGParser
from graphcompress.builders.compress_graph import CGBuilder

r = Reader_NTgz('graph.nt.gz')
p = WikidataParser()
b = CGBuilder(r,p,'tmp','output.gz')

b.make_partitions()
b.merge_partitions()
```

> Output file: `output.gz`
> ```
> 1 5.5 3.6
> 2 -5.6
> 5 -5.1.6
> 6 5.5.2 -3.1
> ```
> (The lines above are the uncompressed file)


### Indexed Graph

```python
from graphcompress.readers import Reader_NT, Reader_NTgz, Reader_CGgz
from graphcompress.parsers import WikidataParser, CGParser
from graphcompress.builders.index_graph import IGBuilder

r = Reader_NTgz('graph.nt.gz')
p = WikidataParser()
b = IGBuilder(r,p,'tmp','output.gz')

b.make_partitions()
b.merge_partitions()
```


> Output file: `output.gz`
> ```
> 1 0 1
> 2 3
> 5 0 2
> 6 1 2 3
> ```
> (The lines above are the uncompressed file)