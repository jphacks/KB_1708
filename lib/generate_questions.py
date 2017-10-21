#coding: utf-8


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



def createQquestionsBy(keyword: str) -> [str]:
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
