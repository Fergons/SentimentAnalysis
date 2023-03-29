from itertools import zip_longest
import json
import findfile
import tqdm
from sklearn.metrics import classification_report
from Levenshtein import distance as levenshtein_distance

task = "joint-aspect-sentiment"
model = "checkpoint-750"


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
        for true in trues:

            pred = find_most_similar_word(true, _pred_quads, label="aspect")
            if pred == "":
                continue
            eval_result["joint"]["total"] += 1
            print(
                f"Matched aspects: {':'.join([true['aspect'], true['category'], true['opinion'], true['polarity']])}, {':'.join([pred['aspect'], pred['category'], pred['opinion'], pred['polarity']])}")
            num_correct_labels = 0
            for label in labels:
                if label == "opinion" and true[label] == "NULL":
                    continue
                eval_result[label]["total"] += 1
                if true[label] == pred[label]:
                    eval_result[label]["count"] += 1
                    num_correct_labels += 1

            if num_correct_labels == len(set(labels) - {"aspect"}):
                eval_result["joint"]["count"] += 1

    for report in eval_result:
        if eval_result[report]["total"] == 0:
            print(f"No gold examples for {report}")
        else:
            print(f"Accuracy for {report}: {eval_result[report]['count'] / eval_result[report]['total']}")

    return eval_result


if __name__ == "__main__":
    # test_files = findfile.find_cwd_files(
    #     ["integrated_datasets", "acos_datasets", "restaurant", "test"],
    #     exclude_key=[".ignore", ".txt", ".xlsx"],
    # )
    test_files = ["D:/PythonProjects/SentimentAnalysis/data/validation/STRATEGY_data.main_categories.jsonl"]
    for f in test_files:
        save_filename = f"evaluation_data-{model}-{'-'.join(f.rsplit('/', 2)[-2:])}"
        save_file = findfile.find_cwd_file(save_filename)
        print("Predicting on {}".format(f))
        if save_file:
            print(f"File {save_file} already exists, woudl you like to use it? (y/n)")
            if input() == "y":
                with open(save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
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
                continue

        from pyabsa import ABSAInstruction, meta_load
        save_file = save_filename
        generator = ABSAInstruction.ABSAGenerator(
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

        for line in tqdm.tqdm(lines):
            result = generator.predict(line["text"], task=task)
            true_quadruples[line_num] = line["labels"]
            pred_quadruples[line_num] = result["Quadruples"]

            num_total += len(line["labels"])
            pred_num_total += len(result["Quadruples"])
            line_num += 1

        with open(save_file, "w", encoding="utf-8") as f:
            to_save = {
                "true_quadruples": true_quadruples,
                "pred_quadruples": pred_quadruples,
                "num_total": num_total,
                "pred_num_total": pred_num_total
            }
            json.dump(to_save, f, ensure_ascii=False)

        if pred_num_total > num_total:
            print(f"Accuracy for number of aspects found: {num_total / pred_num_total}")
        else:
            print(f"Accuracy for number of aspects found: {pred_num_total / num_total}")

        eval_result = evaluate_labels(true_quadruples, pred_quadruples,
                                      labels=["aspect", "polarity", "opinion", "category"])
