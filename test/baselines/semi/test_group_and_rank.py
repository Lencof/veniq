from unittest import TestCase

from veniq.baselines.semi.group_and_rank import (
    in_same_group,
    group_and_rank_in_groups,
    output_best_oportunities)


class GroupAndRankTest(TestCase):
    oport_0 = (3, 5)
    oport_1 = (2, 32)
    oport_2 = (2, 34)
    oport_3 = (33, 50)
    oport_4 = (35, 50)
    oport_5 = (55, 65)

    opportunities = [(3, 4), (13, 14), (11, 14), (30, 34), (31, 34)]
    line_to_semantic_dict = {
        3: ['length', 'rcs'],
        4: ['length', 'i', 'rcs'],
        5: [],
        6: ['rcs', 'i'],
        7: ['rcs', 'rec', 'i', 'grabRes'],
        9: ['rcs', 'rec', 'i', 'grabNonFileSetRes'],
        11: ['length', 'rec', 'j'],
        12: ['rec', 'j', 'getName', 'replace'],
        13: ['rcs', 'i'],
        14: ['rcs', 'i'],
        15: ['afs', 'equals', 'getFullpath', 'getProj'],
        16: ['name.afs', 'getProj', 'getFullpath'],
        17: ['afs', 'equals', 'getProj', 'getPref'],
        18: ['afs', 'getPref', 'getProj'],
        19: ['pr', 'endsWith'],
        20: ['pr'],
        22: ['name', 'pr'],
        25: ['MANIFEST_NAME', 'name', 'equalsIgnoreCase'],
        26: ['j', 'manifests', 'rec', 'i'],
        30: ['manifests', 'i'],
        31: ['manifests', 'i'],
        34: ['manifests']
    }

    def test_in_same_group_1(self):
        self.assertTrue(in_same_group(self.oport_1, self.oport_2))

    def test_in_same_group_2(self):
        self.assertTrue(in_same_group(self.oport_3, self.oport_4))

    def test_not_in_same_group(self):
        self.assertFalse(in_same_group(self.oport_0, self.oport_5))

    def test_diff_in_size(self):
        self.assertFalse(in_same_group(self.oport_0, self.oport_1))

    def test_not_overlap(self):
        self.assertFalse(in_same_group(self.oport_2, self.oport_3))

    def test_not_overlap_custom(self):
        self.assertTrue(in_same_group(self.oport_3, self.oport_4))
        self.assertFalse(in_same_group(self.oport_3, self.oport_4,
                                       min_overlap=0.9))

    def test_group_and_rank_in_groups(self):
        selected_primary = group_and_rank_in_groups(
            self.line_to_semantic_dict,
            self.opportunities,
            max_size_difference=0.25
        )

        expect_primary = [(3, 4), (13, 14), (11, 14), (31, 34)]
        self.assertEqual(set(selected_primary), set(expect_primary))

    def test_output_best_oportunities_top3(self):
        expect_top3 = [(3, 4), (13, 14), (11, 14)]
        select_top3 = output_best_oportunities(self.line_to_semantic_dict,
                                               self.opportunities,
                                               top_k=3,
                                               max_size_difference=0.25)
        self.assertEqual(set(expect_top3), set(select_top3))
