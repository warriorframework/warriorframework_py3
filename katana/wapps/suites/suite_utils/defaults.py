from katana.utils.dict_utils import invert_dict


def executiontypes():
    return {
        "Sequential Cases": "sequential_testcases",
        "Parallel Cases": "parallel_testcases",
        "Iterative Sequential Cases": "iterative_sequential",
        "Iterative Parallel Cases": "iterative_parallel",
        "Run Multiple Times": "run_multiple",
        "Run Until Pass": "run_until_pass",
        "Run Until Failure": "run_until_failure"
    }


def executiontypes_list():
    return [key for key in executiontypes()]


def inverted_executiontypes():
    return invert_dict(executiontypes())


def inverted_executiontypes_list():
    return [key for key in inverted_executiontypes()]


def runtypes():
    return {
        "Sequential Keywords": "sequential_keywords",
        "Parallel Keywords": "parallel_keywords"
    }


def runtypes_list():
    return [key for key in runtypes()]


def inverted_runtypes():
    return invert_dict(runtypes())


def inverted_runtypes_list():
    return [key for key in inverted_runtypes()]


def runmodes():
    return {
        "Standard": "standard",
        "Run Multiple Times": "rmt",
        "Run Until Pass": "rup",
        "Run Until Failure": "ruf"
    }


def runmodes_list():
    return [key for key in runmodes()]


def inverted_runmodes():
    return invert_dict(runmodes())


def inverted_runmodes_list():
    return [key for key in inverted_runmodes()]


def on_errors():
    return {
        "Next": "next",
        "Abort": "abort",
        "Abort As Error": "abort_as_error",
        "Go To": "goto"
    }


def on_errors_list():
    return [key for key in on_errors()]


def inverted_on_errors():
    return invert_dict(on_errors())


def inverted_on_errors_list():
    return [key for key in inverted_on_errors()]


def contexts():
     return {
        "Positive": "positive",
        "Negative": "negative"
    }


def contexts_list():
    return [key for key in contexts()]


def inverted_contexts():
    return invert_dict(contexts())


def inverted_contexts_list():
    return [key for key in inverted_contexts()]


def impacts():
    return {
        "Impact": "impact",
        "No Impact": "noimpact"
    }


def impacts_list():
    return [key for key in impacts()]


def inverted_impacts():
    return invert_dict(impacts())


def inverted_impacts_list():
    return [key for key in inverted_impacts()]


def states_list():
    return ["New", "Test-Assigned", "Released"]


def execute_types_list():
    return ["Yes", "No", "If", "If Not"]