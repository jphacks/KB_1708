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
            # sizeは例えば(800, 600)
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
