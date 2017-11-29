#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for PPP package."""
import unittest
import doctest
import os
import signal
import subprocess
from argparse import ArgumentParser

from pmix.ppp.odkform import OdkForm
from pmix.ppp.odkprompt import OdkPrompt
from pmix.ppp.odkgroup import OdkGroup
# from pmix.odkchoices import OdkChoices  # TODO
# from pmix.odkrepeat import OdkRepeat  # TODO
# from pmix.odktable import OdkTable  # TODO

TEST_PACKAGES = ['pmix.ppp', 'test']
TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
TEST_FILES_DIR = TEST_DIR + 'files/'


# # Mock Objects
class MockForm(OdkForm):
    """Mock object of OdkForm"""

    def __init__(self, mock_file, mock_dir=None):
        """Initialize mock form.

        Args:
            mock_file (str): File name.
            mock_dir (str): Directory.
        """
        path = mock_dir + mock_file if mock_dir else TEST_FILES_DIR + mock_file
        form = super().from_file(path)
        super().__init__(form)


# # Unit Tests
# pylint: disable=too-few-public-methods
# - PyLint check not apply? - http://pylint-messages.wikidot.com/messages:r0903
class PppTest:
    """Base class for PPP package tests."""

    @staticmethod
    def get_forms(data):
        """Convert specified forms from form name strings to objects."""
        forms = {}
        for datum in data:
            # Should streamline setUps. Currently in both tuple and dict.
            try:
                file = datum[0]['file']
            except KeyError:
                file = datum['inputs']['file']
            if file not in forms:
                forms[file] = OdkForm.from_file(TEST_FILES_DIR + file)
        return forms


class OdkPromptTest(unittest.TestCase, PppTest):
    """Unit tests for the OdkPrompt class."""

    media_types = ['image', 'audio', 'video', 'media::image',
                   'media::audio', 'media::video']
    media_lead_char = '['
    media_end_char = ']'
    arbitrary_language_param = 'English'

    def setUp(self):
        """Set up."""
        self.data = (
            ({'inputs': {
                'file': 'FQ.xlsx'
            }, 'expected_outputs': {

            }},
             {'inputs': {
                 'file': 'HQ.xlsx'
             }, 'expected_outputs': {

             }},
            )
        )

    def test_to_dict(self):
        """Test to_dict method."""
        def test_media_fields_in_prompts():
            """Tests for media fields."""
            def asserts(item_dict):
                """Iterate through asserts."""
                for key, val in item_dict.items():
                    for media_type in OdkPromptTest.media_types:
                        if key.startswith(media_type) and val:
                            # A field such as 'media::image::English'
                            # is formatted correctly.
                            self.assertTrue(val[0] == lead_char and
                                            val[-1] == end_char)
                            # A field such as 'image' exists and is
                            # formatted correctly.
                            self.assertTrue(
                                item_dict[media_type][0] == lead_char and
                                item_dict[media_type][-1] == end_char)
                            # No discrepancies between language based and non
                            # language based media fields.
                            self.assertTrue(item_dict[media_type] == val)
                            # The field 'media' exists and formatted correct.
                            self.assertTrue(item_dict['media'])
            lang = OdkPromptTest.arbitrary_language_param
            lead_char = OdkPromptTest.media_lead_char
            end_char = OdkPromptTest.media_end_char
            forms = self.get_forms(self.data)
            for i in self.data:
                file_name = i['inputs']['file']
                for item in forms[file_name].questionnaire:
                    if isinstance(item, OdkPrompt):
                        asserts(item.to_dict(lang))

        test_media_fields_in_prompts()

    def test_initialization_has_choices(self):
        """Test that choice list exists on initialization."""
        forms = self.get_forms(self.data)
        for dummy, form in forms.items():
            for item in form.questionnaire:
                if isinstance(item, OdkPrompt):
                    if item.odktype in item.select_types:
                        msg = 'No choices found in \'{}\'.'.format(item)
                        self.assertTrue(item.choices is not None, msg=msg)


