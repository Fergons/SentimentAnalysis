"""
Created by Frantisek Sabol
Scripts for evaluation of the model on ACOS task
"""
import os

import findfile
import tqdm
from Levenshtein import distance as levenshtein_distance
from app.services.analyzer.acos.data_utils import create_task_output_string
from pathlib import Path
import json
from collections import Counter
from typing import List, Dict, Union
from transformers import MT5Tokenizer, MT5EncoderModel
import torch

# task = "joint-aspect-category"
batch_size = 24

# model = "checkpoints\multitask\joint-acos-1335.GamesACOS-mt5-base-joint-acos-1335.GamesACOS\checkpoint-1863"
# model = "checkpoints\multitask\joint-acos-1335.GamesACOS-finetuned_acos_on_ood_model\checkpoint-1380"
# models = "joint-acos-1335.GamesACOS-mt5-base-i3eg-5e-ood"
# models = "joint-acos-1335.GamesACOS-finetuned_acos_on_ood_model"
# models = "joint-acs-1333.Games_ACS-mt5-base-i2eg"
# models = "joint-acos-1335.GamesACOS-mt5-base-i3eg-5e-ood"
models = "models"
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

# task = "joint-cs"
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
        distance = levenshtein_distance(word[label].lower(), w[label].lower())
        if distance < min_distance:
            min_distance = distance
            most_similar_word = w
    if min_distance > 8:
        most_similar_word = ""
    return most_similar_word


# Initialize the tokenizer and model
tokenizer = MT5Tokenizer.from_pretrained("google/mt5-base")
eval_model = MT5EncoderModel.from_pretrained("google/mt5-base")


def get_aspect_opinion_pair_string(quadruple: dict) -> str:
    return f"{quadruple['aspect'] if quadruple['aspect'] != 'NULL' else ''} {quadruple['opinion'] if quadruple['opinion'] != 'NULL' else ''}"


def compute_similarity(word1: torch.Tensor, word2: torch.Tensor) -> float:
    cos = torch.nn.CosineSimilarity(dim=1)
    return cos(word1, word2).item()


# def find_most_similar_word(word: Dict, word_list: List[Dict], label: str) -> Dict:
#     word_embedding = get_embedding(get_aspect_opinion_pair_string(word))
#     similarities = [compute_similarity(word_embedding, get_embedding(get_aspect_opinion_pair_string(w))) for w in
#                     word_list]
#     if not similarities:
#         return ""
#     return word_list[similarities.index(max(similarities))]


def get_embedding(word: str) -> torch.Tensor:
    inputs = tokenizer(word.strip(), return_tensors="pt")
    outputs = eval_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)


def find_most_similar_word_based_on_all_labels(word, word_list, labels=None):
    if labels is None:
        labels = ["aspect", "opinion"]
    words = []
    for label in labels:
        words.append(find_most_similar_word(word, word_list, label=label))
    # find the occurencies of each dictionary in the list
    # and return the most common one
    words = [json.dumps(word, ensure_ascii=False) for word in words]
    most_common = Counter(words).most_common(1)[0][0]
    return json.loads(most_common)


