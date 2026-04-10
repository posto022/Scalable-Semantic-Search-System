import grpc
from numpy import full
import project2_pb2
import project2_pb2_grpc
from utils.utils import corpus_line_to_record
from pathlib import Path
import os

CONTROLLER_HOST = os.environ.get("CONTROLLER_HOST", "host.docker.internal")
CONTROLLER_PORT = os.environ.get("CONTROLLER_PORT", 50050)
CONTROLLER_TARGET = f"{CONTROLLER_HOST}:{CONTROLLER_PORT}"

WORKSPACE_FOLDER = os.environ.get("WORKSPACE_FOLDER", ".")
CORPUS_FOLDER = Path(WORKSPACE_FOLDER, "corpus")

def put_mini_corpus():

    mini_corpus_path = Path(CORPUS_FOLDER, "mini_corpus.jsonl")

    # Parse the mini corpus jsonl into a list of Record objects
    records : list[project2_pb2.Record] = []
    with open(mini_corpus_path, "r") as f:
        for line in f:
            records.append(corpus_line_to_record(line))

    # Connect to the controller
    with grpc.insecure_channel(CONTROLLER_TARGET) as channel:

        # Create stub
        stub = project2_pb2_grpc.ControllerServiceStub(channel)

        # Iterate over records and Put into database
        for i, record in enumerate(records, start=1):

            response = stub.Put(project2_pb2.PutRequest(record=record))

            print(
                f"put {i}: target={response.target} "
                f"count={response.target_count} split_triggered={response.split_triggered}"
            )

# function to do grouped ingestion (based on course_papers, lecture_slides, lecture_transcripts, and textbook)
# def put_grouped_corpus():
#     # Attempting to go for each folder, then each file in folder, then for each line, do Put()
#     # arbitrarily making the groups be this: course_papers, lecture_slides, lecture_transcripts, and then textbook
#     groups = ["course_papers", "lecture_slides", "lecture_transcripts", "textbook"]

#     # opening gRPC connection
#     with grpc.insecure_channel(CONTROLLER_TARGET) as channel:

#         # Create stub
#         stub = project2_pb2_grpc.ControllerServiceStub(channel)
#         count = 0

#         for group in groups:
#             group_folder = Path(CORPUS_FOLDER, group)
#             # SOURCE: https://www.geeksforgeeks.org/python/python-list-files-in-a-directory/
#             files = sorted(os.listdir(group_folder))
#             for file_name in files:
#                 if not file_name.endswith(".jsonl"):
#                     continue
#                 # SOURCE: https://www.freecodecamp.org/news/how-to-use-pathlib-module-in-python/
#                 file_path = Path(group_folder, file_name)
#                 with open(file_path, "r") as f:
#                     for line in f:
#                         # if count > 150:
#                         #     break

#                         record = corpus_line_to_record(line)
#                         response = stub.Put(project2_pb2.PutRequest(record=record))

#                         print(
#                             f"put {count}: target={response.target} "
#                             f"count={response.target_count} split_triggered={response.split_triggered}"
#                         )

#                         count += 1

def put_full_corpus():
    """TODO: Implement this function... recommended to Put one at at time with full corups to avoid reading whole file"""

    full_corpus_path = Path(CORPUS_FOLDER, "full_corpus_shuffled.jsonl")


    with grpc.insecure_channel(CONTROLLER_TARGET) as channel:

        # Create stub
        stub = project2_pb2_grpc.ControllerServiceStub(channel)

        with open(full_corpus_path, "r") as f:
            count = 0
            for line in f:
                # if count > 150:
                #     break

                record = corpus_line_to_record(line)
                response = stub.Put(project2_pb2.PutRequest(record=record))

                print(
                    f"put {count}: target={response.target} "
                    f"count={response.target_count} split_triggered={response.split_triggered}"
                )
                
                count += 1


def main():

    # put_mini_corpus()
    put_full_corpus()
    # put_grouped_corpus()


if __name__ == "__main__":
    main()
