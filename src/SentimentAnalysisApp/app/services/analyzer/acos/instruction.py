# -*- coding: utf-8 -*-
# file: instruction.py
# time: 15/03/2023
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2021. All Rights Reserved.
# modified by Frantisek Sabol for joint task training

class Instruction:
    def __init__(self, bos_instruction=None, eos_instruction=None):
        self.bos_instruction = bos_instruction
        self.eos_instruction = eos_instruction

    def set_instruction(self, bos_instruction, eos_instruction):
        self.bos_instruction = bos_instruction
        self.eos_instruction = eos_instruction

    def get_instruction(self):
        return self.bos_instruction, self.eos_instruction


class ATEInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""
Definition: The input are sentences about a product or service. The task is to extract the aspects. Here are some examples:

example 1-
input: I charge it at night and skip taking the cord with me because of the good battery life.
{self.eos_instruction}
aspect:battery life|aspect:cord

example 2-
input: Great food, good size menu, great service and an unpretensious setting.
{self.eos_instruction}
aspect:food|aspect:menu|aspect:service|aspect:setting

Now extract aspects from the following example:
input: """

        if self.eos_instruction is None:
            self.eos_instruction = "\nlet us extract aspects one by one: \n"

        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text):
        return self.bos_instruction + input_text + self.eos_instruction


class APCInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""
Definition: The input are sentences about a product or service. The task is to extract the aspects and their corresponding polarity. Here are some examples:

example 1-
input: I charge it at night and skip taking the cord with me because of the good battery life.
The aspects are: battery life, cord
{self.eos_instruction}
battery life:positive|cord:positive

example 2-
input: Great food, good size menu, great service and an unpretensious setting.
The aspects are: food, menu, service, setting
{self.eos_instruction}
food:positive|menu:positive|service:positive|setting:positive

Now predict aspect sentiments from the following example:

input: """
        if self.eos_instruction is None:
            self.eos_instruction = "\nlet us predict sentiments one by one: \n"

        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects):
        return (
                self.bos_instruction
                + input_text
                + f"The aspects are: {aspects}"
                + self.eos_instruction
        )


class OpinionInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""
Definition: The input are sentences about a product or service. The task is to extract the aspects and their corresponding polarity. Here are some examples:

example 1-
input: I charge it at night and skip taking the cord with me because of the good battery life.
The aspects are: battery life, cord
{self.eos_instruction}
battery life:good|cord:NULL

example 2-
input: Great food, good size menu, great service and an unpretensious setting.
The aspects are: food, menu, service, setting
{self.eos_instruction}
food:great|menu:good|service:great|setting:unpretensious

Now extract opinions for the following example:
input:"""
        if self.eos_instruction is None:
            self.eos_instruction = "\nlet us extract opinions one by one: \n"

        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects):
        return (
                self.bos_instruction
                + input_text
                + f"The aspects are: {aspects}"
                + self.eos_instruction
        )


class CategoryInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""
Definition: The input are sentences about a product or service. The task is to extract the aspects and their corresponding categories. Here are some examples:

example 1-
input: I charge it at night and skip taking the cord with me because of the good battery life.
The aspects are: battery life, cord
{self.eos_instruction}
battery life:POWER_SUPPLY#GENERAL|cord:NULL

example 2-
input: Great food, good size menu, great service and an unpretensious setting.
The aspects are: food:FOOD#QUALITY| menu:RESTAURANT#GENERAL|service:SERVICE#GENERAL|setting:SERVICE#GENERAL
{self.eos_instruction}
food:FOOD#QUALITY, menu:RESTAURANT#GENERAL, service:SERVICE#GENERAL, setting:SERVICE#GENERAL

Now extract categories for the following example:
input: """
        if self.eos_instruction is None:
            self.eos_instruction = "\nlet us extract categories one by one: \n"

        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects):
        return (
                self.bos_instruction
                + input_text
                + f"The aspects are: {aspects}"
                + self.eos_instruction
        )


class JointACOSInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""extract all aspect, category, opinion, sentiment quadruples from input video game review:
example 1-
input: Příběh je velmi zajímavý ale multiplayerová část hry je plná cheaterů.
output: Příběh:gameplay:velmi zajímavý:positive|multiplayerová část hry:gameplay:plná cheaterů:negative|cheaterů:community:plná:negative
example 2-
input: Hra obsahuje rozne game mody, mapy a herni prvky.
output: game mody:gameplay:rozne:neutral|mapy:gameplay:NULL:neutral|herni prvky:gameplay:NULL:neutral
example 3-
input: Ziadne bugy hned od vydania, vynikajuce.
output: bugy:preformance_bugs:Ziadne hned od vydania:positive
Now extract aspect:category:opinion:sentiment quadruples for the following example:
input: """
        if self.eos_instruction is None:
            self.eos_instruction = "\noutput: \n"
        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects, **kwargs):
        return (
                self.bos_instruction
                + input_text
                + self.eos_instruction
        )


class JointAspectCategorySentimentInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""extract all aspect, category, sentiment triplets from input video game review:
example 1-
input: Příběh je velmi zajímavý, ale multiplayerová část hry je plná cheaterů.
output: Příběh:gameplay:positive|multiplayerová část hry:gameplay:negative|cheaterů:community:negative
example 2-
input: Hra nabízí skvělý balanc mezi PvP a PvE a některé herní prvky jsou velmi zastaralé.
output: balanc mezi PvP a PvE:gameplay:positive|herní prvky:gameplay:negative
Now extract aspect:category:sentiment for the following example:
input: """
        if self.eos_instruction is None:
            self.eos_instruction = "\noutput: \n"
        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects, **kwargs):
        return (
                self.bos_instruction
                + input_text
                + self.eos_instruction
        )


