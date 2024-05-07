import pathlib
import unittest

from hdfs_client import HdfsClient


class HadoopTests(unittest.TestCase):
    def setUp(self):
        self.client = HdfsClient()

    def test_write_read_csv(self):
        curdir = str(pathlib.Path(__file__).parent)
        filename = 'test_csv.csv'
        csvpath = curdir + '/' + filename

        self.client.write_csv(
            csvpath=csvpath,
            hdfs_csvpath=filename,
        )

        df = self.client.read_csv(
            hdfs_csvpath=filename,
        )

        self.assertEqual(df['created_t'][0], 1623855208)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
