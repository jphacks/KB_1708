class QuestionGeneratorOfKeywords(object):
    '''
    抽出したキーワードのリストを貰って、問題文を返す
    '''

    def __init__(self, keyword: str):
        self.keyword = keyword

    def create_questions_with(self) -> [str]:
        '''
        抽出したキーワードに文章を付加して問題文を生成する
        生成した問題文を”リスト”で返すことに注意

        :param keyword:　抽出したキーワード
        :return questions:　生成した問題文
        '''
        # カテゴリ別で問題を作成
        questions = []
        for key in self.keyword:
            if key[1] == 'PSN':
                questions.append(self.what_did(key[0]))
                questions.append(self.explain(key[0]))
            elif key[1] == 'ART':
                questions.append(self.what_is(key[0]))
                questions.append(self.who_did_create(key[0]))
            elif key[1] == 'DAT':
                questions.append(self.when_happen(key[0]))
            elif key[1] == 'ORG':
                questions.append(self.when_made(key[0]))
                questions.append(self.explain(key[0]))
        # questions.append(self.what_is(self.keyword))
        # questions.append(self.explain(self.keyword))
        # questions.append(self.calculate(self.keyword))
        # questions.append(self.who_did_create(self.keyword))
        # questions.append(self.what_is_synonym_of(self.keyword))
        return questions

    # def convert_keywords_to_qustions_list(self, keywords: [str]):
    #     question_generator = QuestionGeneratorOfKeywords(keywords)
    #     questions_list = []
    #     for keyword in question_generator.keywords:
    #         questions = question_generator.create_questions_with(keyword)
    #         questions_list.append(questions)
    #     # print(questions_list)
    #     return questions_list

    def what_is(self, keyword: str) -> str:
        question = keyword + "とは何か？"
        return question

    def explain(self, keyword: str) -> str:
        question = keyword + "について説明せよ。"
        return question

    def calculate(self, keyword: str) -> str:
        question = keyword + "を計算せよ。"
        return question

    def who_did_create(self, keyword: str) -> str:
        question = keyword + "は誰が考案したか？"
        return question

    def what_is_synonym_of(self, keyword: str) -> str:
        question = keyword + "の類義語は何か。"
        return question

    def what_did(self,keyword: str) -> str:
        question = keyword + 'は何をしたか？'
        return question

    def when_happen(self, keyword: str) -> str:
        question = keyword + 'には何が起こったか？'
        return question

    def when_made(self, keyword: str) -> str:
        question = keyword + 'はいつ作られたか？'
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