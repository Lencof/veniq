from pathlib import Path # use Path
from unittest import TestCase # use TestCase

from veniq.utils.timeout import invoke_with_timeout
from veniq.dataset_collection.validation import fix_start_end_lines_for_opportunity, \
    percent_matched

# create class TestValidation(TestCase):
class TestValidation(TestCase):
    folder = Path(__file__).absolute().parent

    # create def test_validation_semi_2_closing_brackets_with_2_lines_before_block(self):
    def test_validation_semi_2_closing_brackets_with_2_lines_before_block(self):
        file = self.folder / "DynaMenuModel.java"
        # range doesn't include the last item
        # also, add it as it would be numbered starting at 1
        lines_extracted_by_semi = list(range(91, 109))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((91, 108), fixed_lines)

    # create def test_validation_semi_2_closing_brackets_without_lines_before_block(self):
    def test_validation_semi_2_closing_brackets_without_lines_before_block(self):
        file = self.folder / "BaseTextEditor.java"
        # range doesn't include the last item
        # also, add it as it would be numbered starting at 1
        lines_extracted_by_semi = list(range(58, 62))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((58, 63), fixed_lines)

    # create def test_semi_no_need_to_find_closing_brackets(self):
    def test_semi_no_need_to_find_closing_brackets(self):
        file = self.folder / "User.java"
        lines_extracted_by_semi = list(range(17, 22))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((17, 21), fixed_lines)

    # create def test_validation_semi_closing_brackets_with_2_blocks(self):
    def test_validation_semi_closing_brackets_with_2_blocks(self):
        file = self.folder / "CssPreprocessors.java"
        lines_extracted_by_semi = list(range(32, 38))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((32, 39), fixed_lines)

    # create def test_validation_semi_1_closing_brackets(self):
    def test_validation_semi_1_closing_brackets(self):
        file = self.folder / "NameNodeRpcServer.java"
        lines_extracted_by_semi = list(range(232, 235))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((232, 235), fixed_lines)

        file = self.folder / "MetadataEncoder.java"
        lines_extracted_by_semi = list(range(51, 55))
        fixed_lines = fix_start_end_lines_for_opportunity(
            lines_extracted_by_semi,
            str(file)
        )
        self.assertEqual((51, 55), fixed_lines)

    # create def test_get_percent_matched(self):
    def test_get_percent_matched(self):
        semi_lines = list(range(50, 58))
        dataset_lines = list(range(50, 58))
        percent = percent_matched(dataset_lines, semi_lines)
        self.assertEqual(percent, 1.0)

    # create def_test__percent_partially_matched(self):    
    def test_percent_partially_matched(self):
        semi_lines = list(range(65, 81))
        dataset_lines = list(range(69, 82))
        percent = percent_matched(dataset_lines, semi_lines)
        self.assertEqual(percent, 12 / 13)

    # create def test_perecent_not_matched(self):
    def test_percent_not_matched(self):
        semi_lines = list(range(65, 68))
        dataset_lines = list(range(69, 82))
        percent = percent_matched(dataset_lines, semi_lines)
        self.assertEqual(percent, 0)

    # create def test_lines_match_semi_line_is_full_subset_of_dataset_lines(self):    
    def test_lines_match_semi_line_is_full_subset_of_dataset_lines(self):
        semi_lines = list(range(24, 45))
        dataset_lines = list(range(27, 41))
        percent = percent_matched(dataset_lines, semi_lines)
        self.assertEqual(percent, 1.0)

        semi_lines = list(range(78, 99))
        dataset_lines = list(range(72, 121))
        percent = percent_matched(dataset_lines, semi_lines)
        self.assertEqual(percent, 0.42857142857142855)

    # create def test_validation_semi_1_line_large_return(self):    
    def test_validation_semi_1_line_large_return(self):
        file = self.folder / "WebClasspathPanel.java"
        lines_extracted_by_semi = list(range(35, 36))
        fixed_lines = invoke_with_timeout(
            5,
            fix_start_end_lines_for_opportunity,
            lines_extracted_by_semi,
            file
        )
        self.assertEqual((35, 46), fixed_lines)
