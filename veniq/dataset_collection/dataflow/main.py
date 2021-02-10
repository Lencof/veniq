import os
from functools import lru_cache
from functools import partial
from pathlib import Path
from typing import Dict, Tuple

import bonobo

from veniq.dataset_collection.dataflow.preprocess import preprocess
from veniq.dataset_collection.dataflow.annotation import annotate
from veniq.dataset_collection.dataflow.find_inline_methods import find_EMS
from veniq.dataset_collection.dataflow.inlining import inline
from veniq.dataset_collection.dataflow.ncss_filter import filter_by_ncss


def get_list_of_files(path: str):
    test_files = set(Path(path).glob('**/*Test*.java'))
    not_test_files = set(Path(path).glob('**/*.java'))
    for x in not_test_files.difference(test_files):
        yield x


@lru_cache()
def create_dirs(output):
    def create_existing_dir(directory):
        if not directory.exists():
            directory.mkdir(parents=True)

    full_dataset_folder = Path(output) / 'full_dataset'
    output_dir = full_dataset_folder / 'output_files'
    create_existing_dir(output_dir)
    input_dir = full_dataset_folder / 'input_files'
    create_existing_dir(input_dir)
    return {'input_dir': input_dir, 'output_dir': output_dir}


def pass_params_to_next_node(dirs_dict, em_item: Dict[Tuple, Tuple]):
    class_name, invocation_line = list(em_item.keys())[0]
    ast, text, target_node, method_invoked, extracted_m_decl = list(em_item.values())[0]
    params_dict = {
        'ast': ast,
        'class_name': class_name,
        'invocation_line_number_in_original_file': invocation_line,
        'text': text,
        'target_node': target_node,
        'method_invoked': method_invoked,
        'extracted_m_decl': extracted_m_decl
    }

    yield {**params_dict, **dirs_dict}


def get_graph(**bonobo_args):
    output_dir = bonobo_args['output']
    dataset_dir = bonobo_args['dir']
    graph = bonobo.Graph()
    dirs = create_dirs(output_dir)
    em_dict = graph >> get_list_of_files(dataset_dir) >> preprocess >> find_EMS
    f_pass_params_to_next_node = partial(pass_params_to_next_node, dirs)
    em_dict >> f_pass_params_to_next_node >> filter_by_ncss >> annotate >> inline
    # TODO save file to output directory
    # TODO ignore overridden extracted functions, now it must be a different filter
    return graph


def get_services(**options):
    return {}


if __name__ == '__main__':
    system_cores_qty = os.cpu_count() or 1
    # argument_parser = ArgumentParser()

    # args = argument_parser.parse_args()

    bonobo_parser = bonobo.get_argument_parser()
    bonobo_parser.add_argument(
        "-d",
        "--dir",
        # required=True,
        help="File path to JAVA source code for methods augmentations",
        default='/d/mnt/temp/dataset/01'
    )
    bonobo_parser.add_argument(
        "-o", "--output",
        help="Path for file with output results",
        default='augmented_data'
    )
    bonobo_parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=system_cores_qty - 1,
        help="Number of processes to spawn. "
             "By default one less than number of cores. "
             "Be careful to raise it above, machine may stop responding while creating dataset.",
    )
    bonobo_parser.add_argument(
        "-z", "--zip",
        action='store_true',
        help="To zip input and output files."
    )
    bonobo_parser.add_argument(
        "-s", "--small_dataset_size",
        help="Number of files in small dataset",
        default=100,
        type=int,
    )
    with bonobo.parse_args(bonobo_parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options),
        )