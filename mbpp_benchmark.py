import os

import numpy as np
import pandas as pd

# from tqdm import tqdm
from tqdm import tqdm
import multiprocessing as multiprocess

# from datasets import load_dataset
# dataset = load_dataset("mbpp", split="all")
# dataset.to_csv("benchmark_data.csv", index=False)

from pytest_runner import run_pytest
from agent import CodeAgent
from client_interface.client import ClientInterface


class HumanEvalTestBenchmark:
    def __init__(self, dataset, tmp_folder="tmp", max_retries=8, max_feedback=1):
        self.dataset = dataset["code"].to_numpy().tolist()[:10]
        self.tmp_folder = tmp_folder
        self.max_retries = max_retries
        self.max_feedback = max_feedback
        # self.client = ClientInterface()

    def _run_test(self, prompt, num_retries=5, max_feedback=1):
        # from agent import CodeAgent
        # from pytest_runner import run_pytest
        # import pandas as pd

        from agent import CodeAgent
        from client_interface.client import ClientInterface

        source_code = prompt

        result_passes = lambda result: (
            result["coverage"] >= 90
            and (not result["failed_assertions"])
            and (not result["stderr"])
        )

        has_errors = lambda result: (result["failed_assertions"]) or (
            not result["stderr"]
        )

        all_results = []
        model = CodeAgent()  # client=self.client)

        initial_preds = model.generate_response(source_code, n=num_retries)

        return initial_preds

    def run_evaluation(self):
        runs = []

        with multiprocess.Pool(
            processes=multiprocess.cpu_count()
        ) as pool:  # TODO: LOCK NUMBER
            runs = list(
                tqdm(pool.imap(self._run_test, self.dataset), total=len(self.dataset))
            )

        # identical = [self.dataset[0] for _ in range(4)]
        # for i in tqdm(identical):
        #     runs.append(self._run_test(i))
        # runs = self._run_test(self.dataset[0])

        return runs


if __name__ == "__main__":
    dataset = pd.read_csv("benchmark_data.csv", index_col=0)
    evaluator = HumanEvalTestBenchmark(dataset)
    x = evaluator.run_evaluation()
    print(x)
