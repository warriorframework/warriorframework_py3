def test_warrior_utils_import():
    """
    util to test import of warrior exe and
    a function in it
    """
    from warrior.Framework.Utils import data_Utils, file_Utils
    from warrior.Framework.Utils.testcase_Utils import pNote
    from warrior.Framework.Utils.print_Utils import print_info, print_debug
    print_info("verifying whether print info is working, exception will be raised if this line fails")
    print_debug("verifying wether print_debug is working, exception will be raised if this line fails")
    pNote(file_Utils)
    pNote(data_Utils.get_credentials)
    
    return