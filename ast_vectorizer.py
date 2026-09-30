import ast
import numpy as np

AST_NODE_TYPES = [
    "Module", "FunctionDef", "arguments", "arg", "Assign", "AugAssign",
    "For", "Name", "Constant", "Load", "Store", "Add", "Return",
    "If", "Compare", "While", "Expr", "Call", "Attribute", "Subscript"
]

def extract_ast_features(code: str) -> np.ndarray:
    feature_vector = np.zeros(len(AST_NODE_TYPES))
    
    try:
        parsed_tree = ast.parse(code)
        for node in ast.walk(parsed_tree):
            node_type = type(node).__name__
            if node_type in AST_NODE_TYPES:
                idx = AST_NODE_TYPES.index(node_type)
                feature_vector[idx] += 1
    except Exception:
        pass
        
    norm = np.linalg.norm(feature_vector)
    if norm > 0:
        feature_vector = feature_vector / norm
        
    return feature_vector
