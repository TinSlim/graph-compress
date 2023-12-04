# graph~~com~~press

## 

graph~~com~~press is a Python library designed to compress graphs from NTRIPLES.

The resultant format writes the info of a node in a line. First the *NODE ID*, next, groups of connections, every connection has the *EDGE ID* and *NODES CONNECTED USING THE EDGE*. Considers a negative *EDGE ID* as a connection in opposite direction.

> Example:
> ```
> 14 5.3.7 -3.2
> ```
> The line says:
> -  Node 14 connects to Node 3 using Edge 5.
> - Node 14 connects to Node 7 using Edge 5.
> - Node 2 connects to Node 15 using Edge 3.


## Usage

### 

```python
from graphcompress.readers import Reader_NT, Reader_NTgz, Reader_CGgz
from graphcompress.parsers import WikidataParser, CGParser
from graphcompress.builders import Builder

r = Reader_NTgz('graph.nt.gz')
p = WikidataParser()
b = Builder(r,p,'tmp','output.gz')

b.make_partitions()
b.merge_partitions()
```

> Input file: `graph.nt.gz`
>
> ```
> <http://www.wikidata.org/entity/Q1> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q5> .
> <http://www.wikidata.org/entity/Q1> <http://www.wikidata.org/prop/direct/P3> <http://www.wikidata.org/entity/Q6> .
> <http://www.wikidata.org/entity/Q6> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q5> .
> <http://www.wikidata.org/entity/Q6> <http://www.wikidata.org/prop/direct/P5> <http://www.wikidata.org/entity/Q2> .
> ```
> (The lines above are the uncompressed file)

> Output file: `output.gz`
> ```
> 1 5.5 3.6
> 2 -5.6
> 5 -5.1.6
> 6 5.5.2 -3.1
> ```
> (The lines above are the uncompressed file)