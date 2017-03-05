import boto3
import pickle


def pickle_dictionary_to_file(dictionary, output):
    """
    Create a new file and write the provided dictionary to it.
    """
    with open(output, "w") as f:
        pickle.dump(dictionary, f)
