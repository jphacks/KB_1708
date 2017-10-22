# coding: utf-8


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
        questions.append(self.what_is(keyword))
        questions.append(self.explain(keyword))
        questions.append(self.calculate(keyword))
        questions.append(self.who_did_create(keyword))
        questions.append(self.what_is_synonym_of(keyword))
        return questions

    def convert_keywords_to_qustions_list(self, keywords: [str]):
        question_generator = QuestionGeneratorOfKeywords(keywords)
        questions_list = []
        for keyword in question_generator.keywords:
            questions = question_generator.create_questions_with(keyword)
            questions_list.append(questions)
        # print(questions_list)
        return questions_list


    def what_is(self, keyword: str) -> str:
        question = keyword + "の定義を答えよ"
        return question

    def explain(self, keyword: str) -> str:
        question = keyword + "を説明せよ"
        return question

    def calculate(self, keyword: str) -> str:
        question = keyword + "を計算せよ"
        return question

    def who_did_create(self, keyword: str) -> str:
        question = keyword + "は誰が考案したか？"
        return question

    def what_is_synonym_of(self, keyword: str) -> str:
        question = keyword + "の類義語は何か"
        return question





            # # キーワードとして ["abc", "def"]　を使っている時
# question_generator = QuestionGeneratorOfKeywords(["abc", "def"])
# questions_list = []
# for keyword in question_generator.keywords:
#     questions = question_generator.create_questions_with(keyword)
#     questions_list.append(questions)
# print(questionsList)
# # [['abcの定義を答えよ', 'abcを説明せよ', 'abcを計算せよ', 'abcは誰が考案したか？', 'abcの類義語は何か'],
# # ['defの定義を答えよ', 'defを説明せよ', 'defを計算せよ', 'defは誰が考案したか？', 'defの類義語は何か']]