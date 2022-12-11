from pyabsa import AspectTermExtraction as ATEPC, DeviceTypeOption, available_checkpoints
from pyabsa import TaskCodeOption
checkpoint_map = available_checkpoints(TaskCodeOption.Aspect_Term_Extraction_and_Classification, show_ckpts=True)
# checkpoint_map = available_checkpoints()


aspect_extractor = ATEPC.AspectExtractor('english', auto_device=DeviceTypeOption.AUTO)
# aspect_extractor = ATEPC.AspectExtractor('english', auto_device=DeviceTypeOption.AUTO)
# aspect_extractor = ATEPC.AspectExtractor('chinese', auto_device=DeviceTypeOption.AUTO)

while True:
    aspect_extractor.predict(input('Please input a sentence: '))