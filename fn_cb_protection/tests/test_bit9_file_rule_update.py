# -*- coding: utf-8 -*-
"""Tests using pytest_resilient_circuits"""

from __future__ import print_function
import pytest
from resilient_circuits.util import get_config_data, get_function_definition
from resilient_circuits import SubmitTestFunction, FunctionResult

PACKAGE_NAME = "fn_cb_protection"
FUNCTION_NAME = "bit9_file_rule_update"

# Read the default configuration-data section from the package
config_data = get_config_data(PACKAGE_NAME)

# Provide a simulation of the Resilient REST API (uncomment to connect to a real appliance)
resilient_mock = "pytest_resilient_circuits.BasicResilientMock"


def call_bit9_file_rule_update_function(circuits, function_params, timeout=10):
    # Fire a message to the function
    evt = SubmitTestFunction("bit9_file_rule_update", function_params)
    circuits.manager.fire(evt)
    event = circuits.watcher.wait("bit9_file_rule_update_result", parent=evt, timeout=timeout)
    assert event
    assert isinstance(event.kwargs["result"], FunctionResult)
    pytest.wait_for(event, "complete", True)
    return event.kwargs["result"].value


class TestBit9FileRuleUpdate:
    """ Tests for the bit9_file_rule_update function"""

    def test_function_definition(self):
        """ Test that the package provides customization_data that defines the function """
        func = get_function_definition(PACKAGE_NAME, FUNCTION_NAME)
        assert func is not None

    @pytest.mark.parametrize("bit9_file_rule_id, bit9_file_catalog_id, bit9_file_rule_name, bit9_file_rule_description, bit9_file_rule_filestate, bit9_file_rule_sourcetype, bit9_file_rule_policyids, bit9_file_rule_hash, expected_results", [
        (1, None, None, None, 2, 5, None, None, {"value": "xyz"})
    ])
    def test_success(self, circuits_app, bit9_file_rule_id, bit9_file_catalog_id, bit9_file_rule_name, bit9_file_rule_description, bit9_file_rule_filestate, bit9_file_rule_sourcetype, bit9_file_rule_policyids, bit9_file_rule_hash, expected_results):
        """ Test calling with sample values for the parameters """
        function_params = {
            "bit9_file_rule_id": bit9_file_rule_id,
            "bit9_file_catalog_id": bit9_file_catalog_id,
            "bit9_file_rule_name": bit9_file_rule_name,
            "bit9_file_rule_description": bit9_file_rule_description,
            "bit9_file_rule_filestate": bit9_file_rule_filestate,
            "bit9_file_rule_sourcetype": bit9_file_rule_sourcetype,
            "bit9_file_rule_policyids": bit9_file_rule_policyids,
            "bit9_file_rule_hash": bit9_file_rule_hash
        }
        results = call_bit9_file_rule_update_function(circuits_app, function_params)
        assert results is not None
