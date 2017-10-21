import cv2
import time


class SlideCapture:

    def __init__(self, dev_id: int=0):
        """
        カメラのIDを指定する．内臓カメラはだいたい0に設定されているので，webカメラを使いたい場合は1にする．
        今回使うカメラの解像度は1920*1080なので，640*360にリサイズする．
        :param dev_id: カメラのID
        """
        self.dev_id = dev_id
        self.cap = cv2.VideoCapture(self.dev_id)

    def close(self):
        """
        カメラリソースを解放する．なるべく最後に呼んで．
        :return:
        """
        self.cap.release()

    def get_slide_position(self):
        """
        画像からスライドの位置を特定してその座標，大きさを返す．
        :return:
        """

        ret, frame = self.cap.read()
        if not ret:
            print('[error] cannot read frame')
            return False

        # グレースケール
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # 2値化
        _, bin_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)
        # 輪郭検出
        image, contours, hierarchy = cv2.findContours(bin_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # 輪郭フィルタ
        approxs = []
        for con in contours:
            # 一定の面積でフィルタ
            area = cv2.contourArea(con)
            if area > 5000:  # TODO: パラメータ
                approx = cv2.approxPolyDP(con, 0.02 * cv2.arcLength(con, True), True)
                if len(approx) < 4:
                    continue
                approxs.append(approx)
                cv2.drawContours(frame, approx, -1, (255, 0, 0), 3)     # for debug

        # TODO: approxsの中からスライドと思われるものを抽出

        # TODO: スライドの座標，大きさをreturn
        return True

    def monitor_slides(self):
        """
        スライドを監視し，それぞれ1枚ずつjpg画像として保存する．
        :return:
        """

        if not self.cap.isOpened():
            print('[error] cannot open camera')
            return False

        # スライドのだいたいの位置を特定
        slide_position = self.get_slide_position()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print('[error] cannot read frame')
                continue

            # TODO: スライド部分をトリミング

            # TODO: 人などのノイズを検知

            # TODO: スライドの差分を検知, 保存

            # 表示
            out_frame = cv2.resize(frame, (640, 360))
            cv2.imshow('camera capture', out_frame)

            k = cv2.waitKey(1)                  # 1msec待つ
            if k != -1:                         # 何か押したら終了
                break

        # キャプチャを解放する
        cv2.destroyAllWindows()

    def camera_test(self, img_size=(640, 360)):
        """
        ほぼデバッグ用のカメラテストメソッド
        :param img_size:
        :return:
        """
        print('start camera test.')
        print('press esc key for quit.')
        print('press s key for save image')

        while True:
            # retは画像を取得成功フラグ
            ret, frame = self.cap.read()

            # 表示
            frame = cv2.resize(frame, img_size)
            cv2.imshow('camera capture', frame)

            k = cv2.waitKey(1)                  # 1msec待つ
            if k == 27:                         # escキーで終了
                break
            elif k == ord('s'):                 # 保存
                cv2.imwrite('test_frame.jpg', frame)
                print('image \'test_frame/jpg\' saved.')

        # キャプチャを解放する
        cv2.destroyAllWindows()

    def record_video(self, filename: str):
        fps = 30
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(filename, fourcc, fps, size)

        is_record = False
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                show_frame = cv2.resize(frame, (640, 360))
                cv2.imshow('frame', show_frame)
                if is_record:
                    video.write(frame)

                k = cv2.waitKey(1)
                if k == ord('s'):
                    print('start record')
                    is_record = True
                elif k == ord('q'):
                    print('finish record')
                    is_record = False
                    break

            else:
                print('[error] cannot read camera')
                break

        video.release()
        cv2.destroyAllWindows()

    def play_video(self, filename: str):
        video = cv2.VideoCapture(filename, 0)
        time.sleep(2)

        while video.isOpened():

            ret, frame = video.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                cv2.imshow('video', frame)
            else:
                break

            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()