class OdkGroupTest(unittest.TestCase):
    """Unit tests for the OdkGroup class."""

    def setUp(self):
        """Set up."""
        self.data = (
            ({'inputs': {'type': 'begin group', 'name': 'date_group',
                         'label::English': '', 'hint::English': '',
                         'constraint_message::English': '', 'constraint': '',
                         'required': '', 'appearance': 'field-list',
                         'default': '',
                         'relevant': 'today() > date("2017-03-01") and '
                                     'today() < date("2017-11-01")',
                         'read_only': '', 'calculation': '', 'choice_filter':
                             '', 'image::English': '',
                         'save_instance': '', 'save_form': '', 'label::Ateso':
                             '', 'label::Luganda': '',
                         'label::Lugbara': '', 'label::Luo': '',
                         'label::Lusoga': '', 'label::Ngakarimojong': '',
                         'label::Runyankole-Rukiga': '',
                         'label::Runyoro-Rutoro': '', 'hint::Ateso': '',
                         'hint::Luganda': '', 'hint::Lugbara': '', 'hint::Luo':
                             '', 'hint::Lusoga': '',
                         'hint::Ngakarimojong': '', 'hint::Runyankole-Rukiga':
                             '', 'hint::Runyoro-Rutoro': '',
                         'constraint_message::Ateso': '',
                         'constraint_message::Luganda': '',
                         'constraint_message::Lugbara': '',
                         'constraint_message::Luo': '',
                         'constraint_message::Lusoga': '',
                         'constraint_message::Ngakarimojong': '',
                         'constraint_message::Runyankole-Rukiga': '',
                         'constraint_message::Runyoro-Rutoro': '',
                         'label': '', 'hint': '', 'constraint_message': '',
                         'image': '', 'constraint_original': '',
                         'relevant_original': 'today() > date("2017-03-01") '
                                              'and today() < date("2017-11-01"'
                                              ')',
                         'input_field': None},
              'outputs': {
                  'header_primitive_type': type({})
              }}),
        )

    def test_render_header(self):
        """Test header rendering."""
        for i in self.data:
            expected_output = i['outputs']['header_primitive_type']
            output = type(OdkGroup(i['inputs']).format_header(i['inputs']))
            msg = '\n\nCase:\n{}\nOutput:\n{}\nExpected:\n{}'\
                .format(i, output, expected_output)
            self.assertTrue(output == expected_output, msg=msg)


class OdkFormTest(unittest.TestCase, PppTest):
    """Unit tests for the OdkForm class."""

    def setUp(self):
        """Set up."""
        self.data = (
            {'inputs': {'file': 'OdkFormTest.xlsx'}, 'position': 0,
             'outputs': {'class': OdkPrompt,
                         'repr': '<OdkPrompt ever_birth>'}},
            {'inputs': {'file': 'OdkFormTest.xlsx'}, 'position': 1,
             'outputs': {'class': OdkGroup,
                         'repr': '<OdkGroup FB: [<OdkPrompt fb_note>, '
                                 '<OdkPrompt fb_m>, <OdkPrompt fb_y>]>'}},
            {'inputs': {'file': 'OdkFormTest.xlsx'}, 'position': 2,
             'outputs': {'class': OdkPrompt,
                         'repr': '<OdkPrompt birth_events_yes>'}},
            {'inputs': {'file': 'OdkFormTest.xlsx'}, 'position': 3,
             'outputs': {'class': OdkPrompt,
                         'repr': '<OdkPrompt children_living>'}},
        )

    def test_questionnaire(self):
        """Test expected results of converted questionnaire based on position.
        """
        forms = self.get_forms(self.data)

        for datum in self.data:
            expected_output = datum['outputs']
            output = \
                forms[datum['inputs']['file']].questionnaire[datum['position']]

            # - Check Object Representation
            got = str(output)
            expected = expected_output['repr']
            msg = '\nGot: {}\nExpected: {}'.format(got, expected)
            self.assertEqual(got, expected, msg)

            # - Check Object Class
            got = output
            expected = expected_output['class']
            msg = '\nGot: {}\nExpected: {}'.format(got, expected)
            # noinspection PyTypeChecker
            self.assertTrue(isinstance(got, expected), msg)


