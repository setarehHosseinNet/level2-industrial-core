class QualityEvaluator:
    def evaluate(self, temp_end):
        if 840 <= temp_end <= 950:
            return "OK"
        return "NOK"
