from vectorbtpro import IndicatorFactory
from typing_ import IndicatorData


class IndicatorGenerator:
    def __init__(self, data: IndicatorData):
        self.close = data.get("Close")

    def run_indicators(self, indicator_params: dict[str, dict]):
        results = {}
        for name, params in indicator_params.items():
            factory = IndicatorFactory.from_talib(name)

            results[name] = factory.run(self.close, **params)
        return results
