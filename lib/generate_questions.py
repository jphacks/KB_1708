# coding: utf-8

def whatIs(keyword: str) -> str:
    question = keyword + "の定義を答えよ"
    return question


def explain(keyword: str) -> str:
    question = keyword + "を説明せよ"
    return question


def calculate(keyword: str) -> str:
    question = keyword + "を計算せよ"
    return question


def whoDidCreate(keyword: str) -> str:
    question = keyword + "は誰が考案したか？"
    return question


def whatIsSynonymOf(keyword: str) -> str:
    question = keyword + "の類義語は何か"
    return question


class QuestionGeneratorOfKeywords():
    '''
    抽出したキーワードのリストを貰って、問題文を返す
    '''

    def __init__(self, keywords: [str]):
        self.keywords = keywords

    def createQuestionsWith(self, keyword: str) -> [str]:
        '''
        抽出したキーワードに文章を付加して問題文を生成する
        生成した問題文を”リスト”で返すことに注意

        :param keyword:　抽出したキーワード
        :return questions:　生成した問題文
        '''
        questions = []
        questions.append(whatIs(keyword))
        questions.append(explain(keyword))
        questions.append(calculate(keyword))
        questions.append(whoDidCreate(keyword))
        questions.append(whatIsSynonymOf(keyword))

        return questions

# # キーワードとして ["abc", "def"]　を使っている時
# questionGenerator = QuestionGeneratorOfKeywords(["abc", "def"])
# questionsList = []
# for keyword in questionGenerator.keywords:
#     questions = questionGenerator.createQuestionsWith(keyword)
#     questionsList.append(questions)
# print(questionsList)
# # [['abcの定義を答えよ', 'abcを説明せよ', 'abcを計算せよ', 'abcは誰が考案したか？', 'abcの類義語は何か'],
# # ['defの定義を答えよ', 'defを説明せよ', 'defを計算せよ', 'defは誰が考案したか？', 'defの類義語は何か']]