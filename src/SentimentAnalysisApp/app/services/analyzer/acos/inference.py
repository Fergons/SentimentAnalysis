import json
import findfile
import re
from data_utils import create_task_output_string
task = "joint-acos"
model = "checkpoints\multitask\joint-aspect-category-sentiment-1336.Games-acs-after-acos\checkpoint-608"


def run_inference_on_file(model, file, save_result=True):
    save_model = re.sub(r'\\+', '/', model)
    save_filename = f"output-{'-'.join(save_model.rsplit('/', 2)[-2:])}.jsonl"
    save_file = findfile.find_cwd_file(save_filename)
    if save_file:
        with open(save_file, "r", encoding="utf-8") as f:
            results = json.load(f)
            return results

    import tqdm
    from pyabsa import meta_load
    from model import ABSAGenerator

    generator = ABSAGenerator(
        findfile.find_cwd_dir(model)
    )

    lines = meta_load(file)
    results = []
    for line in tqdm.tqdm(lines):
        result = generator.predict(line, task=task)
        results.append(result)

    if save_result:
        with open(save_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    return results


def main():
    inference_files = ["D:/PythonProjects/SentimentAnalysis/data/appid_730_czech.txt"]

    for f in inference_files:
        results = run_inference_on_file(model=model, file=f)
        print(f"Results for file {f}:")
        for result in results:
            print(result["text"])
            quad = create_task_output_string(task, outputs=result["Quadruples"])
            print(quad)

if __name__ == "__main__":
    main()


