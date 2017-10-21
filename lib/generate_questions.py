#coding: utf-8

def whatIs(keyword: str) -> str:
    question = keyword + "は何ですか？"
    return question

def createQquestionsBy(keyword: str) -> [str]:
    questions = []
    questions.append(whatIs(keyword))
    questions.append()

    return questions
