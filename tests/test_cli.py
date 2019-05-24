"""Tests for our main skele CLI module."""

from subprocess import PIPE, Popen


class TestHelp:
    def test_returns_usage_information(self):
        output = Popen(['arte_dl', '-h'], stdout=PIPE).communicate()[0]
        assert b'usage' in output

        output = Popen(['arte_dl', '--help'], stdout=PIPE).communicate()[0]
        assert b'usage' in output
