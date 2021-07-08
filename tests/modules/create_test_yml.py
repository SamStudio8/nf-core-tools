import os
import tempfile
import pytest

import nf_core.modules


def test_modules_custom_yml_dumper(self):
    """Try to create a yml file with the custom yml dumper"""
    out_dir = tempfile.mkdtemp()
    yml_output_path = os.path.join(out_dir, "test.yml")
    meta_builder = nf_core.modules.ModulesTestYmlBuilder("test/tool", False, "./", False, True)
    meta_builder.test_yml_output_path = yml_output_path
    meta_builder.tests = [{"testname": "myname"}]
    meta_builder.print_test_yml()
    assert os.path.isfile(yml_output_path)


def test_modules_test_file_dict(self):
    """Creat dict of test files and create md5 sums"""
    test_file_dir = tempfile.mkdtemp()
    meta_builder = nf_core.modules.ModulesTestYmlBuilder("test/tool", False, "./", False, True)
    with open(os.path.join(test_file_dir, "test_file.txt"), "w") as fh:
        fh.write("this line is just for testing")
    test_files = meta_builder.create_test_file_dict(test_file_dir)
    assert len(test_files) == 1
    assert test_files[0]["md5sum"] == "2191e06b28b5ba82378bcc0672d01786"


def test_modules_create_test_yml_get_md5(self):
    """Get md5 sums from a dummy output"""
    test_file_dir = tempfile.mkdtemp()
    meta_builder = nf_core.modules.ModulesTestYmlBuilder("test/tool", False, "./", False, True)
    with open(os.path.join(test_file_dir, "test_file.txt"), "w") as fh:
        fh.write("this line is just for testing")
    test_files = meta_builder.get_md5_sums(
        entry_point="dummy", command="dummy", results_dir=test_file_dir, results_dir_repeat=test_file_dir
    )
    assert test_files[0]["md5sum"] == "2191e06b28b5ba82378bcc0672d01786"


def test_modules_create_test_yml_entry_points(self):
    """Test extracting test entry points from a main.nf file"""
    meta_builder = nf_core.modules.ModulesTestYmlBuilder("star/align", False, "./", False, True)
    meta_builder.module_test_main = os.path.join(self.nfcore_modules, "tests", "software", "star", "align", "main.nf")
    meta_builder.scrape_workflow_entry_points()
    assert meta_builder.entry_points[0] == "test_star_align"


def test_modules_create_test_yml_check_inputs(self):
    """Test the check_inputs() function - raise UserWarning because test.yml exists"""
    cwd = os.getcwd()
    os.chdir(self.nfcore_modules)
    meta_builder = nf_core.modules.ModulesTestYmlBuilder("star/align", False, "./", False, True)
    meta_builder.module_test_main = os.path.join(self.nfcore_modules, "tests", "software", "star", "align", "main.nf")
    with pytest.raises(UserWarning) as excinfo:
        meta_builder.check_inputs()
    os.chdir(cwd)
    assert "Test YAML file already exists!" in str(excinfo.value)
