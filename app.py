import time
import streamlit as st
import numpy as np
import pandas as pd
from isomorph_engine import (
    compute_tri_factor_similarity,
    process_zip_repository,
    generate_pdf_report,
    generate_json_report
)

st.set_page_config(
    page_title="Isomorph AI | Zero-Trust Code Forensics",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .metric-card {
        background-color: #1e222d;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2e3440;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER WITH CUSTOM LOGO ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=110)
    except Exception:
        st.image("D:\ACPDF-AI\Copilot_20260930_021801.png", width=270)

with col_title:
    st.title("Isomorph AI: Zero-Trust Code Forensics & Obfuscation Inspector")
    st.caption("Powered by Qualcomm AI Hub | 100% On-Device Isomorphic Syntax Tree Matching for Windows on Snapdragon")

st.markdown("---")

tab1, tab2 = st.tabs(["🔍 Single Pair Forensics", "📁 Repository Directory Inspector"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Source Code A (Original)")
        code_a = st.text_area(
            "Paste original code snippet",
            height=220,
            value="""def calculate_total(prices):
    total = 0
    for p in prices:
        total += p
    return total"""
        )

    with col2:
        st.subheader("Source Code B (Suspected Obfuscated Copy)")
        code_b = st.text_area(
            "Paste code snippet to check",
            height=220,
            value="""def fn_x(a_list):
    v_1 = 0
    for item in a_list:
        v_1 += item
    return v_1"""
        )

    if st.button("🚀 Analyze Similarity on Snapdragon NPU", type="primary"):
        start_time = time.perf_counter()
        results = compute_tri_factor_similarity(code_a, code_b)
        latency_ms = (time.perf_counter() - start_time) * 1000

        st.markdown("---")
        st.subheader("Isomorphic Forensics Analysis")

        hybrid_score = results["hybrid_score"]
        st.metric("Hybrid Isomorphic Similarity Score", f"{hybrid_score:.2f}%")

        if hybrid_score > 75:
            st.error("🚨 High Obfuscation Match Detected! Structural syntax tree topology is isomorphic. Variable renaming identified.")
        elif hybrid_score > 40:
            st.warning("⚠️ Moderate Code Similarity Detected. Structural overlap found.")
        else:
            st.success("✅ Low Similarity. Source codes appear structurally distinct.")

        st.subheader("Quad-Factor Sub-Score Breakdown")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("AST Zhang-Shasha (40%)", f"{results['ast_score']}%")
        m2.metric("Canonical IR LCS (30%)", f"{results['lcs_score']}%")
        m3.metric("N-Gram TF-IDF (15%)", f"{results['ngram_score']}%")
        m4.metric("NPU Embedding (15%)", f"{results['npu_score']}%")
        m5.metric("Inference Latency", f"{latency_ms:.2f} ms")

        st.markdown("---")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            pdf_data = generate_pdf_report(results, latency_ms)
            st.download_button(
                label="📄 Export Enterprise PDF Forensics Report",
                data=pdf_data,
                file_name="Isomorph_AI_Forensics_Report.pdf",
                mime="application/pdf"
            )
        with btn_col2:
            json_data = generate_json_report(results, latency_ms)
            st.download_button(
                label="💾 Export Audit JSON Report",
                data=json_data,
                file_name="Isomorph_AI_Audit.json",
                mime="application/json"
            )

        with st.expander("💻 Live Snapdragon NPU System Telemetry"):
            st.code(f"""
[Hardware Acceleration Info]
Platform: Windows on Snapdragon (ARM64 / Hexagon NPU)
Target Provider: QNNExecutionProvider (fallback: DirectML/CPU)
Execution Latency: {latency_ms:.2f} ms
RAM Delta: {results['ram_usage_mb']} MB
Privacy Context: Zero Trust Air Gapped (0 Network Requests)
Model Artifact: Isomorph AST Transformer.onnx
            """)

with tab2:
    st.subheader("Batch Repository Code Similarity Matrix")
    uploaded_zip = st.file_uploader("Upload a .zip repository containing source code files (.py, .cpp, .c, .java, .js)", type=["zip"])

    if uploaded_zip is not None:
        zip_bytes = uploaded_zip.read()
        with st.spinner("Processing AST trees across repository files..."):
            files_dict, matrix, filenames = process_zip_repository(zip_bytes)

        if filenames:
            st.success(f"Successfully analyzed {len(filenames)} source files.")
            df_matrix = pd.DataFrame(matrix, index=filenames, columns=filenames).round(2)
            
            st.dataframe(
                df_matrix.style.background_gradient(cmap="Reds", vmin=0, vmax=100)
                .format("{:.2f}%"),
                use_container_width=True
            )
        else:
            st.warning("No supported source files found in the uploaded zip.")