def evaluate_labels(true_quadruples, pred_quadruples, labels=None, lines=None, task="joint-acos"):
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
    if task == "joint-acos":
        eval_result.update({"triplet": {"count": 0, "total": 0}})

    with open("manual_export.tsv", "w", encoding="utf-8") as fexport:
        fexport.write("Id\tReview\tAspect\tOpinion\tCategory\tPolarity\t\n")
        for i, trues in true_quadruples.items():
            _pred_quads = pred_quadruples[i]
            # remove duplicate dictionaries with the same values from _pred_quads

            trues_str = create_task_output_string(task, outputs=trues)
            pred_quads_str = create_task_output_string(task, outputs=_pred_quads)
            for _pred in _pred_quads:
                fexport.write(f"{i}\t{lines[int(i)]['text']}\t{_pred['aspect']}\t{_pred['opinion']}\t{_pred['category']}\t{_pred['polarity']}\t\n")
            for true in trues:
                eval_result["joint"]["total"] += 1
                if task == "joint-acos":
                    eval_result["triplet"]["total"] += 1

                if len(_pred_quads) == 0:
                    continue
                elif true["aspect"] != "NULL":
                    pred = find_most_similar_word(true, _pred_quads, label="aspect")
                elif len(_pred_quads) == 1:
                    pred = _pred_quads[0]
                else:
                    pred = [p for p in _pred_quads if p["category"] == true['category']]
                    pred = pred[0] if pred else _pred_quads[0]

                if pred == "":
                    continue

                else:
                    print(f"Matched: {create_task_output_string(task, outputs=[true])} == {create_task_output_string(task, outputs=[pred])}")
                    _pred_quads.remove(pred)

                eval_result["aspect"]["total"] += 1
                eval_result["polarity"]["total"] += 1
                eval_result["opinion"]["total"] += 1
                eval_result["category"]["total"] += 1

                polarity_match = true["polarity"].lower().replace(" ","") == pred["polarity"].lower().replace(" ","")
                category_match = true["category"].lower().replace(" ","") == pred["category"].lower().replace(" ","")

                aspect_match = true["aspect"].lower().strip() == pred["aspect"].lower().strip()
                if not aspect_match and (true["aspect"] not in ("NULL", "") and pred["aspect"] not in ("NULL", "")):
                    aspect_match = compute_similarity(get_embedding(true["aspect"]), get_embedding(pred["aspect"])) > 0.5

                if task == "joint-acos":
                    opinion_match = true["opinion"].lower().strip() == pred["opinion"].lower().strip()
                    if not opinion_match and (true["opinion"] not in ("NULL", "") and pred["opinion"] not in ("NULL", "")):
                        opinion_match = compute_similarity(get_embedding(true["opinion"]),
                                                            get_embedding(pred["opinion"])) > 0.5
                    if aspect_match and polarity_match and category_match:
                        eval_result["triplet"]["count"] += 1

                    if aspect_match and polarity_match and opinion_match and category_match:
                        eval_result["joint"]["count"] += 1

                    if aspect_match:
                        eval_result["aspect"]["count"] += 1

                    if polarity_match:
                        eval_result["polarity"]["count"] += 1
                    if opinion_match:
                        eval_result["opinion"]["count"] += 1

                    if category_match:
                        eval_result["category"]["count"] += 1

                elif task == "joint-aspect-category-sentiment":
                    if aspect_match and polarity_match and category_match:
                        eval_result["joint"]["count"] += 1
                    if aspect_match:
                        eval_result["aspect"]["count"] += 1
                    if polarity_match:
                        eval_result["polarity"]["count"] += 1
                    if category_match:
                        eval_result["category"]["count"] += 1



    for report in eval_result:
        if eval_result[report]["total"] == 0:
            print(f"No gold examples for {report}")
        else:
            print(f"Accuracy for {report}: {eval_result[report]['count'] / eval_result[report]['total']}")

    return eval_result


def run_eval_on_model(model, task="joint-acos"):
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
            with open(f, "r", encoding="utf-8") as fopen:
                lines = fopen.readlines()
                lines = [json.loads(line) for line in lines]
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
                                              labels=["aspect", "polarity", "opinion", "category"],
                                              lines=lines,
                                              task=task)
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
        batches = [lines[i:i + batch_size] for i in range(0, len(lines), batch_size)]
        for batch in tqdm.tqdm(batches):

            predictions = generator.batch_predict(batch=[line["text"] for line in batch], task=task)
            for line, result in zip(batch, predictions):
                true_quadruples[line_num] = line["labels"] if len(line["labels"]) > 0 else [
                    {"aspect": "NULL", "polarity": "NULL", "opinion": "NULL", "category": "NULL"}]
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

        print(
            f"Accuracy for number of aspects found: {min(num_total, pred_num_total) / max(num_total, pred_num_total)}")
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
        if "mt5-acos" in save_model_name.rsplit('/', 1)[-1]:
            result = run_eval_on_model(f"{model_checkpoint_dir}\\{model}", task=task)
            results[f"{model_checkpoint_dir}\\{model}"] = result

    with open(f"{model_checkpoint_dir}\\results-{task}.txt", "w", encoding="utf-8") as f:
        for model in results:
            for file in results[model]:
                f.write(f"Results for {model}\n")
                f.write(f"Results for {file}\n")
                eval_result = results[model][file]
                for report in eval_result:
                    if eval_result[report]["total"] == 0:
                        f.write(f"No gold examples for {report}\n")
                    else:
                        f.write(
                            f"Accuracy for {report}: {eval_result[report]['count'] / eval_result[report]['total']}\n")
                f.write("-----------------------\n")

    with open(f"{model_checkpoint_dir}\\results-{task}.tsv", "w", encoding="utf-8") as f:
        if task == "joint-acos":
            f.write("Model\tFile\tJoint\tAspect\tPolarity\tOpinion\tCategory\tTriplet\n")
        else:
            f.write("Model\tFile\tJoint\tAspect\tPolarity\tOpinion\tCategory\n")
        # sort results by keys model.rsplit('-',1)[-1]
        results = {k: v for k, v in sorted(results.items(), key=lambda item: float(item[0].rsplit('-', 1)[-1]))}
        avg_results = []
        for model in results:
            combined = {}
            for file in results[model]:
                f.write(f"{model.rsplit('-', 1)[-1]}\t{file.rsplit('/', 1)[-1]}\t")
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
