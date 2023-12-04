from graphcompress.readers import Reader_NT, Reader_NTgz, Reader_CGgz
from graphcompress.parsers import WikidataParser, CGParser
from graphcompress.builders import Builder
import os
import unittest

ACTUAL_PATH = os.path.dirname(__file__)


class GraphcompressTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GraphcompressTest, self).__init__(*args, **kwargs)
        self.test_file = os.path.join(ACTUAL_PATH, 'data/little.nt')
        self.partitions_dir = os.path.join(ACTUAL_PATH, 'tmp/partitions')
        self.output_file = os.path.join(ACTUAL_PATH, 'tmp/merged.gz')

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(os.path.join(ACTUAL_PATH,'tmp')):
            os.mkdir(os.path.join(ACTUAL_PATH,'tmp'))
    
        if not os.path.exists(os.path.join(ACTUAL_PATH,'tmp','partitions')):
            os.mkdir(os.path.join(ACTUAL_PATH,'tmp','partitions'))
        pass

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(ACTUAL_PATH,'tmp','partitions','part_0.csv'))
        os.remove(os.path.join(ACTUAL_PATH,'tmp','merged.gz'))
        os.rmdir(os.path.join(ACTUAL_PATH,'tmp','partitions'))
        os.rmdir(os.path.join(ACTUAL_PATH,'tmp'))
        pass

    def test_all(self):
        r = Reader_NT(self.test_file)
        p = WikidataParser()
        b = Builder(r,p,self.partitions_dir,self.output_file)

        b.make_partitions()
        b.merge_partitions()

        rc = Reader_CGgz(self.output_file)
        pc = CGParser()
        self.assertEqual(pc.parse_line(next(rc.readline())), (1, [[132, 2, 3]]))        



if __name__ == '__main__':
    unittest.main()


