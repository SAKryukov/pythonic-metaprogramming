import sys
from code.core.enumerations import *

class DefinitionSet:
    # |, * and all brackets are BNF metasymbols: |()[]<>, but + is part of syntax:
    EBNF = "((--<optionName>|-<shortOptionName>)[+|-|:<value>])*"
    BNF = [
        "<command-line-element> ::= <option> | <file>",
        "<option> ::= <option-identifier> | <on-option> | <off-option> | <value-option>,",
        "<file> ::= <value>",
        "<option-identifier> ::= --<optionName>|-<shortOptionName>",
        "<on-option> ::= <option-identifier>+",
        "<off-option> ::= <option-identifier>-",
        "<value-option> ::= <option-identifier>:<value>",
        "<optionName> ::= <identifier>",
        "<shortOptionName> ::= <identifier>",
        "<identifier> ::= <non-space-character> | <non-space-character><identifier>",
        "<value> ::= <character>|<value>"
    ]
    abbreviatedOptionPrefix = '-'
    optionPrefix = abbreviatedOptionPrefix + abbreviatedOptionPrefix
    plus = '+'
    minus = '-'
    valueDelimiter = ':'
    helpDelimiter = valueDelimiter
    helpValidValuesProlog = "Valid:"
    helpValueNotation = "<value>"
    helpValueDelimiter = " "
    optionValueDelimiter = ", "
    infinity = float("infinity")
    regexOptionNameValidator = r"[\s]"
    exceptionEnumerationType = "Expected enumeration type"
    exceptionInputList = "Expected list"
    exceptionInputListElement = "All input list elements must be strings"
    exceptionOptionNameType = "Option names must be strings"
    exceptionInvalidOptionName = "Invalid option name"
    exceptionNonUniqueOptionName = "Option name is not unique"
    exceptionValueModalityType = "Modality must be of enumeration member type CommandLineParser.OptionValueModality"
    exceptionMultiplicityType = "Multiplicity must be of enumeration member type CommandLineParser.Multiplicity"
    invalidValueFormatSignValue = "Option should take the form {0}{1}{2}, {0}{1}{3} or {0}{1}:<value>"
    invalidValueFormatSign = "Option should take the form {0}{1}{2} or {0}{1}{3}"
    invalidValueFormatValue = "Option should take the form {0}{1}:<value>"
    invalidValueFormatNoSign = "For {0}{1}, {2}/{3} Option form is not allowed"
    invalidValueFormatNoValue = "Value option form {0}{1}:<value> is not allowed"
    invalidValueFormat = "Invalid value: {0}"
    titleUnrecognizedOptions = "Unrecognized options: "
    titleMissingOptions = "Missing options: "
    titleInvalidOptions = "Invalid options:"
    titleFormatInvalidOption = "\t'{0}' {1}"
    titleDuplicateOptions = "Duplicate options: "
    formatOptionStateMissing = "<Missing>"  
    formatOptionStateDefault = "<Default>"  
    formatOptionStateDefaultOn = "<On>"  
    formatOptionStateDefaultValueString = "<Default> '{}'"  
    formatOptionStateDefaultValue = "<Default> {}"  
    formatOptionStateDefaultInvalid = "<Invalid>"  
    formatOptionValue = "'{}'"  
    formatOptionPair = "'{0}': {1}"
    @staticmethod
    def listToString(lst): # for ParsingResult.showProblems()
        return str(lst).strip('[]')
    optionModalityBitOption = 1 << 0
    optionModalityBitSign = 1 << 1
    optionModalityBitValue = 1 << 2
    optionModalityBitAny = optionModalityBitOption | optionModalityBitSign | optionModalityBitValue
# class DefinitionSet

class CommandLineParserBase(object):
    class Multiplicity:
        def __init__(self, min, max):
            self.min = min
            self.max = max
        @classmethod
        def any(cls):
            return cls(0, DefinitionSet.infinity)
        @classmethod
        def optional(cls):
            return cls(0, 1)
        @classmethod
        def mandatory(cls):
            return cls(1, 1)
    # class Multiplicity
    @enumeration
    class OptionValueModality: # if present; presence itself is described by OptionDescriptor.multiplicity
        Default = DefinitionSet.optionModalityBitAny
        MustUseValuelessOptionOnly = DefinitionSet.optionModalityBitOption
        MustUseSignOnly = DefinitionSet.optionModalityBitSign
        MustUseValueOnly = DefinitionSet.optionModalityBitValue
        MustNotUseValuelessOption = DefinitionSet.optionModalityBitSign | DefinitionSet.optionModalityBitValue 
        MustNotUseSign = DefinitionSet.optionModalityBitOption | DefinitionSet.optionModalityBitValue
        MustNotUseValue = DefinitionSet.optionModalityBitOption | DefinitionSet.optionModalityBitSign
    # class OptionValueModality
    @enumeration
    class DefaultValidValueSet:
        pass
