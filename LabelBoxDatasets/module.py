import labelbox as lb
import os
import json
from uuid import uuid4

from google.cloud import storage


#API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJja2xtOGJ3ZnZwN3FmMDc3OXQ5cWhkc3pxIiwib3JnYW5pemF0aW9uSWQiOiJja2xtOGJ3ZjZhYnRsMDczOTZzandyNWEyIiwiYXBpS2V5SWQiOiJjbDJvaTJjbXdjcjA5MHphZTNvaW0zZWNpIiwic2VjcmV0IjoiNjEzMWQzNDU5NTM4YjVjOTIyMjhmM2FkOWYyNzNjZTAiLCJpYXQiOjE2NTE0ODI1NDEsImV4cCI6MjI4MjYzNDU0MX0.3SU12_8bDTZaF9i2b58Vk8QjvcL06QkQA0W3Gw5gAlQ"




class LabelBoxDataset:
    """
    Class to create a LabelBox dataset from a list of images in a GCS bucket.

    Args:
        api_key (str): The LabelBox API key.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.file_list = []
        self.gs_uri_list = []

    def get_filenames_frombucket(self, bucket_name, prefix = ''):
        """
        Get a list of filenames from a GCS bucket.

        Args:
            bucket_name (str): The name of the GCS bucket.
            prefix (str): The prefix of the filenames to get.
        """
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        self.file_list = [blob.name for blob in blobs]
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        self.gs_uri_list = ['gs://' + bucket_name + '/' + blob.name for blob in blobs]


    def generate_dataset(self, dataset_name):
        """
        Create a LabelBox dataset from a list of images in a GCS bucket.

        Args:
            dataset_name (str): The name of the LabelBox dataset.
        """
        client = lb.Client(api_key=self.api_key)
        dataset = client.create_dataset(name=dataset_name)
        self.assets = []
        for el in self.gs_uri_list[1:]:
            self.assets.append({"row_data": el, "external_id": str(el.split('/')[-1].split('.')[0])})
        task = dataset.create_data_rows(self.assets)
        task.wait_till_done()
        print("Dataset created.")

    def move_blobs(self, bucket_name, destination_bucket_name):
        """
        Move a list of blobs from one GCS bucket to another.

        Args:
            bucket_name (str): The name of the source GCS bucket.
            destination_bucket_name (str): The name of the destination GCS bucket.
        """
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(bucket_name)
        destination_bucket = storage_client.bucket(destination_bucket_name)

        for source_blob in source_bucket.list_blobs():
            new_blob = source_bucket.copy_blob(
                source_blob, destination_bucket, 'images/' + str(uuid4()) + '.jpg'
            )
            print(
                "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
                    source_blob.name,
                    source_bucket.name,
                    new_blob.name,
                    destination_bucket.name,
                )
            )

            source_blob.delete()

            print("Blob {} deleted.".format(source_blob.name))
