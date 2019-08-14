import re
from hearthstone_card_generator import CardGenerator, CardInformationDatabase
from card_formatter import CardFormatter

class CommentParser:
    def __init__(self):
        self.__cardFomatter = CardFormatter()
        self.__cardGenerator = CardGenerator(CardInformationDatabase())
    def parse_comment(self, comment):
        doubleBracketedTexts = self.__get_double_bracketed_texts(comment)
        tripleBracketedTexts = self.__get_triple_bracketed_texts(comment)
        bracketedTexts = self.__process_bracketed_texts(doubleBracketedTexts, tripleBracketedTexts)
        newMessage = ''
        for bracketedText in bracketedTexts:
            if self.__is_double_bracketed(bracketedText.group(0)):
                cardName = bracketedText.group(1)
                card = self.__cardGenerator.get_card_information(name=cardName)
                if card:
                    newMessage += self.__cardFomatter.format_card(self.__cardGenerator.get_card_information(name=cardName))
            else:
                newMessage += self.__cardFomatter.format_card(self.__cardGenerator.generate_random_card(name=bracketedText.group(1)))
        return f'```{newMessage}```' if newMessage != '' else ''

    def __get_double_bracketed_texts(self, messageContent):
        return list(filter(lambda match: not match.group(0).startswith('[[['), re.finditer(r'\[\[(.*?)\]\]', messageContent, re.M | re.I)))

    def __get_triple_bracketed_texts(self, messageContent):
        return list(re.finditer(r'\[\[\[(.*?)\]\]\]', messageContent, re.M | re.I))

    def __is_double_bracketed(self, bracketedText):
        return bracketedText.startswith('[[') and not bracketedText.startswith('[[[')

    def __process_bracketed_texts(self, doubleBracketedTexts, tripleBracketedTexts):
      bracketedTexts = (doubleBracketedTexts + tripleBracketedTexts)[:7]
      bracketedTexts.sort(key=lambda bt: bt.span()[0])
      return bracketedTexts