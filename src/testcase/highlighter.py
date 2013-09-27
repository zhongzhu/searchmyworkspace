from PySide.QtCore import *
from PySide.QtGui import *

class TetSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(TetSyntaxHighlighter, self).__init__(parent)

        self.highlightingRules = []
        self.tetSyntaxHighlight = {"INSTRUCTION WORD": { 'color':"#008080", 'bold':"true", 'italic':"false"},
                                "TYPE WORD": { 'color':"#AA007F", 'bold':"true", 'italic':"false"},
                                "STRUCT": { 'color':"#FF1493", 'bold':"true", 'italic':"false"},
                                "GI": { 'color':"#000080", 'bold':"true", 'italic':"false"},
                                "STRING": { 'color':"#008000", 'bold':"true", 'italic':"false"},
                                "VARIABLE": { 'color':"#FF8000", 'bold':"true", 'italic':"false"},
                                "ARGUMENT": { 'color':"#CE0000", 'bold':"true", 'italic':"false"},
                                "COMMENT": { 'color':"#AA5F0A", 'bold':"false", 'italic':"true"},
                                "COMMENT DOC": { 'color':"#808080", 'bold':"false", 'italic':"true"},
                                "CURRENT LINE": { 'color':"#E8F2FE", 'bold':"false", 'italic':"false"},
                                "LINENUMBERAREA": { 'color':"#E4E4E4", 'bold':"false", 'italic':"false"},
                                "BACKGROUND": { 'color':"#FFFFFF", 'bold':"false", 'italic':"false"}}

        # setActionRule();
        actionCharFormat = QTextCharFormat()
        keywordPatterns = ['if', 'else']
        self._updateCharFormat('INSTRUCTION WORD', actionCharFormat)
        self.highlightingRules = [(QRegExp("\\b" + keyword + "\\b"), actionCharFormat) for keyword in keywordPatterns]

        # setStructRule();
        structCharFormat = QTextCharFormat()
        keywordPatterns = ["function" , "description" , "arguments" , "variables" , "responseMapping", "steps"]
        self._updateCharFormat('STRUCT', structCharFormat)
        self.highlightingRules.extend([(QRegExp(keyword), structCharFormat) for keyword in keywordPatterns])

        # setSimpleTypeRule();
        simpleTypeCharFormat = QTextCharFormat()
        keywordPatterns = ['string', 'int', 'double', 'TArray', 'TMap', 'TDateTime', 'TFile', 'TRegExp']
        self._updateCharFormat('TYPE WORD', simpleTypeCharFormat)
        self.highlightingRules.extend([(QRegExp("\\b" + keyword + "\\b"), simpleTypeCharFormat) for keyword in keywordPatterns])

        # setGiRule();
        generalInfoCharFormat = QTextCharFormat()
        keywordPatterns = ['TC_ID', 'QC_ID', 'Title', 'Author', 'Created', 'Purpose', 'Usage', 'Tag']
        self._updateCharFormat('GI', generalInfoCharFormat)
        self.highlightingRules.extend([(QRegExp("\\b" + keyword + "\\b"), generalInfoCharFormat) for keyword in keywordPatterns])

        # setVariableRuleForTet();
        variableCharFormat = QTextCharFormat()
        self._updateCharFormat('VARIABLE', variableCharFormat)
        self.highlightingRules.append((QRegExp("\\$\\w+"), variableCharFormat))

        # setArgumentRuleForTet();
        argumentNameCharFormat = QTextCharFormat()
        self._updateCharFormat('ARGUMENT', argumentNameCharFormat)
        self.highlightingRules.append((QRegExp("-[^0-9]\\S*"), argumentNameCharFormat))

        # setQuotedTextRuleForTet();
        quotedTextCharFormat = QTextCharFormat()
        self._updateCharFormat('STRING', quotedTextCharFormat)
        self.highlightingRules.append((QRegExp("\"[^\"]+\""), quotedTextCharFormat))

        # setCommentRule();
        commentCharFormat = QTextCharFormat()
        self._updateCharFormat('COMMENT', commentCharFormat)
        self.highlightingRules.append((QRegExp("comment\\s.*"), commentCharFormat))
        self.highlightingRules.append((QRegExp("comment$"), commentCharFormat))

        # setCommentDocRule();
        commentDocCharFormat = QTextCharFormat()
        self._updateCharFormat('COMMENT DOC', commentDocCharFormat)
        self.highlightingRules.append((QRegExp("\\/\\/.*"), commentDocCharFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, format)
                index = pattern.indexIn(text, index + length)

    def _updateCharFormat(self, type, charFormat):
        charFormat.setForeground(QColor(self.tetSyntaxHighlight[type]['color']))
        if self.tetSyntaxHighlight[type]['bold'] == "true":
            charFormat.setFontWeight(QFont.Bold)
        if self.tetSyntaxHighlight[type]['italic'] == "true":
            charFormat.setFontItalic(True)
