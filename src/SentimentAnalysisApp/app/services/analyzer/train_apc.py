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
                                  from_checkpoint='',
                                  dataset=dataset,
                                  checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,
                                  auto_device=True,
                                  load_aug=False
                                  )