# pip install datasets evaluate
from datasets import load_dataset
from evaluate import load

human_eval = load_dataset("openai_humaneval", split="test")

code_eval_metric = load("code_eval")
test_cases = ["assert add(2,3)==5"]
candidates = [["def add(a,b): return a*b", "def add(a, b): return a+b"]]
pass_at_k, results = code_eval_metric.compute(references=test_cases, predictions=candidates, k=[1, 2])
print(pass_at_k)  # {'pass@1': 0.5, 'pass@2': 1.0}

