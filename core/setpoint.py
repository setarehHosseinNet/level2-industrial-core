class SetpointCalculator:
    def calculate(self, length, width, material):
        base_temp = 1200 if material == "ST37" else 1250
        return base_temp + 0.1 * length * width