import random

from pyabsa import AspectTermExtraction as ATEPC
from pyabsa import DatasetItem, ModelSaveOption, DeviceTypeOption

config = ATEPC.ATEPCConfigManager.get_atepc_config_english()
config.model = ATEPC.ATEPCModelList.FAST_LCF_ATEPC
config.evaluate_begin = 0
config.max_seq_len = 256
config.batch_size = 16
config.pretrained_bert = "microsoft/mdeberta-v3-base"
config.log_step = -1
config.l2reg = 1e-8
config.num_epoch = 20
config.use_bert_spc = True
config.use_amp = False
config.cache_dataset = True
config.cross_validate_fold = -1
config.patience = 5
config.show_metric = True

config.index_to_IOB_label = {1: 'B-ASP', 2: 'I-ASP', 3: 'O'}
config.IOB_label_to_index = {'B-ASP': 1, 'I-ASP': 2, 'O': 3}

dataset = DatasetItem("1110.game_reviews")

trainer = ATEPC.ATEPCTrainer(config=config,
                             from_checkpoint='',
                             dataset=dataset,
                             checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,
                             auto_device=True,
                             load_aug=False
                             )
extractor = trainer.load_trained_model()
trainer.destroy()

atepc_examples = [
    'Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
    'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
    'Celkem vklidu hra s velmi dobrou grafikou, ale špatnou optimalizací.  :)',
    "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
    "Hra je super, potrebuje ešte pár optimalizácií, ale už teraz je to najlepší Battle Royale aký som kedy hral.PS: Je to jediný Battle Royale, čo som kedy hral :D"
    ]
extractor.batch_predict(atepc_examples,  #
                        save_result=True,
                        print_result=True,  # print the result
                        pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
                        )
extractor.destroy()
