import sublime
import sublime_plugin
import re


class ExpandAbbreviationCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = sublime.active_window().active_view()
        r = self.view.sel()[0]
        empty_region = r.empty()
        line = view.substr(sublime.Region(r.b, r.b - 2))
        if empty_region and (line == "++" or
                             line == "--" or
                             line == "+=" or
                             line == "-=" or
                             line == "*=" or
                             line == "/=" or
                             line == "%="):
            begin_line = self.view.full_line(r).a
            region_text = sublime.Region(begin_line, self.view.sel()[0].b - 2)
            prec_text = view.substr(region_text)
            if re.search(r'([\w]+\s?)$', prec_text):
                word = re.search(r'([\w]+\s?)$', prec_text).group(1)
                postfix = ""
                if line == "++":
                    postfix = " + 1;"
                elif line == "--":
                    postfix = " - 1;"
                elif line == "+=":
                    postfix = " + "
                elif line == "-=":
                    postfix = " - "
                elif line == "*=":
                    postfix = " * "
                elif line == "/=":
                    postfix = " / "
                elif line == "%=":
                    postfix = " % "
                snippet = word + " = " + word + postfix
                begin_word = self.view.sel()[0].b - len(word) - 2
                region = sublime.Region(begin_word, self.view.sel()[0].b)
                self.view.replace(edit, region, snippet)
                return
        elif not empty_region:
            self.view.run_command('indent')
            return

        self.view.insert(edit, self.view.sel()[0].b, '\t')
