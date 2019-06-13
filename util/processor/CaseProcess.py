from case.cases.base import BaseCase
from util.processor.process import Processor


class CaseProcessor(Processor):

    def add_case(self, case):
        if isinstance(case, BaseCase):
            self.sources.append(case)

