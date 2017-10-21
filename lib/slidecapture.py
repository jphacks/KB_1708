import cv2
import time


class SlideCaptureError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SlideCapture:

    def __init__(self, dev_id: int=cv2.CAP_ANY):
        """
        カメラのIDを指定する．内臓カメラはだいたい0に設定されているので，webカメラを使いたい場合は1にする．
        今回使うカメラの解像度は1920*1080なので，640*360にリサイズする．
        :param dev_id: カメラのID
        """
        self.dev_id = dev_id
        self.cap = cv2.VideoCapture(self.dev_id)
        self.cap_open_check()

    def cap_open_check(self):
        if not self.cap.isOpened():
            raise SlideCaptureError('camera is not opened!')

    def open(self, dev_id: int=cv2.CAP_ANY):
        """
        カメラに再接続
        :param dev_id:
        :return:
        """
        self.cap.release()
        self.dev_id = dev_id
        self.cap = cv2.VideoCapture(self.dev_id)

    def close(self):
        """
        カメラリソースを解放する．なるべく最後に呼んで．
        :return:
        """
        self.cap.release()

    def calibration(self, cache_path:str ='./media/cache'):
        """
        画像を一枚取得してキャッシュディレクトリに'calibration.jpg'として保存する．
        :param cache_path: キャッシュディレクトリのパス
        :return: TF
        """

        self.cap_open_check()
        ret, frame = self.cap.read()
        if not ret:
            raise SlideCaptureError('cannot read frame')

        cv2.imwrite(cache_path + '/calibration.jpg', frame)

        return True

    def get_slide_position(self):
        """
        画像からスライドの位置を特定してその座標，大きさを返す．
        :return:
        """

        self.cap_open_check()
        ret, frame = self.cap.read()
        if not ret:
            raise SlideCaptureError('cannot read frame')

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

        self.cap_open_check()

        # スライドのだいたいの位置を特定
        slide_position = self.get_slide_position()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

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

        self.cap_open_check()

        print('start camera test.')
        print('press esc key for quit.')
        print('press s key for save image')

        while True:
            # retは画像を取得成功フラグ
            ret, frame = self.cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

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
        self.cap_open_check()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

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

        video.release()
        cv2.destroyAllWindows()

    def play_video(self, filename: str):
        video = cv2.VideoCapture(filename, 0)
        time.sleep(2)

        self.cap_open_check()
        while True:

            ret, frame = video.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

            frame = cv2.resize(frame, (640, 360))
            cv2.imshow('video', frame)

            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()