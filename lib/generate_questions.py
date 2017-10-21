# coding: utf-8

def what_is(keyword: str) -> str:
    question = keyword + "の定義を答えよ"
    return question


def explain(keyword: str) -> str:
    question = keyword + "を説明せよ"
    return question


def calculate(keyword: str) -> str:
    question = keyword + "を計算せよ"
    return question


def who_did_create(keyword: str) -> str:
    question = keyword + "は誰が考案したか？"
    return question


def what_is_synonym_of(keyword: str) -> str:
    question = keyword + "の類義語は何か"
    return question


class QuestionGeneratorOfKeywords():
    '''
    抽出したキーワードのリストを貰って、問題文を返す
    '''

    def __init__(self, keywords: [str]):
        self.keywords = keywords

    def create_questions_with(self, keyword: str) -> [str]:
        '''
        抽出したキーワードに文章を付加して問題文を生成する
        生成した問題文を”リスト”で返すことに注意

        :param keyword:　抽出したキーワード
        :return questions:　生成した問題文
        '''
        questions = []
        questions.append(what_is(keyword))
        questions.append(explain(keyword))
        questions.append(calculate(keyword))
        questions.append(who_did_create(keyword))
        questions.append(what_is_synonym_of(keyword))

        return questions

# # キーワードとして ["abc", "def"]　を使っている時
# question_generator = QuestionGeneratorOfKeywords(["abc", "def"])
# questions_list = []
# for keyword in question_generator.keywords:
#     questions = question_generator.create_questions_with(keyword)
#     questions_list.append(questions)
# print(questionsList)
# # [['abcの定義を答えよ', 'abcを説明せよ', 'abcを計算せよ', 'abcは誰が考案したか？', 'abcの類義語は何か'],
# # ['defの定義を答えよ', 'defを説明せよ', 'defを計算せよ', 'defは誰が考案したか？', 'defの類義語は何か']]