
class WikidataParser():
    def parse_line(self, line):
        """
        Parses a line from a Wikidata NTRIPLES dump file
        line		'<http://www.wikidata.org/entity/Q1> <http://www.wikidata.org/prop/direct/P1> <http://www.wikidata.org/entity/Q2> .'
        ret			(1,1,2)
        """
        line_split = line.split(" ")
        subj = int(line_split[0][33:-1].replace('Q',''))
        pred = int(line_split[1][38:-1].replace('P',''))
        obj = int(line_split[2][33:-1].replace('Q',''))
        return (subj, pred, obj)

class CGParser():
    def parse_line(self, line):
        """
        Parses a line from a CG file
        line		'1 2.3 4.5 6.7'
        ret			(1,[[2,3],[4,5],[6,7]])
        """
        line_split = line.split(" ")
        subj = int(line_split[0])
        return (subj,[[int(y) for y in x.split(".")] for x in line_split[1:]])