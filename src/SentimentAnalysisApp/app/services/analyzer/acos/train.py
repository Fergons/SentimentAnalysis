import os
import warnings
import data_utils
import model
import findfile
warnings.filterwarnings("ignore")
import pandas as pd
from transformers import TrainerCallback
import json


class LoggingCallback(TrainerCallback):
    def __init__(self, log_file: str):
        super().__init__()
        self.log_file = log_file
        self.log_data = {"train_loss": [], "eval_loss": []}

    def on_log(self, args, state, control, logs=None, **kwargs):
        if "loss" in logs:
            self.log_data["train_loss"].append(logs["loss"])
        if "eval_loss" in logs:
            self.log_data["eval_loss"].append(logs["eval_loss"])

        with open(self.log_file, "w") as f:
            json.dump(self.log_data, f)


task_name = "multitask"
# experiment_name = "acos_finetuning_on_acs_all_data_mt5"
experiment_name = "finetuned_acos_on_ood_model"
task = "joint-acos"
train_dataset_name = "1335.GamesACOS"
test_dataset_name = "1335.GamesACOS"
logging_callback = LoggingCallback(f"{task}-{train_dataset_name}-{experiment_name}_logs.json")
# model_checkpoint = 'allenai/tk-instruct-base-def-pos'
# model_checkpoint = "kevinscaria/ate_tk-instruct-base-def-pos-neg-neut-combined"
# model_checkpoint = 'allenai/tk-instruct-large-def-pos'
# model_checkpoint = 'checkpoints/multitask/joint-aspect-category-sentiment-1336.Games-acs-after-acos/checkpoint-608'
# model_checkpoint = 'checkpoints/multitask/joint-aspect-category-sentiment-1337.GamesCzechEng/checkpoint-last'
# model_checkpoint = 'checkpoints/multitask/joint-aspect-category-sentiment-1336.Games/checkpoint-760'
# model_checkpoint = 'checkpoints/multitask/googlemt5-base-joint-aspect-sentiment-501.Laptop14/checkpoint-1467'
# model_checkpoint = "google/mt5-base"
model_checkpoint = "checkpoints\multitask\joint-acos-506.Synthetic-ood_data\checkpoint-3537"
from_checkpoint = False
print("Experiment Name: ", experiment_name)
model_out_path = "checkpoints"
model_out_path = os.path.join(
    model_out_path, task_name, f"{task}-{train_dataset_name}-{experiment_name}"
)
print("Model output path: ", model_out_path)

# Load the data
id_train_file_path = f"../../../../integrated_datasets/acos_datasets/{train_dataset_name}"
id_test_file_path = f"../../../../integrated_datasets/acos_datasets/{test_dataset_name}"


id_tr_df = data_utils.read_json(id_train_file_path, "train.main_categories")
id_te_df = data_utils.read_json(id_test_file_path, "test.main_categories")

id_tr_df = pd.DataFrame(id_tr_df)
id_te_df = pd.DataFrame(id_te_df)

loader = data_utils.InstructDatasetLoader(id_tr_df, id_te_df)

if loader.train_df_id is not None:
    loader.train_df_id = loader.prepare_instruction_dataloader(loader.train_df_id, task=task)
if loader.test_df_id is not None:
    loader.test_df_id = loader.prepare_instruction_dataloader(loader.test_df_id, task=task)

# Create T5 utils object
t5_exp = model.ABSAGenerator(model_checkpoint)

# Tokenize Dataset
id_ds, id_tokenized_ds, ood_ds, ood_tokenzed_ds = loader.create_datasets(
    t5_exp.tokenize_function_inputs
)

# Training arguments
training_args = {
    "output_dir": model_out_path,
    "evaluation_strategy": "epoch",
    "resume_from_checkpoint": False,
    "save_strategy": "epoch",
    "learning_rate": 5e-5,
    "per_device_train_batch_size": 6,
    "per_device_eval_batch_size": 16,
    "num_train_epochs": 10,
    "weight_decay": 0.01,
    "warmup_ratio": 0.1,
    "load_best_model_at_end": True,
    "push_to_hub": False,
    "eval_accumulation_steps": 1,
    "predict_with_generate": True,
    "logging_steps": id_tokenized_ds.num_rows["train"]/6,
    "use_mps_device": False,
    "fp16": False
}

# Train model
model_trainer = t5_exp.train(id_tokenized_ds, additional_callbacks=[logging_callback], **training_args)
print("Training finished")