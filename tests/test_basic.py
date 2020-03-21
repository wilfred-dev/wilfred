####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

from click.testing import CliRunner
from wilfred.wilfred import cli


def test_basic():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, "--version")

    assert result.exit_code == 0


def test_path():
    runner = CliRunner()
    result = runner.invoke(cli, "--path")

    assert result.exit_code == 0
