import os.path

from hdfs_client import HdfsClient
from kmeans_clustering import KMeansClustering
from scaler import Scaler
from spark_session_provider import SparkSessionProvider
from utils import root_dir
from vectorizer import Vectorizer


def main():
    hdfs_client = HdfsClient()
    dataset_path = root_dir() + '/dataset.csv'
    hdfs_path = os.path.basename(dataset_path)
    hdfs_client.upload_file(
        hdfs_path=hdfs_path,
        local_path=dataset_path,
        overwrite=True,
    )

    spark = SparkSessionProvider().provide_session()
    vectorizer = Vectorizer()
    scaler = Scaler()
    clusterizer = KMeansClustering()

    local_path = root_dir() + '/tmp.csv'
    dataset = hdfs_client.read_csv(
        hdfs_csv_path=hdfs_path,
        local_path=local_path,
        spark_session=spark,
    )

    vectorized_dataset = vectorizer.vectorize(dataset)
    scaled_dataset = scaler.scale(vectorized_dataset)
    scaled_dataset.collect()

    _ = clusterizer.clusterize(scaled_dataset)

    spark.stop()


if __name__ == '__main__':
    main()
