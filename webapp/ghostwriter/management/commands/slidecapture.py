import cv2
import time
import numpy as np


class SlideCaptureError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SlideCapture:

    def __init__(self, dev_id: int=cv2.CAP_ANY, video_filename:str =None,
                 threshold_area: int =5000, threshold_bin: int =120, threshold_diff: int =400):
        """
        カメラのIDを指定する．内臓カメラはだいたい0に設定されているので，webカメラを使いたい場合は1にする．
        今回使うカメラの解像度は1920*1080なので，640*360にリサイズする．
        :param dev_id: カメラのID
        :param video_filename: ログのvideoでテストするときに使う
        """

        # video capture init
        if video_filename:
            self.video_cap = cv2.VideoCapture(video_filename, 0)
        else:
            self.video_cap = None

        # camera capture init
        self.dev_id = dev_id
        self.cap = cv2.VideoCapture(self.dev_id)
        self.cap_open_check()

        # threshold params
        self.th_area = threshold_area
        self.th_bin = threshold_bin
        self.th_diff = threshold_diff

        # for pinto
        time.sleep(10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return True

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
        if self.video_cap:
            self.video_cap.release()
        self.cap.release()
        print('capture closed')

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

        # マーカー
        height = frame.shape[0]
        width = frame.shape[1]
        cv2.rectangle(frame,    # 枠
                      (int(width * 1/8), int(height * 1/8)),(int(width * 7/8), int(height * 7/8)),
                      (0, 0, 255), 10)
        cv2.line(frame,         # 縦線
                 (int(width / 2), int(height * 7/16)),(int(width / 2), int(height * 9/16)),
                 (0, 0, 255), 10)
        cv2.line(frame,         # 横線
                 (int(width * 9/20), int(height / 2)), (int(width * 11/20), int(height / 2)),
                 (0, 0, 255), 10)

        cv2.imwrite(cache_path + '/calibration.jpg', frame)

        return True

    def get_slide_position(self, filename:str =None):
        """
        画像からスライドの位置を特定してその座標，大きさを返す．
        :param filename: ログの画像からデバッグするときに使う
        :return:
        """

        if filename:        # for debug
            frame = cv2.imread(filename)

        elif self.video_cap:        # for debug
            ret, frame = self.video_cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

        else:
            self.cap_open_check()
            ret, frame = self.cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

        # グレースケール
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # 2値化
        _, bin_frame = cv2.threshold(gray_frame, self.th_bin, 255, cv2.THRESH_BINARY)
        # 輪郭検出
        image, contours, hierarchy = cv2.findContours(bin_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # 輪郭フィルタ
        approxs = []
        for con in contours:
            # 一定の面積でフィルタ
            area = cv2.contourArea(con)
            if area > self.th_area:
                approx = cv2.approxPolyDP(con, 0.02 * cv2.arcLength(con, True), True)
                if len(approx) < 4:
                    continue
                approxs.append(approx)
                cv2.drawContours(frame, approx, -1, (255, 0, 0), 15)     # for debug

        # 一番スライドっぽいのを抽出(より中心に近いものを？)
        # 中心は960, 540のはず
        id_ans = 0
        center = np.array([960, 540])
        for i, approx in enumerate(approxs):
            if i == 0:
                continue
            m_cndd = np.mean(approx, axis=0)
            u_cndd = center - m_cndd

            m_ans = np.mean(approxs[id_ans], axis=0)
            u_ans = center - m_ans

            if np.linalg.norm(m_cndd) < np.linalg.norm(u_ans):
                id_ans = i

        # for debug
        # out_frame = cv2.resize(frame, (640, 360))
        # cv2.imshow('camera capture', out_frame)
        # print(len(approxs))
        # for approx in approxs:
        #     print(type(approx), approx)
        # while True:
        #     k = cv2.waitKey(1)
        #     if k == ord('q'):
        #         break
        # cv2.destroyAllWindows()
        # print(approxs[id_ans])

        return approxs[id_ans]

    def monitor_slides(self, save_dir: str):
        """
        スライドを監視し，それぞれ1枚ずつjpg画像として保存する．
        :return:
        """
        print("task executed")

        # self.cap_open_check()
        print("open checked")
        # cv2.namedWindow("camera capture", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)     # for debug

        # スライドのだいたいの位置を特定
        slide_position = self.get_slide_position()
        print("get_position")
        trim_from_x = np.min(slide_position, axis=0)[0][0]
        trim_from_y = np.min(slide_position, axis=0)[0][1]
        trim_to_x = np.max(slide_position, axis=0)[0][0]
        trim_to_y = np.max(slide_position, axis=0)[0][1]

        # ゴミ実装
        if self.video_cap:  # for debug (from log video file)
            ret, frame = self.video_cap.read()
        else:
            ret, frame = self.cap.read()

        if not ret:
            raise SlideCaptureError('cannot read frame')

        p_frame = frame
        num_save = 0

        while True:

            if self.video_cap:          # for debug (from log video file)
                ret, frame = self.video_cap.read()
            else:
                ret, frame = self.cap.read()

            if not ret:
                break
                # raise SlideCaptureError('cannot read frame')

            # スライド部分をトリミング
            trim_frame = frame[trim_from_y:trim_to_y, trim_from_x:trim_to_x]

            # グレースケール
            gray_trim_frame = cv2.cvtColor(trim_frame, cv2.COLOR_RGB2GRAY)
            # 2値化
            _, bin_trim_frame = cv2.threshold(gray_trim_frame, self.th_bin, 255, cv2.THRESH_BINARY)

            # TODO: 人などのノイズを検知

            # スライドの差分を検知, 保存
            diff = p_frame.astype(np.int) - frame.astype(np.int)
            # diff_weight = np.mean(np.abs(diff))         # 平均絶対誤差
            diff_weight = np.mean(np.square(diff))    # 平均二乗誤差
            if diff_weight > self.th_diff:
                cv2.imwrite(save_dir+'/'+str(num_save)+'.jpg', frame)
                num_save += 1

            # print(diff_weight)
            p_frame = frame

            # 表示
            # cv2.drawContours(frame, slide_position, -1, (255, 0, 0), 30)    # for debug
            out_frame = cv2.resize(frame, (640, 360))
            cv2.imshow('camera capture', bin_trim_frame)

            # k = cv2.waitKey(1)                  # 1msec待つ
            # if k != -1:                         # 何か押したら終了
            #     break

        cv2.destroyAllWindows()

    def camera_test(self, img_size=(640, 360)):
        """
        ほぼデバッグ用のカメラテストメソッド
        :param img_size:
        :return:
        """

        self.cap_open_check()

        print('start camera test.')
        print('\'esc\' : quit')
        print('\'s\' : save image')

        num_jpg = 0
        while True:

            ret, frame = self.cap.read()
            if not ret:
                raise SlideCaptureError('cannot read frame')

            # 表示
            show_frame = cv2.resize(frame, img_size)
            cv2.imshow('camera capture', show_frame)

            k = cv2.waitKey(1)                  # 1msec待つ
            if k == 27:                         # escキーで終了
                break
            elif k == ord('s'):                 # 保存
                cv2.imwrite('log_frame'+str(num_jpg)+'.jpg', frame)
                num_jpg += 1
                print('image \'test_frame.jpg\' saved.')

        cv2.destroyAllWindows()

    def record_video(self, filename: str):
        fps = 30
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(filename, fourcc, fps, size)

        print('\'s\' : start recording.')
        print('\'q\' : stop recoding and save video')

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
            if k == ord('q'):           # quit
                break

        video.release()
        cv2.destroyAllWindows()