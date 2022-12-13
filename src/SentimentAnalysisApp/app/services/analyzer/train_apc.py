import random
from pyabsa import AspectPolarityClassification as APC
from pyabsa import DatasetItem, ModelSaveOption, DeviceTypeOption

config = APC.APCConfigManager.get_apc_config_multilingual()
config.model = APC.APCModelList.FAST_LSA_T_V2
config.evaluate_begin = 0
config.max_seq_len = 512
config.batch_size = 16
config.pretrained_bert = "yangheng/deberta-v3-large-absa-v1.1"
config.log_step = -1
config.l2reg = 1e-8
config.num_epoch = 20
config.seed = [random.randint(0, 1000) for _ in range(5)]
config.cache_dataset = True

dataset = DatasetItem("1111.game_reviews")

aspect_extractor = APC.APCTrainer(config=config,
                                  from_checkpoint='fast_lcf_atepc_1111.game_reviews_cdw_apcacc_62.35_apcf1_48.51_atef1_78.29',
                                  dataset=dataset,
                                  checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,
                                  auto_device=True,
                                  load_aug=False
                                  ).load_trained_model()

atepc_examples = [
    'Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
    'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
    'Celkem vklidu hra s velmi dobrou grafikou, ale špatnou optimalizací.  :)',
    "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
    "Hra je super, potrebuje ešte pár optimalizácií, ale už teraz je to najlepší Battle Royale aký som kedy hral.PS: Je to jediný Battle Royale, čo som kedy hral :D"
    ]

aspect_extractor.batch_predict(atepc_examples,  #
                               save_result=True,
                               print_result=True,  # print the result
                               pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
                               )
