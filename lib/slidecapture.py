import cv2


class SlideCapture:
    def __init__(self, dev_id: int=0):
        """
        カメラのIDを指定する．内臓カメラはだいたい0に設定されているので，webカメラを使いたい場合は1にする．
        :param dev_id: カメラのID
        """
        self.dev_id = dev_id

    def camera_test(self, img_size=(800, 600)):
        print('start camera test.')
        print('press esc key for quit.')
        print('press s key for save image')

        cap = cv2.VideoCapture(self.dev_id)

        while True:
            # retは画像を取得成功フラグ
            ret, frame = cap.read()

            # フレームをリサイズ
            frame = cv2.resize(frame, img_size)

            # フレームを表示する
            cv2.imshow('camera capture', frame)

            k = cv2.waitKey(1)                  # 1msec待つ
            if k == 27:                         # escキーで終了
                break
            elif k == ord('s'):                 # 保存
                cv2.imwrite('test_frame.jpg', frame)
                print('image \'test_frame/jpg\' saved.')

        # キャプチャを解放する
        cap.release()
        cv2.destroyAllWindows()

    def monitor_slides(self):

        cap = cv2.VideoCapture(self.dev_id)
        if not cap.isOpened():
            print('[error] cannot open camera')
            return False

        while True:
            # retは画像を取得成功フラグ
            ret, frame = cap.read()
            if not ret:
                print('[error] cannot read frame')
                continue

            # グレースケール
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # 2値化 TODO: パラメータ
            _, bin_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)

            # TODO: 人などのノイズ処理

            # スライドの輪郭検出
            # リファレンス：http://opencv.jp/opencv-2.1/cpp/structural_analysis_and_shape_descriptors.html
            image, contours, hierarchy = cv2.findContours(bin_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            for con in contours:

                # 一定の面積でフィルタ
                area = cv2.contourArea(con)
                if area > 5000:             # TODO: パラメータ
                    approx = cv2.approxPolyDP(con, 0.02 * cv2.arcLength(con, True), True)
                    if len(approx) < 4:
                        continue
                    cv2.drawContours(frame, approx, -1, (255, 0, 0), 3)

            # 表示
            out_frame = cv2.resize(frame, (800, 600))
            cv2.imshow('camera capture', out_frame)

            k = cv2.waitKey(1)                  # 1msec待つ
            if k != -1:                         # 何か押したら終了
                break

        # キャプチャを解放する
        cap.release()
        cv2.destroyAllWindows()