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
        if not self.text:
            return []

        ret = self.goolab.entity(sentence=self.text, class_filter=u"PSN|ORG|ART|DAT")
        for idx in range(len(ret['ne_list'])):
            key = (ret['ne_list'][idx][0], ret['ne_list'][idx][1])
            keywords.append(key)
        return keywords


    def __create_questions(self):
        """
        抽出したキーワードに文章を付加して問題文を生成する
        生成した問題文を”リスト”で返すことに注意

        :param keyword:　抽出したキーワード
        :return questions:　生成した問題文
        """
        # カテゴリ別で問題を作成
        questions = []
        for key in self.keywords:
            if key[1] == 'PSN':
                questions.append(key[0] + 'は何をしたか？')
                questions.append(key[0] + 'について説明せよ。')
            elif key[1] == 'ART':
                questions.append(key[0] + 'とは何か？')
                questions.append(key[0] + 'は誰が考案したか？')
            elif key[1] == 'DAT':
                questions.append(key[0] + 'には何が起こったか？')
            elif key[1] == 'ORG':
                questions.append(key[0] + 'はいつ作られたか？')
                questions.append(key[0] + 'について説明せよ。')

        return questions

    def get_questions(self, max_questions: int=3):
        """
        問題文リストからランダムに問題を返す
        :param max_questions: 問題数
        :return: ランダムに選択された問題文リスト
        """
        n_ques = len(self.questions)
        if max_questions > n_ques:
            max_questions = n_ques
        return random.sample(self.questions, max_questions)
