from autogen import register_function
from .registry import TOOL_REGISTRY


def load_and_register_tools(
    tool_names: list[str],
    caller,
    executor,
    auto_desc: bool = True
) -> list[str]:
    """Charge et enregistre uniquement les outils demandés."""
    available = set(TOOL_REGISTRY.keys())
    missing = [t for t in tool_names if t not in available]
    if missing:
        raise ValueError(f"🚫 Tools not found: {missing}. Available: {list(available)}")

    registered = []
    for name in tool_names:
        func = TOOL_REGISTRY[name]
        desc = f"{name} tool" if auto_desc else ""
        register_function(func, caller=caller, executor=executor, description=desc)
        registered.append(name)
        
    print(f"🔧 Registered: {registered}")
    return registered