from .azure import AzureOperator, AzureModels
from .gemini import GeminiOperator, GeminiModels
from .operator import Operator
from enum import StrEnum

def new_operator(model: StrEnum) -> Operator:
    if type(model) is AzureModels:
        return AzureOperator(model)
    elif type(model) is GeminiModels:
        return GeminiOperator(model)
    else:
        raise ValueError(f"Unknown operator {model}")
