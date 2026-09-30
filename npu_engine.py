import onnxruntime as ort
import numpy as np

class SnapdragonNPUEngine:
    def __init__(self):
        self.providers = [
            ('QNNExecutionProvider', {'backend_path': 'QnnHtp.dll', 'htp_performance_mode': 'high_performance'}),
            'DmlExecutionProvider',
            'CPUExecutionProvider'
        ]
        print("[+] Snapdragon NPU Engine initialized.")

    def compute_ast_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm_a = np.linalg.norm(vec1)
        norm_b = np.linalg.norm(vec2)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))
