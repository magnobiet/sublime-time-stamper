#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import datetime
import re


class TimeStamperCommand(sublime_plugin.TextCommand):

    def run(self, edit, user_input=None):

        self.edit = edit
        self.settings = sublime.load_settings('TimeStamper.sublime-settings')

        timestamp_str = datetime.datetime.now().strftime('/*! ' + self.settings.get('pattern') + ' */')
        acceptedPath = False
        acceptedExtension = False

        for path in self.settings.get('accepted_paths'):

            if path == '*':
                acceptedPath = True
                break

            rgPath = re.compile(path, re.IGNORECASE | re.DOTALL)
            rPath = rgPath.search(self.view.file_name())

            if rPath:
                acceptedPath = True
                break

        if not acceptedPath:
            return ''

        for ext in self .settings.get('accepted_extensions'):

            if self.view.file_name().endswith('.' + ext):
                acceptedExtension = True
                break

        if acceptedExtension:

            # Regex for verify Exists TimeStamp
            sTimeStamp = '(\\/\\*[\\d\\D]*?\\*\\/)'
            rg = re.compile(sTimeStamp, re.IGNORECASE | re.DOTALL)
            m = rg.search(self.view.substr(self.view.line(0)))

            # Exists, Replace this
            if m:

                # Regex Blank Spaces after TimeStamp
                rgSpaces = self.view.find(sTimeStamp + '+(\\n)', 0)
                erSpaces = re.search('(\\n\\n)', self.view.substr(
                    self.view.full_line(rgSpaces)))

                # No Blank Spaces, Add Blank Space before TimeStamp
                if erSpaces is None:
                    timestamp_str = timestamp_str + '\n'

                # Replace
                self.view.replace(edit, self.view.line(0), timestamp_str)

            else:
                # Add
                self.view.insert(edit, 0, timestamp_str + '\n\n')


class AddTimeStampWhenSaving(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.run_command('time_stamper')
