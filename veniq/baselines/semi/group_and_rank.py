from typing import List, Tuple

from veniq.baselines.semi.grouping_size import is_similar_size
from veniq.baselines.semi.overlap import is_overlap


def _temp_hasMoreBenefitThan(
        oport_1: Tuple[int, int],
        oport_2: Tuple[int, int]) -> bool:
    """
    Temporary method implementing fitness function for
    ranking hypotheses.
    To be substituted with a real implementation.
    Returns True if oport_1 has more benefit than oport_2
    """
    return True


def _temp_fitness_f(opport: Tuple[int, int]) -> float:
    """
    Actually, this function also needs to have access to the whole
    method body. We will fix it in the next PR.
    """
    return 1.0


def in_same_group(
        oport_1: Tuple[int, int],
        oport_2: Tuple[int, int],
        max_size_difference: float = 0.2,
        min_overlap: float = 0.1) -> bool:
    """
    Checks if two oportunuties should be grouped,
    by checking overlap and size difference.
    """
    simil_size = is_similar_size(oport_1, oport_2,
                                 max_size_difference=max_size_difference)
    overlap = is_overlap(oport_1, oport_2, min_overlap=min_overlap)
    return simil_size and overlap


def group_and_rank_in_groups(
        oportunities: List[Tuple[int, int]],
        **kwargs) -> List[Tuple[int, int]]:
    """
        Implements Fig.7 in the paper. Groups oportunities
        and selects primary per group. Returns the set
        of primary oportunities
    """
    alternatives = set()

    for i, oport_1 in enumerate(oportunities):
        if i in alternatives:
            continue

        for j in range(i + 1, len(oportunities)):
            oport_2 = oportunities[j]
            if oport_2 in alternatives:
                continue

            if in_same_group(oport_1, oport_2, **kwargs):
                if _temp_hasMoreBenefitThan(oport_1, oport_2):
                    alternatives.add(j)
                else:
                    alternatives.add(i)

    primary_opport_indices = set(range(len(oportunities))) - alternatives
    return [oportunities[i] for i in primary_opport_indices]


def output_best_opportunities(
        opportunities: List[Tuple[int, int]],
        top_k: int = 5,
        **kwargs) -> List[Tuple[int, int]]:
    """
    Runs grouping and ranking to produce the set of 'primanry oportunities'.
    Given the final list, outputs top-k according to the fitness functon.
    """
    primary_opportunities = group_and_rank_in_groups(opportunities, **kwargs)
    primary_opportunities_eval = {o: _temp_fitness_f(o) for o in
                                  primary_opportunities}
    sorted_oport = sorted(
        primary_opportunities_eval.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return [x[0] for x in sorted_oport[:top_k]]
