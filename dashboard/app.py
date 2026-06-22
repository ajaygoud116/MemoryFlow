import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from memory_store.store import MemoryStore
from pipeline.memoryflow import run_memoryflow
from benchmarking.benchmark import calculate_metrics


st.set_page_config(
    page_title="MemoryFlow Dashboard",
    layout="wide"
)

store = MemoryStore()

st.title(" MemoryFlow Dashboard")
st.caption("Importance-Aware Hierarchical Context Compression")



with st.sidebar:
    st.header(" Controls")

    query = st.text_input("Query", value="travel recommendations")

    run_btn = st.button(" Run MemoryFlow")

    st.markdown("---")
    st.info("Paste conversation below and run pipeline")


with st.container(border=True):
    st.subheader("Conversation Input")

    conversation_text = st.text_area(
        "Enter one memory per line",
        height=180,
        value="""My budget is $2500
I am allergic to shellfish
I prefer luxury hotels
I want to visit Switzerland"""
    )

conversation = [
    line.strip()
    for line in conversation_text.split("\n")
    if line.strip()
]



if "generated_context" not in st.session_state:
    st.session_state.generated_context = ""


if run_btn:
    st.session_state.generated_context = run_memoryflow(
        conversation,
        query,
        store
    )
    st.toast("MemoryFlow executed successfully ")


with st.container(border=True):
    st.subheader("Query Result")

    if st.session_state.generated_context:

        st.markdown(f"**Query:** `{query}`")

        st.success(st.session_state.generated_context)

    else:
        st.warning("Run MemoryFlow to generate results.")



metrics = calculate_metrics(store)

col1, col2, col3, col4 = st.columns(4)

col1.metric(" Total Memories", metrics["total_memories"])
col2.metric(" Active Memories", metrics["active_memories"])
col3.metric(" Archived", metrics["archived_memories"])
col4.metric(" Compression", f"{metrics['compression_ratio']}%")



with st.container(border=True):
    st.subheader(" Tier Distribution")

    tier_df = pd.DataFrame({
        "Tier": list(metrics["tier_distribution"].keys()),
        "Count": list(metrics["tier_distribution"].values())
    })

    if len(tier_df) > 0:
        st.bar_chart(tier_df.set_index("Tier"))
    else:
        st.info("No tier data available.")


with st.container(border=True):
    st.subheader("Memory Explorer")

    memories = store.get_memories(active_only=False)

    rows = []

    for m in memories:
        rows.append({
            "ID": m.memory_id,
            "Status": "Active" if m.active else "Archived",
            "Tier": m.tier,
            "AMIS": round(m.amis_score, 2),
            "Topic": m.topic,
            "Value": m.value,
            "Count": m.retrieval_count,
        })

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No memories stored yet.")


with st.container(border=True):
    st.subheader(" Memory Timeline")

    for m in memories:
        with st.expander(f"{m.topic} • Tier {m.tier} • ID {m.memory_id}"):

            colA, colB = st.columns(2)

            with colA:
                st.write("**Original**")
                st.code(m.text)

            with colB:
                st.write("**Compressed**")
                st.code(m.compressed_text)

            st.caption(f"""
AMIS Score: {m.amis_score}  
Frequency: {m.frequency_score}  
Recency: {m.recency_score}
""")

            if m.metadata:
                st.json(m.metadata)