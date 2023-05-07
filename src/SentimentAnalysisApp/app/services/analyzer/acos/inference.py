"""
Created by Frantisek Sabol
Script for running inference on a file with a trained model. [dev]
"""
import json
import findfile
import re
from pathlib import Path
from app.services.analyzer.acos.data_utils import create_task_output_string
task = "joint-acos"
model = "checkpoints\multitask\joint-acos-1335.GamesACOS-finetuned_acos_on_ood_model\checkpoint-1380"


def run_inference_on_file(model, file, save_result=True):
    save_model = re.sub(r'\\+', '/', model)

    # save_filename = f"{model}/{inference}/output-{'-'.join(save_model.rsplit('/', 2)[-2:])}.jsonl"
    Path(save_model, "inference").mkdir(parents=True, exist_ok=True)
    save_filename = f"{model}/inference/{file.rsplit('/', 1)[-1]}.output.jsonl"
    save_file = findfile.find_cwd_file(save_filename)
    if save_file:
        if input(f"Found existing file {save_file}, do you want to overwrite it? (y/n)") in ["n", "N"]:
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
    # for line in tqdm.tqdm(lines):
    #     result = generator.predict(line, task=task)
    #     results.append(result)
    batches = [lines[i:i + 100] for i in range(0, len(lines), 100)]
    for batch in tqdm.tqdm(batches):
        result = generator.batch_predict(batch=batch, task=task)
        results.extend(result)

    if save_result:
        with open(save_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    return results


def main():
    inference_files = ["D:/PythonProjects/SentimentAnalysis/data/appid_730_czech.txt", "D:/PythonProjects/SentimentAnalysis/data/appid_668580_czech.txt"]

    for f in inference_files:
        results = run_inference_on_file(model=model, file=f)
        print(f"Results for file {f}:")
        for result in results:
            print(result["text"])
            quad = create_task_output_string(task, outputs=result["Quadruples"])
            print(quad)


if __name__ == "__main__":
    main()


