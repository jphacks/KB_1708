import cv2


class SlideCapture:
    def __init__(self, dev_id=0):
        """
        カメラのIDを指定する．内臓カメラはだいたい0に設定されているので，webカメラを使いたい場合は1にする．
        :param dev_id: カメラのID
        """
        self.dev_id = dev_id

    def camera_test(self, size=(800, 600)):
        print('start camera test.')
        print('press esc key for quit.')

        cap = cv2.VideoCapture(self.dev_id)

        while True:
            # retは画像を取得成功フラグ
            ret, frame = cap.read()

            # フレームをリサイズ
            # sizeは例えば(800, 600)
            if size is not None and len(size) == 2:
                frame = cv2.resize(frame, size)

            # フレームを表示する
            cv2.imshow('camera capture', frame)

            k = cv2.waitKey(1)  # 1msec待つ
            if k == 27:  # escキーで終了
                break

        # キャプチャを解放する
        cap.release()
        cv2.destroyAllWindows()
