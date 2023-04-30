import json
import os

import findfile
import tqdm
from Levenshtein import distance as levenshtein_distance
from app.services.analyzer.acos.data_utils import create_task_output_string
from pathlib import Path


# task = "joint-aspect-category"


# model = "checkpoints\multitask\joint-acos-1335.GamesACOS-mt5-base-joint-acos-1335.GamesACOS\checkpoint-1863"
# model = "checkpoints\multitask\joint-acos-1335.GamesACOS-finetuned_acos_on_ood_model\checkpoint-1380"
# models = "joint-acos-1335.GamesACOS-byt5-base-i2eg-2b"
models = "joint-acos-1335.GamesACOS-mt5-base-i3eg-5e-ood"
# models = "joint-acos-1335.GamesACOS-finetuned_acos_on_ood_model"
# models = "joint-acs-1333.Games_ACS-mt5-base-i2eg"
# model = "checkpoint-750"

# test_files = ["D:/PythonProjects/SentimentAnalysis/data/validation/STRATEGY_data.main_categories.jsonl",
#               "D:/PythonProjects/SentimentAnalysis/data/validation/PUZZLE_generated_data.main_categories.jsonl",
#               "D:/PythonProjects/SentimentAnalysis/data/validation/FPS_generated_data.main_categories.jsonl"]

task = "joint-acos"
test_files = [
    "D:/PythonProjects/SentimentAnalysis/data/validation/ACOS_val.jsonl"
]

# task = "joint-aspect-category-sentiment"
# test_files = [
#     "D:/PythonProjects/SentimentAnalysis/data/validation/ACS_val.jsonl"
# ]


def find_most_similar_word(word, word_list, label="aspect"):
    """
    Find the most similar word in a word list
    :param word: word to be found
    :param word_list: word list
    :param label: label type
    :return: most similar word
    """
    min_distance = 100
    most_similar_word = ""
    for w in word_list:
        distance = levenshtein_distance(word[label], w[label])
        if distance < min_distance:
            min_distance = distance
            most_similar_word = w
    if min_distance > 2:
        return ""
    return most_similar_word


def evaluate_labels(true_quadruples, pred_quadruples, labels=None):
    """
    Evaluate the prediction results of a specific label
    :param true_quadruples: golden label list
    :param pred_quadruples: prediction label list
    :param label: label type
    :return: precision, recall, f1
    """
    if labels is None:
        labels = ["aspect", "polarity", "opinion", "category"]

    eval_result = {"joint": {"count": 0, "total": 0}}
    eval_result.update({label: {"count": 0, "total": 0} for label in labels})

    for i, trues in true_quadruples.items():
        _pred_quads = pred_quadruples[i]
        trues_str = create_task_output_string(task, outputs=trues)
        pred_quads_str = create_task_output_string(task, outputs=_pred_quads)
        print(f"True: {trues_str}")
        print(f"Pred: {pred_quads_str}")
        for true in trues:
            eval_result["joint"]["total"] += 1
            if true["aspect"] != "NULL":
                pred = find_most_similar_word(true, _pred_quads, label="aspect")
            else:
                pred = find_most_similar_word(true, _pred_quads, label="category")
            if pred == "":
                continue
            num_correct_labels = 0
            for label in labels:
                if label in ("opinion", "category") and true[label] == "NULL":
                    continue
                eval_result[label]["total"] += 1
                if true[label].lower() == pred[label].lower():
                    eval_result[label]["count"] += 1
                    num_correct_labels += 1

            if num_correct_labels == 3:
                eval_result["joint"]["count"] += 1

    for report in eval_result:
        if eval_result[report]["total"] == 0:
            print(f"No gold examples for {report}")
        else:
            print(f"Accuracy for {report}: {eval_result[report]['count'] / eval_result[report]['total']}")

    return eval_result


