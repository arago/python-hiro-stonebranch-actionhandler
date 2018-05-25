from docopt import docopt


class DocoptBuilder:
    def __init__(self) -> None:
        super().__init__()
        self.description = None
        self.usages = []
        self.options = []
        self.arguments = []
        self.escs = []  # exit status code s
        self.environments = []
        self.files = []
        self.examples = []

    def build(self, program_name: str, short_name: str) -> docopt:
        result = []
        if self.description is not None:
            result.append(self.description)
            result.append('')
        result.append('Usage:')
        for usage in self.usages:
            result.append('  ' + usage)
        if len(self.options) > 0:
            result.append('')
            if len(self.options) == 1:
                result.append('Option:')
            else:
                result.append('Options:')
            first_len = 0
            for option in self.options:  # type: str
                if '\t' in option:
                    option_len = len(option.split('\t')[0])
                else:
                    option_len = len(option)
                if option_len > first_len:
                    first_len = option_len
            self.options.sort()
            for option in self.options:
                if '\t' in option:
                    fmt = '  %%-%us  %%s' % first_len
                    args = tuple(option.split('\t'))
                    result.append(fmt % args)
                else:
                    result.append('  %s' % option)
        if len(self.arguments) > 0:
            result.append('')
            if len(self.arguments) == 1:
                result.append('Argument:')
            else:
                result.append('Arguments:')
            for argument in self.arguments:
                result.append('  ' + argument)
        if len(self.escs) > 0:
            result.append('')
            if len(self.escs) == 1:
                result.append('Exit Status Value:')
            else:
                result.append('Exit Status Values:')
            for exit_status_code in self.escs:
                result.append('  ' + exit_status_code)
        if len(self.environments) > 0:
            result.append('')
            if len(self.environments) == 1:
                result.append('Environment Variables:')
            else:
                result.append('Environment Variable:')
            for environment_variable in self.environments:
                result.append('  ' + environment_variable)
        if len(self.files) > 0:
            result.append('')
            if len(self.files) == 1:
                result.append('File:')
            else:
                result.append('Files:')
            for file in self.files:
                result.append('  ' + file)
        if len(self.examples) > 0:
            result.append('')
            if len(self.examples) == 1:
                result.append('Example:')
            else:
                result.append('Examples:')
            for example in self.examples:
                result.append('  ' + example)

        raw_doc = '\n'.join(result)
        formatted_doc = raw_doc.format(program_name=program_name, short_name=short_name)
        return docopt(doc=formatted_doc)  # see http://docopt.org
