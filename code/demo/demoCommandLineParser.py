from code.core.enumerations import *
from code.commandLine.commandLineParser import CommandLineParser 

class DemoBase(object):
    showHelpAndProblems = False
    @enumeration
    class Protocol:
        tcp = None
        udp = None
    # classProtocol
    @staticmethod
    def descriptionValidator(option):
        if not ' ' in option.value.strip():
            return "Description cannot be in one word"
    @staticmethod
    def pathValidator(option):
        if ';' in option.value or ':' in option.value:
            return "Path cannot contain delimiters"
# DemoBase

class Demo(DemoBase):

    @enumeration
    class DescriptorPropertyOptions:
        Version = CommandLineParser.OptionDescriptor(
            # both names may miss,
            # then enumeration member names becomes full option name
            description = "Version: Show program version and exit",
            valueModality = CommandLineParser.OptionValueModality.MustUseValuelessOptionOnly)
        Help = CommandLineParser.OptionDescriptor(
            "help", description = "Help: Give usage message and exit",
            valueModality = CommandLineParser.OptionValueModality.MustUseValuelessOptionOnly)
        Recursive = CommandLineParser.OptionDescriptor(
            abbreviatedName = "R",
            multiplicity = CommandLineParser.Multiplicity.mandatory(),
            valueModality = CommandLineParser.OptionValueModality.MustUseSignOnly)
        Protocol = CommandLineParser.OptionDescriptor(
            "protocol", "p",
            # description can be missing
            values = DemoBase.Protocol,
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly)
        SearchPath = CommandLineParser.OptionDescriptor(
            "search-path", "s", description = "Search Path",
            multiplicity = CommandLineParser.Multiplicity.any(),
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly,
            validator = DemoBase.pathValidator)
        Output = CommandLineParser.OptionDescriptor(
            "output", "o", description = "Output file",
            default = ".",
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly)
        Description = CommandLineParser.OptionDescriptor(
            "description", description = "Description of the use case",
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly,
            validator = DemoBase.descriptionValidator)
    # class DescriptorPropertyOptions

    @classmethod
    def demo(self):
        parser = CommandLineParser()
        input = ["--help", "--something-wrong", "f1", "f2", "--", "-", "--protocol:tcp", "--help", "--help:2", "--description:just-word"]
        input = ["--something-wrong", "--help+", "f1", "f2", "-s:ha;ha", "-s:3", "-s:3"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        print("Command line syntax: " + parser.result.EBNF)
        print(str())
        parser.result.showHelp()
        if not parser.result.hasProblems():
            return
        print(str())
        print("Problems:")
        print(str())
        access = parser.result.options 
        parser.result.showProblems()
        print("Files: " + str(parser.result.fileList))
        res = access[self.DescriptorPropertyOptions.Output]
        cnt = len(access)
        ss = str(access)
        print("Options: " + ss)
        #
        optionList = []
        for option in access:
            optionList.append("{0}: '{1}'".format(option, option.value))
        print("Option iterator demo: " + ", ".join(optionList))
    # demo

# Demo

Demo.demo()
