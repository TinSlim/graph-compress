from graphpress.readers import Reader_NT, Reader_NTgz, Reader_CGgz
from graphpress.parsers import WikidataParser, CGParser
from graphpress.builders import Builder

r = Reader_NT('sample/little.nt')
p = WikidataParser()
b = Builder(r,p,'sample/output','merged.gz')

b.make_partitions()
b.merge_partitions()

rc = Reader_CGgz('merged.gz')
pc = CGParser()
assert pc.parse_line(next(rc.readline())) == (1, [[132, 2, 3]])
