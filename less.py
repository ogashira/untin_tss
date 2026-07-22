from typing import List
from IThreshold import IThreshold

class Less(IThreshold):

    def calc_threshold(self, thresholds: List, val: float) -> int:
        thresholds.sort()

        resultThreshold = 0
        for threshold in thresholds:
            if threshold > val:
                resultThreshold = threshold
                break

        return resultThreshold
