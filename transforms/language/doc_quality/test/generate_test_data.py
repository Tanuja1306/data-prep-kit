import json

import pyarrow as pa
from data_processing.data_access import DataAccessLocal
from test_docquality import TestDocQualityTransform


"""
input table:
"""
table = pa.Table.from_pydict(
    {"document_id": pa.array(["doc01"]), "contents": pa.array([" : This documents is for test . ? "])}
)


"""
expected output table:
"""
# copy expected_table from the input_df
schema = table.schema
data = table.to_pydict()
expected_table = pa.Table.from_pydict(data, schema=schema)
expected_table = expected_table.append_column("docq_total_words", pa.array([8]))
expected_table = expected_table.append_column("docq_mean_word_len", pa.array([3.125]))
expected_table = expected_table.append_column("docq_symbol_to_word_ratio", pa.array([0.0]))
expected_table = expected_table.append_column("docq_sentence_count", pa.array([1]))
expected_table = expected_table.append_column("docq_lorem_ipsum_ratio", pa.array([0.0]))
expected_table = expected_table.append_column("docq_curly_bracket_ratio", pa.array([0.0]))
expected_table = expected_table.append_column("docq_contain_bad_word", pa.array([False]))
expected_table = expected_table.append_column("docq_bullet_point_ratio", pa.array([0.0]))
expected_table = expected_table.append_column("docq_ellipsis_line_ratio", pa.array([0.0]))
expected_table = expected_table.append_column("docq_alphabet_word_ratio", pa.array([0.625000]))
expected_table = expected_table.append_column("docq_contain_common_en_words", pa.array([False]))
expected_table = expected_table.append_column("metakenlm_docq_perplex_score", pa.array([6709.1]))

expected_metadata_list = [{"total_docs_count": 1}, {}]


# This main() is run to generate the test data file whenever the test data defined in TestDocQualityTransform changes.
# It generates the test and out put data into the input and expected directories.
if __name__ == "__main__":
    config = {"input_folder": "../test-data", "output_folder": "../test-data"}
    data_access = DataAccessLocal(config, [], False, -1)
    inp = table
    out = expected_table
    data_access.save_table("../test-data/input/test1.parquet", inp)
    data_access.save_table("../test-data/expected/test1.parquet", out)

    with open("../test-data/expected/metadata.json", "w") as json_file:
        json.dump(expected_metadata_list, json_file)