class MultiConversionTest(unittest.TestCase):
    """Test conversion of n files in n languages for n option combinations."""

    @staticmethod
    def ls(_dir):
        """Call LS on a directory."""
        proc = subprocess.Popen(['ls', _dir, '-l'], stdout=subprocess.PIPE,
                                shell=True,
                                preexec_fn=os.setsid)
        ls = proc.stdout.read().decode('UTF-8').split('\n')
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        return ls

    def test_multi_conversion(self):
        src_dir = TEST_FILES_DIR + 'multiple_file_language_option_conversion/'
        out_dir = src_dir + 'ignored/'
        src_dir_ls_input = MultiConversionTest.ls(src_dir)
        src_files = \
            [src_dir + x for x in src_dir_ls_input if x.endswith('.xlsx')]
        subprocess.call(['rm', '-rf', out_dir])
        subprocess.call(['mkdir', out_dir])
        subprocess.call(['python', '-m', 'pmix.ppp'] + src_files +
                        ['-o', out_dir, '-f', 'doc', '-p', 'minimal',
                         '-l', 'English', 'Français'])
        out_dir_ls_input = MultiConversionTest.ls(out_dir)
        expected_output = \
            "['/Users/joeflack4/projects/pmix_dev/test/files/mu" \
            "ltiple_file_language_option_conversion/ignored/:'," \
            " 'BFR5-Female-Questionnaire-v13-jef-English-minima" \
            "l.doc', 'BFR5-Female-Questionnaire-v13-jef-Françai" \
            "s-minimal.doc', 'BFR5-Household-Questionnaire-v13-" \
            "jef-English-minimal.doc', 'BFR5-Household-Question" \
            "naire-v13-jef-Français-minimal.doc', 'BFR5-Listing" \
            "-v1-jef-English-minimal.doc', 'BFR5-Listing-v1-jef" \
            "-Français-minimal.doc', 'BFR5-Reinterview-Question" \
            "naire-v13-jef-English-minimal.doc', 'BFR5-Reinterv" \
            "iew-Questionnaire-v13-jef-Français-minimal.doc', '" \
            "BFR5-SDP-Questionnaire-v13-jef-English-minimal.doc" \
            "', 'BFR5-SDP-Questionnaire-v13-jef-Français-minima" \
            "l.doc', 'BFR5-Selection-v2-jef-English-minimal.doc" \
            "', 'BFR5-Selection-v2-jef-Français-minimal.doc', '']"
        self.assertEqual(str(out_dir_ls_input), expected_output)


def get_args():
    """CLI for PPP test runner."""
    desc = 'Run tests for PPP package.'
    parser = ArgumentParser(description=desc)
    doctests_only_help = 'Specifies whether to run doctests only, as ' \
                         'opposed to doctests with unittests. Default is' \
                         ' False.'
    parser.add_argument('-d', '--doctests-only', action='store_true',
                        help=doctests_only_help)
    args = parser.parse_args()
    return args


def get_test_modules(test_package):
    """Get files to test.

    Args:
        test_package (str): The package containing modules to test.

    Returns:
        list: List of all python modules in package.

    """
    if test_package == 'pmix.ppp':  # TODO: Make dynamic.
        root_dir = TEST_DIR + "../" + "pmix/ppp"
    elif test_package == 'test':
        root_dir = TEST_DIR
    else:
        raise Exception('Test package not found.')

    test_modules = []
    for dirpath, dummy, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filename = filename[:-3]
                sub_pkg = dirpath.replace(root_dir, '').replace('/', '.')
                test_module = test_package + sub_pkg + '.' + filename
                test_modules.append(test_module)
    return test_modules


def get_test_suite(test_packages):
    """Get suite to test.

    Returns:
        TestSuite: Suite to test.

    """
    suite = unittest.TestSuite()
    for package in test_packages:
        pkg_modules = get_test_modules(test_package=package)
        for pkg_module in pkg_modules:
            suite.addTest(doctest.DocTestSuite(pkg_module))
    return suite


if __name__ == '__main__':
    PARAMS = get_args()
    TEST_SUITE = get_test_suite(TEST_PACKAGES)
    unittest.TextTestRunner(verbosity=1).run(TEST_SUITE)

    if not PARAMS.doctests_only:
        unittest.main()
