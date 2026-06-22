import math


def compute_recall_at_k(
    retrieved,
    relevant,
    k
):

    if not relevant:
        return 0.0


    retrieved_k = retrieved[:k]


    hits = sum(
        1
        for item in retrieved_k
        if item in relevant
    )


    return hits / len(relevant)



def compute_precision_at_k(
    retrieved,
    relevant,
    k
):

    retrieved_k = retrieved[:k]


    if len(retrieved_k) == 0:
        return 0.0


    hits = sum(
        1
        for item in retrieved_k
        if item in relevant
    )


    return hits / len(retrieved_k)



def compute_mrr(
    retrieved,
    relevant
):

    for rank,item in enumerate(retrieved):

        if item in relevant:

            return 1 / (rank + 1)


    return 0.0



def compute_dcg(relevances):

    dcg = 0.0

    for i, rel in enumerate(relevances):

        dcg += ((2**rel - 1)/math.log2(i + 2))

    return dcg



def compute_ndcg_at_k(
    retrieved,
    relevance_map,
    k
):

    retrieved_k = retrieved[:k]


    actual = [
        relevance_map.get(
            item,
            0
        )
        for item in retrieved_k
    ]


    dcg = compute_dcg(
        actual
    )


    ideal = sorted(
        relevance_map.values(),
        reverse=True
    )[:k]


    idcg = compute_dcg(
        ideal
    )


    if idcg == 0:

        return 0.0


    return round(dcg / idcg,4)