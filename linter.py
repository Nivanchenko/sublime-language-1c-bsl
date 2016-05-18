"""This module exports the OneScriptLint plugin class."""

import sublime
import os
from SublimeLinter.lint import Linter, util

class OneScriptLint(Linter):
    """Provides an interface to OneScriptLint."""

    syntax = '1c'
    cmd = ('oscript -encoding=utf-8 -check @')
    regex = r'\{\S+\s+(?P<error>.*)\s\/\s.*:\s+(?P<line>\d+)\s+\/\s+(?P<message>.*)\}'
    error_stream = util.STREAM_BOTH
    comment_re = r'\s*//'

    def run(self, cmd, code):
        lintOtherExtensions = sublime.load_settings('Language 1C (BSL).sublime-settings').get('lintOtherExtensions')
        linterEntryPoint = sublime.load_settings('Language 1C (BSL).sublime-settings').get('linterEntryPoint')
        filePath = self.filename
        arrFilePath = filePath.split('.')
        if len(arrFilePath) == 0:
            return
        extension = arrFilePath[len(arrFilePath) - 1];
        if not extension == 'os' and lintOtherExtensions.find(extension) == -1:
            return

        if not linterEntryPoint == '':
            project_path = ''
            projectPaths = sublime.active_window().folders()
            for projectPath in projectPaths:
                if filePath.find(projectPath) > -1:
                    project_path = projectPath;
                    break

            cmd.append("-env=" + os.path.join(project_path, linterEntryPoint))
        
        return self.communicate(cmd, code)
