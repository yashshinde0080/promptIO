from frameworks.standard import StandardFramework
from frameworks.reasoning import ReasoningFramework
from frameworks.race import RACEFramework
from frameworks.care import CAREFramework
from frameworks.ape import APEFramework
from frameworks.create import CREATEFramework
from frameworks.tag import TAGFramework
from frameworks.creo import CREOFramework
from frameworks.rise import RISEFramework
from frameworks.pain import PAINFramework
from frameworks.coast import COASTFramework
from frameworks.roses import ROSESFramework
from frameworks.resee import RESEEFramework

FRAMEWORK_REGISTRY = {
    "standard": StandardFramework(),
    "reasoning": ReasoningFramework(),
    "race": RACEFramework(),
    "care": CAREFramework(),
    "ape": APEFramework(),
    "create": CREATEFramework(),
    "tag": TAGFramework(),
    "creo": CREOFramework(),
    "rise": RISEFramework(),
    "pain": PAINFramework(),
    "coast": COASTFramework(),
    "roses": ROSESFramework(),
    "resee": RESEEFramework(),
}


def get_framework(name: str):
    framework = FRAMEWORK_REGISTRY.get(name.lower())
    if not framework:
        raise ValueError(f"Unknown framework: {name}. Available: {list(FRAMEWORK_REGISTRY.keys())}")
    return framework