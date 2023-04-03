import json
import findfile

task = "joint-aspect-sentiment-category"
model = "checkpoint-1400"


def run_inference_on_file(model, file, save_result=True):

    save_filename = f"output-{model}-{'-'.join(file.rsplit('/', 2)[-2:])}.jsonl"
    save_file = findfile.find_cwd_file(save_filename)
    if save_file:
        with open(save_file, "r", encoding="utf-8") as f:
            results = json.load(f)
            return results

    import tqdm
    from pyabsa import ABSAInstruction, meta_load
    generator = ABSAInstruction.ABSAGenerator(
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
    inference_files = ["D:/PythonProjects/SentimentAnalysis/data/appid_1426210_czech.txt"]

    for f in inference_files:
        results = run_inference_on_file(model=model, file=f)
        print(f"Results for file {f}:")
        for result in results:
            print(result["text"])
            quad = "|".join([f"{q['aspect']}:{q['category']}:{q['opinion']}:{q['polarity']}" for q in result["Quadruples"]])
            print(quad)

if __name__ == "__main__":
    main()


