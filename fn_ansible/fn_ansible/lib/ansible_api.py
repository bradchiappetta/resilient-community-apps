# (c) Copyright IBM Corp. 2010, 2019. All Rights Reserved.
# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use

""" This module intends to provide a high level API 
for Ansible's core level modules and their functionalities.
"""



from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.module_utils._text import to_bytes
from ansible.parsing.vault import VaultSecret
import yaml
import os
import traceback


NUM_OF_FORKS = 5
VAULT_PASS_KEY = "vault_pass"
DEFAULT_VAULT_ID = "default"


def run_playbook(
        playbook_path,
        hosts_path,
        user_name,
        root_password,
        playbook_extra_vars,
        playbook_become_method,
        playbook_become_user,
        vault_password_file=None,
        connection_type="smart",
    ):  # pylint: disable= too-many-arguments, too-many-locals

    """This function is responsible for running a playbook
    and returns the results of the queries that the playbook
    contains.
    """

    loader = DataLoader()
    if vault_password_file:
        vault_password = read_secret(vault_password_file, VAULT_PASS_KEY)
        loader.set_vault_secrets(
            [(DEFAULT_VAULT_ID, VaultSecret(_bytes=to_bytes(vault_password)))]
        )
    inventory = InventoryManager(loader=loader, sources=hosts_path)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    if playbook_extra_vars:
        variable_manager.extra_vars = playbook_extra_vars

    passwords = {"become_pass": root_password}

    Options = namedtuple(                  # pylint: disable= invalid-name
        "Options",
        [
            "connection",
            "remote_user",
            "ask_sudo_pass",
            "verbosity",
            "ack_pass",
            "module_path",
            "forks",
            "become",
            "become_method",
            "become_user",
            "check",
            "listhosts",
            "listtasks",
            "listtags",
            "syntax",
            "sudo_user",
            "sudo",
            "diff",
        ],
    )
    options = Options(
        connection=connection_type,
        remote_user=user_name,
        ack_pass=None,
        sudo_user=None,
        forks=NUM_OF_FORKS,
        sudo=None,
        ask_sudo_pass=False,
        verbosity=5,
        module_path=None,
        become=True,
        become_method=playbook_become_method,
        become_user=playbook_become_user,
        check=False,
        diff=False,
        listhosts=None,
        listtasks=None,
        listtags=None,
        syntax=None,
    )

    playbook = PlaybookExecutor(
        playbooks=playbook_path,
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords,
    )

    result = {}
    try:
        playbook.run()
        stats = playbook._tqm._stats    # pylint: disable= protected-access
        hosts = sorted(stats.processed.keys())
        for host in hosts:
            result = {host: stats.summarize(host)}
    except Exception as original_exception:
        original_error = traceback.format_exc(original_exception)
        caution_text = "> That didn't work, please check 3 important things: \
        \n\t > 1. Configuration in app.config file \n\t \
        > 2. Playbook variables provided in correct format without extra space \
        \n\t > 3. Playbook syntax."
        raise ValueError(original_error + "\n\t" + caution_text)

    return result


def read_secret(file_path, key):
    """ This method returns vault password stored in a YML file """

    if os.path.exists(file_path):
        with open(file_path) as f_p:
            data = yaml.safe_load(f_p)
        return data[key]
    else:
        raise ValueError("File not present in following path: '%s'" % file_path)
