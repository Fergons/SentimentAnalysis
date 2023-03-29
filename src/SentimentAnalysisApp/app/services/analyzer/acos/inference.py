import json
import findfile
import tqdm
from pyabsa import ABSAInstruction, meta_load

task = "joint-aspect-sentiment"
model = "checkpoint-1400"


def run_inference_on_file(generator, file, save_result=True):
    lines = meta_load(file)
    save_filename = f"output-{model}-{'-'.join(file.rsplit('/', 2)[-2:])}"
    save_file = findfile.find_cwd_file(save_filename)

    results = []
    for line in tqdm.tqdm(lines):
        result = generator.predict(line, task=task)
        results.append(result)

    if save_result:
        with open(save_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    return results


def main():
    inference_files = ["D:/PythonProjects/SentimentAnalysis/data/appid_1426210_czech.txt"]
    generator = ABSAInstruction.ABSAGenerator(
        findfile.find_cwd_dir(model)
    )
    for f in inference_files:
        results = run_inference_on_file(generator=generator, file=f)
        print(f"Results for file {f}:")
        for result in results:
            print(result["text"])
            quad = "|".join([f"{q['aspect']}:{q['category']}:{q['opinion']}:{q['polarity']}" for q in result["Quadruples"]])
            print(quad)

if __name__ == "__main__":
    main()