def run_eval_on_model(model):
    save_model_name = model.replace('\\', '/')
    save_dir = Path(model, 'eval')
    save_dir.mkdir(exist_ok=True)

    # save to the same dir
    results = {}
    for f in test_files:
        save_filename = Path(save_dir, f"{f.rsplit('/', 1)[-1].rsplit('.', 1)[0]}.{task}.eval.jsonl")
        save_file = save_filename.exists()
        print("Predicting on {}".format(f))
        if save_file:
            print(f"File {save_filename} already exists, woudl you like to use it? (y/n)")
            # if input() == "y":
            if True:
                with open(save_filename, "r", encoding="utf-8") as fopen:
                    data = json.load(fopen)
                    true_quadruples = data["true_quadruples"]
                    pred_quadruples = data["pred_quadruples"]
                    num_total = data["num_total"]
                    pred_num_total = data["pred_num_total"]

                if pred_num_total > num_total:
                    print(f"Accuracy for number of aspects found: {num_total / pred_num_total}")
                else:
                    print(f"Accuracy for number of aspects found: {pred_num_total / num_total}")

                eval_result = evaluate_labels(true_quadruples, pred_quadruples,
                                              labels=["aspect", "polarity", "opinion", "category"])
                results[f] = eval_result
                continue

        from pyabsa import meta_load
        from model import ABSAGenerator

        generator = ABSAGenerator(
            # "flant5-base-absa",
            findfile.find_cwd_dir(model),
        )

        lines = meta_load(f)
        true_quadruples = {}
        pred_quadruples = {}
        num_total = 0
        pred_num_total = 0
        acc_count = 0
        line_num = 0
        # create batches
        batches = [lines[i:i + 32] for i in range(0, len(lines), 32)]
        for batch in tqdm.tqdm(batches):

            predictions = generator.batch_predict(batch=[line["text"] for line in batch], task=task)
            for line, result in zip(batch, predictions):
                true_quadruples[line_num] = line["labels"] if len(line["labels"]) > 0 else [{"aspect": "NULL", "polarity": "NULL", "opinion": "NULL", "category": "NULL"}]
                pred_quadruples[line_num] = result["Quadruples"]

                num_total += len(line["labels"]) if len(line["labels"]) > 1 else 1
                pred_num_total += len(result["Quadruples"])
                line_num += 1

        with open(save_filename, "w", encoding="utf-8") as fopen:
            to_save = {
                "true_quadruples": true_quadruples,
                "pred_quadruples": pred_quadruples,
                "num_total": num_total,
                "pred_num_total": pred_num_total
            }
            json.dump(to_save, fopen, ensure_ascii=False)

        print(f"Accuracy for number of aspects found: {min(num_total, pred_num_total) / max(num_total, pred_num_total)}")
        eval_result = evaluate_labels(true_quadruples, pred_quadruples,
                                      labels=["aspect", "polarity", "opinion", "category"])
        results[f] = eval_result
    return results


if __name__ == "__main__":
    # test_files = findfile.find_cwd_files(
    #     ["integrated_datasets", "acos_datasets", "restaurant", "test"],
    #     exclude_key=[".ignore", ".txt", ".xlsx"],
    # )model
    model_checkpoint_dir = findfile.find_cwd_dir(models)
    # get list of dirs of dir
    models = os.listdir(model_checkpoint_dir)
    results = {}
    for model in models:
        save_model_name = model.replace('\\', '/')
        if "checkpoint" in save_model_name.rsplit('/', 1)[-1]:
            result = run_eval_on_model(f"{model_checkpoint_dir}\\{model}")
            results[f"{model_checkpoint_dir}\\{model}"] = result
    with open(f"{model_checkpoint_dir}\\results.txt", "w", encoding="utf-8") as f:
        for model in results:
            for file in results[model]:
                f.write(f"Results for {model}\n")
                f.write(f"Results for {file}\n")
                eval_result = results[model][file]
                for report in eval_result:
                    if eval_result[report]["total"] == 0:
                        f.write(f"No gold examples for {report}\n")
                    else:
                        f.write(f"Accuracy for {report}: {eval_result[report]['count'] / eval_result[report]['total']}\n")
                f.write("-----------------------\n")


    with open(f"{model_checkpoint_dir}\\results.tsv", "w", encoding="utf-8") as f:
        f.write("Model\tFile\tJoint\tAspect\tPolarity\tOpinion\tCategory\n")
        # sort results by keys model.rsplit('-',1)[-1]
        results = {k: v for k, v in sorted(results.items(), key=lambda item: int(item[0].rsplit('-', 1)[-1]))}
        avg_results = []
        for model in results:
            combined = {}
            for file in results[model]:
                f.write(f"{model.rsplit('-',1)[-1]}\t{file.rsplit('/',1)[-1]}\t")
                eval_result = results[model][file]
                for report in eval_result:
                    if report not in combined:
                        combined[report] = {"total": 0, "count": 0}
                    if eval_result[report]["total"] == 0:
                        f.write(f"0.0\t")
                    else:
                        f.write(f"{eval_result[report]['count'] / eval_result[report]['total']}\t")
                    combined[report]["total"] += eval_result[report]["total"]
                    combined[report]["count"] += eval_result[report]["count"]
                f.write("\n")
            # add combined results averaged over all files
            avg_results.append(combined)
        for model, combined in zip(results.keys(), avg_results):
            f.write(f"{model.rsplit('-', 1)[-1]}\tcombined\t")
            for report in combined:
                if combined[report]["total"] == 0:
                    f.write(f"0.0\t")
                else:
                    f.write(f"{combined[report]['count'] / combined[report]['total']:.2f}\t")
            f.write("\n")

