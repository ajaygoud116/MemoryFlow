from retrieval.retriever import retrieve_memories

from benchmarking.retrieval_metrics import (
    compute_recall_at_k,
    compute_precision_at_k,
    compute_mrr,
    compute_ndcg_at_k
)



def evaluate_retrieval(
    store,
    test_cases,
    k=5
):

    results = []


    for case in test_cases:


        query = case["query"]

        relevant_texts = case["relevant_texts"]

        relevant_ids = [
            m.memory_id

            for m in store.get_memories(active_only=False)
            if m.text.strip().lower() in
                [t.strip().lower() for t in relevant_texts]

        ]


        retrieved = retrieve_memories(
            store,
            query,
            top_k=k
        )


        retrieved_ids = [

            memory.memory_id

            for memory, score

            in retrieved

        ]


        # DEBUG
        print("\nQUERY:", query)
        print(
            "RETRIEVED:",
            retrieved_ids
        )

        print(
            "EXPECTED:",
            relevant_ids
        )


        results.append({

            "query": query,


            "recall@k":

                compute_recall_at_k(
                    retrieved_ids,
                    relevant_ids,
                    k
                ),


            "precision@k":

                compute_precision_at_k(
                    retrieved_ids,
                    relevant_ids,
                    k
                ),


            "mrr":

                compute_mrr(
                    retrieved_ids,
                    relevant_ids
                ),


            "ndcg@k":

                compute_ndcg_at_k(

                    retrieved_ids,

                    {
                        rid:1
                        for rid in relevant_ids
                    },

                    k

                )

        })


    return results