# class CommandLineParserBase

class CommandLineParser(CommandLineParserBase):
    
    # interface:

    @enumeration
    class OptionState:
        Unspecified =   None # not mentioned in command line
        Invalid =       None
        Missing =       None # mandatory but not mentioned in command line
        Default =       None # -opt or --option
        Plus =          None # -opt+ or --option+ 
        Minus =         None # -opt- or --option-
        Value =         None # -opt:someString or --option:someString or "-opt:some String" or "--option:some String" 
        File =          None # "some string" or someString, no - or --
    # class OptionState

    class OptionDescriptor: # part of option-defining metadata
        def __init__(
                self,
                fullName = None, abbreviatedName = None,
                multiplicity = CommandLineParserBase.Multiplicity.optional(),
                valueModality = CommandLineParserBase.OptionValueModality.Default,
                description = str(),
                default = None,
                values = CommandLineParserBase.DefaultValidValueSet,
                validator = lambda option : None # returns string if a problem
            ):
                self.fullName = fullName
                self.abbreviatedName = abbreviatedName
                self.multiplicity = multiplicity 
                self.valueModality = valueModality
                self.description = description
                self.default = default
                self.values = values
                self.validator = validator
                if Enum.IsInstanceOfEnumerationType(values) and len(values) > 0:
                    self.valueModality.value |= DefinitionSet.optionModalityBitValue
        # constructor
    # class OptionDescriptor

    class Option: # result of parsing
        def __init__(
            self,
            descriptor,
            optionInput, name, abbreviatedForm, optionState,
            value):
                self.descriptor = descriptor
                self.optionInput = optionInput
                self.name = name
                self.abbreviatedForm = abbreviatedForm
                self.optionState = optionState
                self.value = value
        # constructor
        def __str__(self):
            return self.name
    # class Option

    class ParsingResult:
        def __init__(self, options, unrecognizedOptions, missingOptions, duplicateOptions, fileList, invalidOptions, help):
            self.options = options
            self.unrecognizedOptions = unrecognizedOptions
            self.missingOptions = missingOptions 
            self.duplicateOptions = duplicateOptions
            self.fileList = fileList
            self.invalidOptions = invalidOptions
            self.help = help
            #
            self.EBNF = DefinitionSet.EBNF
            self.BNF = DefinitionSet.BNF
        def showHelp(self):
            for line in self.help:
                print(line)
        def isValid(self):
            return not (self.invalidOptions or self.missingOptions) 
        def hasProblems(self):
            return self.unrecognizedOptions or self.duplicateOptions or not self.isValid()            
        def showHelp(self):
            for line in self.help:
                print(line)
        def showProblems(self):
            if self.hasProblems():
                self.showUnrecognizedOptions()    
                self.showMissingOptions()    
                self.showInvalidOptions()    
                self.showDuplicateOptions()    
        # implementation detail:
        def showUnrecognizedOptions(self):
            if self.unrecognizedOptions:
                print(DefinitionSet.titleUnrecognizedOptions + DefinitionSet.listToString(self.unrecognizedOptions))
        def showMissingOptions(self):
            if self.missingOptions:
                print(DefinitionSet.titleMissingOptions + DefinitionSet.listToString(self.missingOptions))
        def showInvalidOptions(self):
            if self.invalidOptions:
                print(DefinitionSet.titleInvalidOptions)
                for element in self.invalidOptions:
                    print(DefinitionSet.titleFormatInvalidOption.format(element.option.optionInput, element.problem))
        def showDuplicateOptions(self):
            if self.duplicateOptions:
                print(DefinitionSet.titleDuplicateOptions + DefinitionSet.listToString(self.duplicateOptions))
    # class ParsingResult

    def Parse(self, metadataEnum, inputList = None):
        self.validateAndNormalize(metadataEnum, inputList)
        self.result = self.ParsingResult(
            options = {},
            unrecognizedOptions = [],
            missingOptions = [],
            duplicateOptions = [],
            fileList = [],
            invalidOptions = [],
            help = self.generateHelp(metadataEnum)
        )
        metadataDictionary = {}
        metadataDictionaryAbbreviated = {}
        for option in metadataEnum.all():
            metadataDictionary[option.value.fullName] = option 
            metadataDictionaryAbbreviated[option.value.abbreviatedName] = option
        if not inputList:
            inputList = sys.argv[1:]
        for word in inputList:
            self.parseOption(word, metadataDictionary, metadataDictionaryAbbreviated)
        self.reclassifyRecognizedOptions(metadataEnum)
        self.result.options = self.reKeyOptions(metadataEnum, self.result.options)
        self.result.options = self.createAccessWrapper(metadataEnum)
    # Parse

    # implementation:

    def createAccessWrapper(self, metadataEnum):
        cls = type(str(), (), {})
        def getItem(self, enumerationMember):
            return self.optionDictionary[enumerationMember]
        cls.__getitem__ = getItem
        def getLength(self):
            return len(self.metadata)
        cls.__len__ = getLength
        instance = cls()
        instance.optionDictionary = dict(self.result.options)
        instance.metadata = metadataEnum
        instance.declaringClass = type(self)
        def toString(self):
            def optionToString(option):
                value = DefinitionSet.formatOptionStateMissing
                if option:
                    if option.optionInput == None:
                        if option.optionState != self.declaringClass.OptionState.Missing:
                            value = DefinitionSet.formatOptionStateDefault
                            allowValue = (option.descriptor.value.valueModality.value & DefinitionSet.optionModalityBitValue) > 0
                            if allowValue:
                                fmt = DefinitionSet.formatOptionStateDefaultValue
                                if isinstance(option.value, str):
                                    fmt = DefinitionSet.formatOptionStateDefaultValueString
                                value = fmt.format(option.value)
                    if option.optionState == self.declaringClass.OptionState.Invalid:
                        value = DefinitionSet.formatOptionStateDefaultInvalid
                    elif option.optionState == self.declaringClass.OptionState.Default:
                        value = DefinitionSet.formatOptionStateDefaultOn
                    elif option.optionState == self.declaringClass.OptionState.Value:
                        value = DefinitionSet.formatOptionValue.format(option.value)
                    elif option.optionState == self.declaringClass.OptionState.Plus:
                        value = DefinitionSet.plus
                    elif option.optionState == self.declaringClass.OptionState.Minus:
                        value = DefinitionSet.minus
                return DefinitionSet.formatOptionPair.format(enumerationMember.name, value)
            # optionToString
            result = []
            for enumerationMember in self.metadata.all():
                option = self.optionDictionary[enumerationMember]
                if isinstance(option, list):
                    for element in option:
                        result.append(optionToString(element))
                else:
                    result.append(optionToString(option))
            return DefinitionSet.optionValueDelimiter.join(result)
        cls.__str__ = toString
        def iterator(self):
            for enumerationMember in self.metadata.all():
                option = self.optionDictionary[enumerationMember]
                if isinstance(option, list):
                    for subOption in option:
                        yield subOption    
                else:
                    yield self.optionDictionary[enumerationMember]
        cls.__iter__ = iterator
        return instance
    # createAccessWrapper

    def reclassifyRecognizedOptions(self, metadataEnum):
        def validateOption(option):
            modality = option.descriptor.value.valueModality.value
            prefix = DefinitionSet.optionPrefix
            if option.abbreviatedForm:
                prefix = DefinitionSet.abbreviatedOptionPrefix
            if option.optionState == self.OptionState.Default:
                if (modality & DefinitionSet.optionModalityBitOption) == 0:
                    allowSign = (modality & DefinitionSet.optionModalityBitSign) > 0
                    allowValue = (modality & DefinitionSet.optionModalityBitValue) > 0
                    if allowSign and allowValue:
                        return DefinitionSet.invalidValueFormatNoPlusMinusValue.format(
                            prefix, option.name, DefinitionSet.minus, DefinitionSet.plus)
                    elif allowSign:
                        return DefinitionSet.invalidValueFormatSign.format(
                            prefix, option.name, DefinitionSet.minus, DefinitionSet.plus)
                    elif allowValue:
                        return DefinitionSet.invalidValueFormatValue.format(
                            prefix, option.name)
            if option.optionState == self.OptionState.Minus or option.optionState == self.OptionState.Plus:
                if (modality & DefinitionSet.optionModalityBitSign) == 0: 
                    return DefinitionSet.invalidValueFormatNoSign.format(
                        prefix, option.name, DefinitionSet.minus, DefinitionSet.plus)
            if option.optionState == self.OptionState.Value:
                if (modality & DefinitionSet.optionModalityBitValue) == 0: 
                    return DefinitionSet.invalidValueFormatNoValue.format(
                        prefix, option.name)
                else:
                    if option.descriptor.value.values and len(option.descriptor.value.values) > 0:
                        if not option.descriptor.value.values(option.value):
                            return DefinitionSet.invalidValueFormat.format(option.value)
            if option.descriptor.value.validator:
                return option.descriptor.value.validator(option)
        # validateOption
        for descriptor in metadataEnum.all():
            found = descriptor.index in self.result.options
            optionList = None
            if found:
                optionList = self.result.options[descriptor.index]
            if descriptor.value.multiplicity and not optionList:
                if descriptor.value.multiplicity.min > 0: # that is, mandatory
                    self.result.missingOptions.append(DefinitionSet.optionPrefix + descriptor.value.fullName)
            if not optionList:
                continue
            removeCount = len(optionList) - descriptor.value.multiplicity.max
            if removeCount > 0:
                while removeCount > 0:
                    removeCount += -1
                    self.result.duplicateOptions.append(optionList.pop().optionInput)
            for option in optionList:
                optionProblem = validateOption(option)
                if optionProblem != None:
                    option.optionState = self.OptionState.Invalid
                    invalidOption = type(str(), (), {})()
                    invalidOption.option = option
                    invalidOption.problem = optionProblem
                    self.result.invalidOptions.append(invalidOption)        
        # loop
    # reclassifyRecognizedOptions

    def reKeyOptions(self, metadataEnum, options):
        result = {}
        for key in options.keys():
            option = metadataEnum[key]
            result[option] = options[key]
        for key in metadataEnum.all():
            if key in result:
                if isinstance(result[key], list) and len(result[key]) == 1:
                    result[key] = result[key][0]
            else:
                optionState = self.OptionState.Missing if key.value.multiplicity.min > 0 else self.OptionState.Unspecified
                result[key] = self.Option(
                    key,
                    None, key.value.fullName, False,
                    optionState,
                    key.value.default)
        return result
    # reKeyOptions

    @classmethod
    def validateAndNormalize(cls, metadata, inputList):
        optionNamePattern = re.compile(DefinitionSet.regexOptionNameValidator)
        if not Enum.IsInstanceOfEnumerationType(metadata):
            raise TypeError(DefinitionSet.exceptionEnumerationType, metadata)
        fullNameSet = set()
        abbreviatedNameSet = set()
        def validateName(setInstance, name):
            if not name:
                return
            if not isinstance(name, str):   
                raise TypeError(DefinitionSet.exceptionOptionNameType, name, type(name))
            if name in setInstance:
                raise ValueError(DefinitionSet.exceptionNonUniqueOptionName, name)
            if name.startswith(DefinitionSet.abbreviatedOptionPrefix) or optionNamePattern.findall(name):
                raise ValueError(DefinitionSet.exceptionInvalidOptionName, name)
            setInstance.add(name)
        # validateName
        for descriptor in metadata.all():
            if not descriptor.value.fullName: # the only "Normalize" part:
                descriptor.value.fullName = descriptor.name
            fullName = descriptor.value.fullName
            abbreviatedName = descriptor.value.abbreviatedName
            validateName(fullNameSet, fullName)
            validateName(abbreviatedNameSet, abbreviatedName)
            multiplicity = descriptor.value.multiplicity
            if not multiplicity == None:
                if not isinstance(multiplicity, cls.Multiplicity):
                    raise TypeError(DefinitionSet.exceptionMultiplicityType, multiplicity, type(multiplicity)) 
            valueModality = descriptor.value.valueModality
            if not valueModality == None:
                if not Enum.IsMemberOfEnumeration(cls.OptionValueModality, valueModality):
                    raise TypeError(DefinitionSet.exceptionValueModalityType, cls.OptionValueModality, valueModality, type(valueModality))
        validValueSet = descriptor.value.values
        if not Enum.IsInstanceOfEnumerationType(validValueSet):
            raise TypeError(DefinitionSet.exceptionEnumerationType, validValueSet)                 
        if not isinstance(inputList, list):
            raise TypeError(DefinitionSet.exceptionInputList, inputList)
        for listItem in inputList:
            if not isinstance(listItem, str):
                raise TypeError(DefinitionSet.exceptionInputListElement, inputList)
    # validateAndNormalize

    @staticmethod
    def generateHelp(metadata):
        def generateOptionValidValues(prefix, descriptor):
            if not (descriptor.value.values and len(descriptor.value.values) > 0):
                 return None
            result = [DefinitionSet.helpValidValuesProlog]
            for value in descriptor.value.values.all():
                strValue = value.value
                if strValue == None:
                    strValue = value.name
                result.append(prefix + DefinitionSet.valueDelimiter + strValue)
            return DefinitionSet.helpValueDelimiter.join(result)
        def generateOptionValidityInfo(prefix, descriptor):
            result = generateOptionValidValues(prefix, descriptor)
            if result != None:
                return result
            result = [DefinitionSet.helpValidValuesProlog]
            bitmap = descriptor.value.valueModality.value
            if (bitmap & DefinitionSet.optionModalityBitOption) > 0:
                result.append(prefix)
            if (bitmap & DefinitionSet.optionModalityBitSign) > 0:
                result.append(prefix + DefinitionSet.minus)
                result.append(prefix + DefinitionSet.plus)
            if (bitmap & DefinitionSet.optionModalityBitValue) > 0:
                result.append(prefix + DefinitionSet.valueDelimiter + DefinitionSet.helpValueNotation)
            return DefinitionSet.helpValueDelimiter.join(result)
        help = []
        count = len(metadata)
        for descriptor in metadata.all():
            count += -1
            nameLines = []
            if descriptor.value.fullName:
                nameLines.append(DefinitionSet.optionPrefix + descriptor.value.fullName)
            if descriptor.value.abbreviatedName:
                nameLines.append(DefinitionSet.abbreviatedOptionPrefix + descriptor.value.abbreviatedName)
            nameLines[len(nameLines) - 1] += DefinitionSet.helpDelimiter
            help += nameLines # not append!
            if descriptor.value.description:
                help.append(descriptor.value.description)
            if descriptor.value.valueModality and descriptor.value.valueModality != CommandLineParserBase.OptionValueModality.Default:
                shortName = descriptor.value.abbreviatedName
                prefix = DefinitionSet.abbreviatedOptionPrefix
                if not shortName:
                    shortName = descriptor.value.fullName
                    prefix = DefinitionSet.optionPrefix
                validityInfo = generateOptionValidityInfo(
                    prefix + shortName, descriptor)
                if validityInfo:
                    help.append(validityInfo)
            if count > 0:
                help.append(str())
        return help
    # generateHelp
    
    def parseOption(self, word, metadataDictionary, metadataDictionaryAbbreviated):
        optionName = None
        optionState = self.OptionState.Default
        value = None
        isAbbreviated = False
        theRest = str()
        if word.startswith(DefinitionSet.optionPrefix):
            theRest = word[len(DefinitionSet.optionPrefix):]
        elif word.startswith(DefinitionSet.abbreviatedOptionPrefix):
            isAbbreviated = True
            theRest = word[len(DefinitionSet.abbreviatedOptionPrefix):]
        else:
            self.result.fileList.append(word)
            return
        if len(theRest) < 1:
            self.result.unrecognizedOptions.append(word)
            return
        terms = theRest.split(DefinitionSet.valueDelimiter, 1)
        if len(terms) == 2:
            optionName = terms[0]
            value = terms[1]
            optionState = self.OptionState.Value
        elif len(terms) == 1:
            optionName = terms[0]
            if optionName.endswith(DefinitionSet.plus):
                optionName = optionName[:-1]
                optionState = self.OptionState.Plus
            elif optionName.endswith(DefinitionSet.minus):
                optionName = optionName[:-1]
                optionState = self.OptionState.Minus
        else:
            self.result.unrecognizedOptions.append(word)
            return
        metadataDictionary = metadataDictionaryAbbreviated if isAbbreviated else metadataDictionary
        if optionName in metadataDictionary:
            descriptor = metadataDictionary[optionName]
            option = self.Option(descriptor, word, optionName, isAbbreviated, optionState, value)
            key = descriptor.index
            if not key in self.result.options:
                self.result.options[key] = []
            self.result.options[key].append(option)
        else:
            self.result.unrecognizedOptions.append(word)
    # parseOption

# class CommandLineParser