class JointAspectSentimentInstruction(Instruction):
    def __init__(self, bos_instruction=None, eos_instruction=None):
        super().__init__(bos_instruction, eos_instruction)
        if self.bos_instruction is None:
            self.bos_instruction = f"""joint aspect sentiment extraction:
example 1-
input: Příběh je velmi zajímavý, ale multiplayerová část hry je plná cheaterů.
output: Příběh:gameplay:velmi zajímavý:positive|multiplayerová část hry:gameplay:plná cheaterů:negative|cheaterů:community:plná:negative
example 2-
input: Hra nabízí skvělý balanc mezi PvP a PvE no některé herní prvky jsou velmi zastaralé.
output: balanc mezi PvP a PvE:gameplay:skvělý:positive|herní prvky:gameplay:velmi zastaralé:negative
Now extract aspect:category:opinion:sentiment for the following example:
input: """
        if self.eos_instruction is None:
            self.eos_instruction = "\noutput: \n"
        if not self.bos_instruction:
            self.bos_instruction = bos_instruction
        if not self.eos_instruction:
            self.eos_instruction = eos_instruction

    def prepare_input(self, input_text, aspects, **kwargs):
        return (
                self.bos_instruction
                + input_text
                + self.eos_instruction
        )

#example 1-
# input: Příběh je velmi zajímavý ale multiplayerová část hry je plná cheaterů.
# output: Příběh:gameplay:velmi zajímavý:positive|multiplayerová část hry:gameplay:plná cheaterů:negative|cheaterů:community:plná:negative
# example 2-
# input: Hra nabízí skvělý balanc mezi PvP a PvE a některé herní prvky jsou velmi zastaralé.
# output: balanc mezi PvP a PvE:gameplay:skvělý:positive|herní prvky:gameplay:velmi zastaralé:negative
# example 3-
# input: Hra obsahuje rozne game mody, mapy a herni prvky.
# output: game mody:gameplay:rozne:neutral|mapy:gameplay:NULL:neutral|herni prvky:gameplay:NULL:neutral
# Now extract aspect:category:opinion:sentiment for the following example:
# example 4-
# input: Ziadne bugy hned od vydania, vynikajuce.
# output: bugy:preformance_bugs:Ziadne hned od vydania:positive
# Now extract aspect:category:opinion:sentiment for the following example:


# example 1-
# input: Příběh je velmi zajímavý, ale multiplayerová část hry je plná cheaterů.
# output: Příběh:gameplay:positive|multiplayerová část hry:gameplay:negative|cheaterů:community:negative
# example 2-
# input: Hra nabízí skvělý balanc mezi PvP a PvE a některé herní prvky jsou velmi zastaralé.
# output: balanc mezi PvP a PvE:gameplay:positive|herní prvky:gameplay:negative
# example 3-
# input: Hra obsahuje rozne game mody, mapy a herni prvky.
# output: game mody:gameplay:neutral|mapy:gameplay:neutral|herni prvky:gameplay:neutral
# example 4-
# input: Ziadne bugy hned od vydania, vynikajuce.
# output: bugy:preformance_bugs:positive
# Now extract aspect:category:sentiment for the following example:


# self.bos_instruction = f"""extract all aspect, category, opinion, sentiment quadruples from input video game review:
# example 1-
# input: Příběh je velmi zajímavý ale multiplayerová část hry je plná cheaterů.
# output: Příběh:gameplay:velmi zajímavý:positive|multiplayerová část hry:gameplay:plná cheaterů:negative|cheaterů:community:plná:negative
# example 2-
# input: Hra nabízí skvělý balanc mezi PvP a PvE a některé herní prvky jsou velmi zastaralé.
# output: balanc mezi PvP a PvE:gameplay:skvělý:positive|herní prvky:gameplay:velmi zastaralé:negative
# example 3-
# input: Hra obsahuje rozne game mody, mapy a herni prvky.
# output: game mody:gameplay:rozne:neutral|mapy:gameplay:NULL:neutral|herni prvky:gameplay:NULL:neutral
# Now extract aspect:category:opinion:sentiment for the following example:
# example 4-
# input: Ziadne bugy hned od vydania, vynikajuce.
# output: bugy:preformance_bugs:Ziadne hned od vydania:positive
# Now extract aspect:category:opinion:sentiment quadruples for the following example:
# input:


#             self.bos_instruction = f"""extract all aspect, category, sentiment triplets from input video game review:
# example 1-
# input: Příběh je velmi zajímavý, ale multiplayerová část hry je plná cheaterů.
# output: Příběh:gameplay:positive|multiplayerová část hry:gameplay:negative|cheaterů:community:negative
# example 2-
# input: Hra nabízí skvělý balanc mezi PvP a PvE a některé herní prvky jsou velmi zastaralé.
# output: balanc mezi PvP a PvE:gameplay:positive|herní prvky:gameplay:negative
# example 3-
# input: Hra obsahuje rozne game mody, mapy a herni prvky.
# output: game mody:gameplay:neutral|mapy:gameplay:neutral|herni prvky:gameplay:neutral
# example 4-
# input: Ziadne bugy hned od vydania, vynikajuce.
# output: bugy:preformance_bugs:positive
# Now extract aspect:category:sentiment for the following example:
# input: """