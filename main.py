import os.path

import matplotlib.pyplot as plt

from hdfs_client import HdfsClient
from kmeans_clustering import KMeansClustering
from scaler import Scaler
from spark_session_provider import SparkSessionProvider
from utils import cur_dir
from vectorizer import Vectorizer


def plot_silhouette_scores(scores, k_search_range):
    plt.plot(k_search_range, scores)
    plt.xlabel('k')
    plt.ylabel('silhouette score')
    plt.title('Silhouette Score')
    plt.show()


def move_dataset_to_hfds(
        datasetpath,
        hdfs_client: HdfsClient,
        hdfs_path,
):
    hdfs_client.write_csv(datasetpath, hdfs_path, overwrite=True)


def main():
    hdfs_client = HdfsClient()
    dataset_path = cur_dir() + '/dataset.csv'
    hdfs_path = os.path.basename(dataset_path)
    move_dataset_to_hfds(dataset_path, hdfs_client, hdfs_path)
    pd_dataset = hdfs_client.read_csv(hdfs_path)

    spark = SparkSessionProvider().provide_session()
    vectorizer = Vectorizer()
    scaler = Scaler()
    clusterizer = KMeansClustering()

    # https://stackoverflow.com/questions/77217809/comparing-reading-directly-using-pyspark-vs-pandas-and-then-converting-to-spark
    dataset = spark.createDataFrame(pd_dataset)

    vectorized_dataset = vectorizer.vectorize(dataset)
    scaled_dataset = scaler.scale(vectorized_dataset)

    scores = clusterizer.clusterize(scaled_dataset)
    plot_silhouette_scores(scores, clusterizer.k_search_range)

    spark.stop()


if __name__ == '__main__':
    main()
