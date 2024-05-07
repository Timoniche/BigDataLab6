import configparser
import pathlib

import pandas as pd

from hdfs import InsecureClient


class HdfsClient:
    def __init__(self):
        self.config = configparser.ConfigParser()
        curdir = str(pathlib.Path(__file__).parent)
        self.config.read(curdir + '/config.ini')
        self.client = InsecureClient(
            url=self.config['hadoop']['url'],
            user=self.config['hadoop']['user'],
        )

    def write_csv(
            self,
            csvpath,
            hdfs_csvpath,
            overwrite=True,
    ):
        df = pd.read_csv(
            csvpath,
            sep='\t',
            low_memory=False,
        )
        with self.client.write(
                hdfs_csvpath,
                encoding='utf-8',
                overwrite=overwrite,
        ) as writer:
            df.to_csv(writer)

    def read_csv(
            self,
            hdfs_csvpath,
    ):
        with self.client.read(hdfs_csvpath, encoding='utf-8') as reader:
            df = pd.read_csv(reader)

        return df
