Pythonic Metaprogramming, Enumerations and Other Goodies[](title)

[*Sergey A Kryukov*](https://www.SAKryukov.org)

## Contents[](notoc)

[](toc)

## Introduction

This article is supposed to present a line of études on the very essence of Python _metaprogramming_, the way I consider most fruitful and interesting.

We shall consider the cases where some classes are created dynamically. In essence, this is the same as creation of objects.
SA???

## Metaprogramming Basics

Following my own understanding of minimalism, I'll try to show the weird anatomy of what I want to make our scope.

### Preface

### Face

### Bottom... Line

## NamedDictionary

## Enumeration

## Command Line Purchaser

### BNF Syntax

```
<command-line-element> ::= <option> | <file> 
<option> ::= <option-identifier> | <on-option> | <off-option> | <value-option>,
<file> ::= <value>
<option-identifier> ::= --<optionName>|-<shortOptionName>
<on-option> ::= <option-identifier>+
<off-option> ::= <option-identifier>-
<value-option> ::= <option-identifier>:<value>
<optionName> ::= <identifier>
<shortOptionName> ::= <identifier>
<identifier> ::= <non-space-character> | <non-space-character><identifier>
<value> ::= <character>|<value>

```

The input to the parser is the list of `<command-line-element>` elements. For command line provided to some script, we need additional declarations. The only problem here is about strings containing space characters. In the list, there are not problems, but a //SA???

```
<command-line> ::= <generalized-command-line-element> | <command-line> <generalized-command-line-element>    
<generalized-command-line-element> ::= <command-line-element> | <quoted-command-line-element>
<quoted-command-line-element> ::= "<command-line-element>"
```

## Time for Metaclasses

### No Pseudo-Hidden Objects

### No Name Clash

SA??? The _iterator_ `all()` implemented via a _generator_... In memory of Ada reserved word `all`.

#### Hiding in Function

### No Hiding

### Inaccessible Attributes

```
def makeInaccessibleAttributeName(cls, name):
    return cls.DefinitionSet.inaccessibleNamePrefix + name 
```

Python developer are strange people. They defend their language, in the case of SA???

In Python, as in some other scripting languages, such as JavaScript, access to objects can be limited by putting some code inside a function.

### "A new-style class can't have only classic bases"

```
bases.append(object)
```