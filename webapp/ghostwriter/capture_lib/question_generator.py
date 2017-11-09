from goolabs import GoolabsAPI
import random


class QuestionGenerator(object):

    def __init__(self, text: str, goolab_api_key: str):
        """
        GoolabAPIを使用して文字列から問題作成をするクラス
        :param text: 問題作成用文字列
        :param goolab_api_key: goolabのAPI Key
        """
        self.text = text
        self.goolab = GoolabsAPI(goolab_api_key)
        self.keywords = self.__get_keywords()
        self.questions = self.__create_questions()

    def __get_keywords(self):
        """
        textパラメータからGoolabAPIを使用してキーワード抽出
        :return: キーワードリスト
        """
        keywords = []
        ret = self.goolab.entity(sentence=self.text, class_filter=u"PSN|ORG|ART|DAT")
        for idx in range(len(ret['ne_list'])):
            key = (ret['ne_list'][idx][0], ret['ne_list'][idx][1])
            keywords.append(key)
        return keywords


    def __create_questions(self):
        '''
        抽出したキーワードに文章を付加して問題文を生成する
        生成した問題文を”リスト”で返すことに注意

        :param keyword:　抽出したキーワード
        :return questions:　生成した問題文
        '''
        # カテゴリ別で問題を作成
        questions = []
        for key in self.keywords:
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

        return questions

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

    def get_questions(self, num_questions: int=3):
        """
        問題文リストからランダムに問題を返す
        :param num_questions: 問題数
        :return: ランダムに選択された問題文リスト
        """
        return random.sample(self.questions, num_questions)
