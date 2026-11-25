"""Loading and validation of the word class configuration files (`.json`).

   Convention: an optional field that does not apply is simply omitted
   from the config file.  Code should test for it with `config.get(key)`
   or `key in config`, never by comparing against a sentinel like "None".

"""

import json

from fstmorph.src.log import info

REQUIRED_FIELDS = [
    "pos",
    "morphology_source_path",
    "regular_csv_files",
    "irregular_csv_files",
    "lexical_database",
    "regular_lexc_file",
    "morph_features",
    "missing_tag_marker",
    "missing_form_marker",
    "multichar_symbols",
]

OPTIONAL_FIELDS = [
    "irregular_lexc_file",
    "pre_element",
    "pre_element_template_path",
    "pre_element_source_path",
    "pre_element_lexical_database",
    "derivational_csv_file",
]

# Fields that only make sense together: either all are given or none is.
PRE_ELEMENT_FIELDS = ["pre_element", "pre_element_template_path",
                      "pre_element_source_path"]

# Values which older config files used to mean "not specified".
LEGACY_EMPTY_VALUES = ["", "None", "NONE", None]


def load_config(config_file):
    """Read `config_file`, check it, and return it as a dict.

       Optional fields holding a legacy "empty" value ("", "None",
       "NONE" or null) are dropped, so that downstream code only has to
       check whether a key is present.

    """
    with open(config_file) as f:
        config = json.load(f)

    missing = [key for key in REQUIRED_FIELDS if key not in config]
    if missing:
        raise ValueError(f"{config_file}: missing required field(s): "
                         f"{', '.join(missing)}")

    for key in ["lexical_database"]:
        if config[key] in LEGACY_EMPTY_VALUES:
            raise ValueError(f"{config_file}: required field '{key}' "
                             f"cannot be empty")

    for key in OPTIONAL_FIELDS:
        if key in config and config[key] in LEGACY_EMPTY_VALUES:
            info(f"{config_file}: '{key}' is set to {config[key]!r}; "
                 f"omit the field instead.")
            del config[key]

    present = [key for key in PRE_ELEMENT_FIELDS if key in config]
    if present and len(present) != len(PRE_ELEMENT_FIELDS):
        raise ValueError(f"{config_file}: {', '.join(PRE_ELEMENT_FIELDS)} "
                         f"must be given together, but only "
                         f"{', '.join(present)} present")

    return config
