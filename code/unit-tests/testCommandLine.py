import unittest, sys, os
from code.core.enumerations import *
from code.commandLine.commandLineParser import CommandLineParser 

class CommandLineTestBase(unittest.TestCase):
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
# CommandLineTestBase

class CommandLineTest(CommandLineTestBase):
    
    @enumeration
    class OptionsInvalidNameWithBlankSpace:
         First = CommandLineParser.OptionDescriptor("1 2", str())
    @enumeration
    class OptionsInvalidNameBadStart:
         First = CommandLineParser.OptionDescriptor("--3", str())
    @enumeration
    class OptionsInvalidNameTab:
         First = CommandLineParser.OptionDescriptor("4\t5", str())
    @enumeration
    class OptionsNonUniqueShortName:
        First = CommandLineParser.OptionDescriptor("CoolStory", "a")
        Duplicate = CommandLineParser.OptionDescriptor("CoolStory", "b")
    @enumeration
    class OptionsNonUniqueLongName:
        First = CommandLineParser.OptionDescriptor("First", "f")
        Second = CommandLineParser.OptionDescriptor("Second", "f")
    @enumeration
    class OptionsEmptyNames:
         First = CommandLineParser.OptionDescriptor(str(), str())
    badNameMetadataSet = [
        OptionsInvalidNameWithBlankSpace,
        OptionsInvalidNameBadStart,
        OptionsInvalidNameTab,
        OptionsNonUniqueShortName,
        OptionsNonUniqueLongName]

    @enumeration
    class OptionsInvalidMultiplicity:
        First = CommandLineParser.OptionDescriptor("First", "f",
            multiplicity=str())
    @enumeration
    class OptionsInvalidModality:
        First = CommandLineParser.OptionDescriptor("First", "f",
            valueModality=str())
    @enumeration
    class OptionsInvalidValueSet:
        First = CommandLineParser.OptionDescriptor("First", "f",
            values = ["one", "two", "tree"])
    badOptionDescriptorMetadataSet = [OptionsInvalidMultiplicity, OptionsInvalidModality, OptionsInvalidValueSet]

    @enumeration
    class TrivialOptions:
        First = CommandLineParser.OptionDescriptor("First", "f", description = "First thing to do")
        Second = CommandLineParser.OptionDescriptor("Second", "s", description = "Not to forget the second one", multiplicity = CommandLineParser.Multiplicity.mandatory())

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
            abbreviatedName = "R", description = "Recursive: Operate recursively (down directory tree)",
            multiplicity = CommandLineParser.Multiplicity.mandatory(),
            valueModality = CommandLineParser.OptionValueModality.MustUseSignOnly)
        protocol = CommandLineParser.OptionDescriptor(
            # description can be missing
            values = CommandLineTestBase.Protocol,
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly)
        Output = CommandLineParser.OptionDescriptor(
            "output", "o", description = "Output file",
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly)
        Description = CommandLineParser.OptionDescriptor(
            "description", description = "Description of the use case",
            valueModality = CommandLineParser.OptionValueModality.MustUseValueOnly,
            validator = CommandLineTestBase.descriptionValidator)
    # class DescriptorPropertyOptions

    def testParserInputValidation(self):
        parser = CommandLineParser()
        try:
            badInput = str()
            parser.Parse(self.TrivialOptions, badInput)
        except TypeError:
            try:
                badInput = [0, 0]
                parser.Parse(self.TrivialOptions, badInput)
            except TypeError:
                return
            self.fail("Exception ValueError should be thrown on non-string command-line option: " + str(type(badInput)))      
            return
        self.fail("Exception ValueError should be thrown on invalid input type: " + str(type(badInput)))      
    # testParserInputValidation

    def testRaiseOnBadNames(self):
        parser = CommandLineParser()
        for metadata in self.badNameMetadataSet:
            try:
                parser.Parse(metadata, [])
            except ValueError:
                continue
            self.fail("Exception ValueError should be thrown on bad options metadata: " + str(metadata))
        # but!
        parser.Parse(self.OptionsEmptyNames, ["no-option"])
        self.assertTrue(parser.result)
    # testRaiseOnBadNames

    def testRaiseOnBadOptionDescriptor(self):
        parser = CommandLineParser()
        for metadata in self.badOptionDescriptorMetadataSet:
            try:
                parser.Parse(metadata, [])
            except TypeError:
                continue
            self.fail("Exception TypeError should be thrown on bad options metadata: " + str(metadata))
    # testRaiseOnBadOptionDescriptor

    def testParsingResult(self):
        parser = CommandLineParser()
        input = ["-a-", "--", "-", "--", "--First:1", "-f:2", "-First-", "--First-"]
        parser.Parse(self.TrivialOptions, input)
        self.assertTrue(parser.result.options)
        self.assertEqual(len(parser.result.options), 2)
        count = 0
        for value in parser.result.options:
            if value != None:
                count += 1
        self.assertTrue(count, 3)
        self.assertTrue(parser.result.unrecognizedOptions)
        self.assertTrue(parser.result.options[self.TrivialOptions.First].optionInput, "--First:1")
        self.assertEqual(len(parser.result.unrecognizedOptions), 5)
    # testParsingResult

    def testHelp(self):
        parser = CommandLineParser()
        input = ["--help", "--something-wrong", "--", "-" "--protocol", "--help", "--help:2", "--description:just-one-word"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        saveStdout = sys.stdout
        if not self.showHelpAndProblems:
            print("To see help and description of parsing result problems, either change assign showHelpAndProblems = True or run demoCommandLineParser.py")
            sys.stdout = open(os.devnull, 'w')
        try:
            print("Command line syntax: " + parser.result.EBNF)
            print(str())
            parser.result.showHelp()
            if not parser.result.hasProblems():
                return
            print(str())
            print("Problems:")
            print(str())
            parser.result.showProblems()
        finally:
            saveStdout = sys.stdout
    # testHelp

    def testInvalidOptions(self):
        parser = CommandLineParser()
        input = ["--protocol:tcp", "--protocol", "--protocol-", "-o:good", "--help"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        self.assertFalse(parser.result.invalidOptions)
        input = ["--protocol:http", "--protocol", "--protocol-", "-o:good", "--help"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        self.assertEquals(len(parser.result.invalidOptions), 1)
        self.assertEquals(parser.result.invalidOptions[0].option.value, "http")
        input = ["--protocol:http", "--description:long enough"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        self.assertEquals(len(parser.result.invalidOptions), 1)
        input = ["--protocol", "--description:just-one-word"]
        parser.Parse(self.DescriptorPropertyOptions, input)
        self.assertEquals(len(parser.result.invalidOptions), 2)
    # testInvalidOptions

# class CommandLineTest

if __name__ == '__main__':
    unittest.main()