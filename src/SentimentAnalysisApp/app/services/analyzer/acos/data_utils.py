# -*- coding: utf-8 -*-
# file: data_utils.py
# time: 15/03/2023
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2021. All Rights Reserved.
# modified by Fergons for joint task training

import json

import findfile
import pandas as pd
from datasets import DatasetDict, Dataset

from .instruction import (
    ATEInstruction,
    CategoryInstruction,
    OpinionInstruction,
    APCInstruction,
    JointAspectCategorySentimentInstruction,
    JointAspectSentimentInstruction,
    JointACOSInstruction
)


class InstructDatasetLoader:
    def __init__(
            self,
            train_df_id,
            test_df_id,
            train_df_ood=None,
            test_df_ood=None,
            sample_size=1,
    ):
        self.train_df_id = train_df_id.sample(frac=sample_size, random_state=1999)
        self.test_df_id = test_df_id
        if train_df_ood is not None:
            self.train_df_ood = train_df_ood.sample(frac=sample_size, random_state=1999)
        else:
            self.train_df_ood = train_df_ood
        self.test_df_ood = test_df_ood

    def prepare_instruction_dataloader(self, df, task="ate"):
        """
        Prepare the data in the input format required.
        """
        ate_instructor = ATEInstruction()
        apc_instructor = APCInstruction()
        op_instructor = OpinionInstruction()
        cat_instructor = CategoryInstruction()
        aspect_category_sentiment_instructor = JointAspectCategorySentimentInstruction()
        aspect_sentiment_instructor = JointAspectSentimentInstruction()
        jointACOS_instructor = JointACOSInstruction()

        alldata = []
        for i, data in df.iterrows():
            _aspects = [label.get("aspect","NULL") for label in data["labels"]]
            aspects = []
            for asp in _aspects:
                if asp.strip() not in aspects:
                    aspects.append(asp.strip())
            aspects = "|".join(aspects)

            polarities = []
            _polarities = [
                "{}:{}".format(label.get("aspect","NULL"), label.get("polarity","NULL"))
                for label in data["labels"]
            ]
            for pol in _polarities:
                if pol not in polarities:
                    polarities.append(pol)
            polarities = "|".join(polarities)

            opinions = "|".join(
                [
                    "{}:{}".format(label.get("aspect","NULL"), label.get("opinion","NULL"))
                    for label in data["labels"]
                ]
            )

            categories = "|".join(
                [
                    "{}:{}".format(label.get("aspect","NULL"), label.get("category","NULL"))
                    for label in data["labels"]
                ]
            )

            joint = "|".join(
                [
                    f"{label.get('aspect', 'NULL')}:{label.get('category', 'NULL')}:{label.get('opinion', 'NULL')}:{label.get('polarity', 'NULL')}"
                    for label in data["labels"]
                ]
            )

            if task == "ate":
                alldata.append(
                    {"text": ate_instructor.prepare_input(data["text"]), "labels": aspects}
                )

            elif task == "apc":
                alldata.append(
                    {"text": apc_instructor.prepare_input(data["text"], aspects), "labels": polarities}
                )

            elif task == "op":
                alldata.append(
                    {"text": op_instructor.prepare_input(data["text"], aspects), "labels": opinions}
                )
            elif task == "cat":
                alldata.append(
                    {
                        "text": cat_instructor.prepare_input(data["text"], aspects),
                        "labels": categories,
                    }
                )
            elif task == "joint-acos":
                alldata.append(
                    {
                        "text": aspect_category_sentiment_instructor.prepare_input(data["text"], aspects=aspects),
                        "labels": joint
                    }
                )

            elif task == "joint-aspect-category-sentiment":
                alldata.append(
                    {
                        "text": aspect_category_sentiment_instructor.prepare_input(data["text"], aspects=aspects),
                        "labels": "|".join([
                            f"{label.get('aspect', 'NULL')}:{label.get('category', 'NULL')}:{label.get('polarity', 'NULL')}"
                            for label in data["labels"]
                        ]),
                    }
                )
            elif task == "joint-aspect-sentiment":
                alldata.append(
                    {
                        "text": aspect_sentiment_instructor.prepare_input(data["text"], aspects=aspects),
                        "labels": "|".join([
                            f"{label.get('aspect', 'NULL')}:{label.get('polarity', 'NULL')}"
                            for label in data["labels"]
                        ]),
                    }
                )

        alldata = pd.DataFrame(alldata)
        return alldata

    def create_datasets(self, tokenize_function):
        """
        Create the training and test dataset as huggingface datasets format.
        """
        # Define train and test sets
        if self.test_df_id is None:
            indomain_dataset = DatasetDict(
                {"train": Dataset.from_pandas(self.train_df_id)}
            )
        else:
            indomain_dataset = DatasetDict(
                {
                    "train": Dataset.from_pandas(self.train_df_id),
                    "test": Dataset.from_pandas(self.test_df_id),
                }
            )
        indomain_tokenized_datasets = indomain_dataset.map(
            tokenize_function, batched=True
        )

        if (self.train_df_ood is not None) and (self.test_df_ood is None):
            other_domain_dataset = DatasetDict(
                {"train": Dataset.from_pandas(self.train_df_id)}
            )
            other_domain_tokenized_dataset = other_domain_dataset.map(
                tokenize_function, batched=True
            )
        elif (self.train_df_ood is None) and (self.test_df_ood is not None):
            other_domain_dataset = DatasetDict(
                {"test": Dataset.from_pandas(self.train_df_id)}
            )
            other_domain_tokenized_dataset = other_domain_dataset.map(
                tokenize_function, batched=True
            )
        elif (self.train_df_ood is not None) and (self.test_df_ood is not None):
            other_domain_dataset = DatasetDict(
                {
                    "train": Dataset.from_pandas(self.train_df_ood),
                    "test": Dataset.from_pandas(self.test_df_ood),
                }
            )
            other_domain_tokenized_dataset = other_domain_dataset.map(
                tokenize_function, batched=True
            )
        else:
            other_domain_dataset = None
            other_domain_tokenized_dataset = None

        return (
            indomain_dataset,
            indomain_tokenized_datasets,
            other_domain_dataset,
            other_domain_tokenized_dataset,
        )


def read_json(data_path, data_type="train"):
    data = []

    files = findfile.find_files(data_path, [data_type, ".jsonl"], exclude_key=[".txt"])
    for f in files:
        print(f)
        with open(f, "r", encoding="utf8") as fin:
            for line in fin:
                data.append(json.loads(line))
    return data
