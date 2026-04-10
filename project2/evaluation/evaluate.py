import json
import random
import grpc
import os
import statistics
from pathlib import Path

from project2_pb2 import *
import project2_pb2_grpc
from utils.config import CONTROLLER_TARGET

QUESTIONS_FILE = Path(os.environ.get("WORKSPACE_FOLDER", "."), "question_set", "questions_scored.jsonl")

def load_random_question(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        questions: list[dict] = [json.loads(line) for line in file]
    return random.choice(questions)

def summarize_scores(scores: list[float]) -> dict[str, float]:
    if not scores:
        return {
            "avg": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "stdev": 0.0,
        }

    return {
        "avg": statistics.mean(scores),
        "median": statistics.median(scores),
        "min": min(scores),
        "max": max(scores),
        "stdev": statistics.stdev(scores) if len(scores) > 1 else 0.0,
    }


def print_stats(label: str, stats: dict[str, float]) -> None:
    print(label)
    print(f"  avg:    {stats['avg']:.4f}")
    print(f"  median: {stats['median']:.4f}")
    print(f"  min:    {stats['min']:.4f}")
    print(f"  max:    {stats['max']:.4f}")
    print(f"  stdev:  {stats['stdev']:.4f}")

### This function was created for readablity in main() for processing the questions in the json file ###
### Prior to this change all of the processing was done in main. Decided to put in a function instead. ###
def process_question(q: dict, stub):
    response: SearchLocalResponse = stub.Search(
        SearchRequest(embedding=q["embedding"])
    )
    expected_ids: list[str] = [x["id"] for x in q["top5"]]
    expected_scores: list[float] = [x["score"] for x in q["top5"]]

    actual_ids: list[str] = [hit.id for hit in response.hits]
    actual_scores: list[float] = [hit.score for hit in response.hits]

    hits: int = len(set(expected_ids) & set(actual_ids))
    hit_rate: float = hits / len(expected_ids) if expected_ids else 0.0

    return response, expected_ids, expected_scores, actual_ids, actual_scores, hits, hit_rate


def iteration_questions(path):
    with open(path, "r", encoding="utf-8") as file:
        questions: list[dict] = [json.loads(line) for line in file]
    return questions


def main() -> None:
    q: dict = iteration_questions(QUESTIONS_FILE)
    all_hit_rates = []
    all_expected_scores = []
    all_actual_scores = []

    with grpc.insecure_channel(CONTROLLER_TARGET) as channel:
        stub = project2_pb2_grpc.ControllerServiceStub(channel)
        ### Removed response call and placed in Process question ###
        for question in q:
            response, expected_ids, expected_scores, actual_ids, actual_scores, hits, hit_rate = process_question(question, stub)
            all_hit_rates.append(hit_rate)
            all_expected_scores.extend(expected_scores)
            all_actual_scores.extend(actual_scores)
    overall_hit_rate = sum(all_hit_rates) / len(all_hit_rates)
    expected_stats: dict[str, float] = summarize_scores(all_expected_scores)
    actual_stats: dict[str, float] = summarize_scores(all_actual_scores)
    print("=" * 80)
    # ### If you would like to see previous report Uncomment this block and Comment block below ###
    # print(f"QUESTION: {q['question']}")
    # print()
    # print(f"Target node:        {response.target}")
    # print(f"Hit rate:           {hits}/{len(expected_ids)} = {hit_rate:.4f}")
    # print(f"# Vectors Searched: {response.vectors_searched}")
    # print()

    # print_stats("Expected top-5 scores", expected_stats)
    # print()
    # print_stats("Actual returned scores", actual_stats)

    # print()
    # print("Expected IDs:")
    # for x in expected_ids:
    #     print(f"  {x}")

    # print()
    # print("Actual IDs:")
    # for x in actual_ids:
    #     print(f"  {x}")

    print("TOTAL RESULTS")
    print(f"Average hit rate: {overall_hit_rate:.4f}\n")
    print_stats("Total Expected Scores", expected_stats)
    print()
    print_stats("Total Actual Scores", actual_stats)
    print("=" * 80)


if __name__ == "__main__":
    main()