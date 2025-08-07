from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import cv2
import easyocr

class GetColor:
    def extract_colors(self, image_path):
        # Mở ảnh
        image = Image.open(image_path).convert('RGB')
        image_np = np.array(image)

        # Tăng tương phản
        image_np = cv2.convertScaleAbs(image_np, alpha=1.3, beta=0)

        # Dùng EasyOCR tìm vùng text
        reader = easyocr.Reader(['en'])  # Thêm 'vi' nếu cần tiếng Việt
        results = reader.readtext(image_path, detail=1)

        # In text lấy được
        print("Text EasyOCR nhận diện / Text detected by EasyOCR:")
        for (bbox, text, _) in results:
            print(f"- {text}")
        if not results:
            print("Không tìm thấy text / No text detected.")
            return None, None, None

        # Tạo mask cho text
        text_mask = np.zeros(image_np.shape[:2], dtype=np.uint8)
        for (bbox, _, _) in results:
            (x1, y1), (x2, y2), _, _ = bbox
            # Thêm padding 30 pixel
            x1, y1 = max(int(x1) - 30, 0), max(int(y1) - 30, 0)
            x2, y2 = min(int(x2) + 30, image_np.shape[1]), min(int(y2) + 30, image_np.shape[0])
            text_mask[y1:y2, x1:x2] = 255

        # Mask nền
        bg_mask = cv2.bitwise_not(text_mask)

        # Lấy pixel
        text_pixels = image_np[text_mask == 255].reshape(-1, 3)
        bg_pixels = image_np[bg_mask == 255].reshape(-1, 3)

        # Kiểm tra pixel
        if len(text_pixels) < 2:
            print("Lỗi: Quá ít pixel text / Error: Too few text pixels.")
            return None, None, None
        if len(bg_pixels) < 2:
            print("Lỗi: Quá ít pixel nền / Error: Too few background pixels.")
            return None, None, None

        # Phân cụm màu (n_clusters=2)
        kmeans = KMeans(n_clusters=2, random_state=0)
        bg_labels = kmeans.fit_predict(bg_pixels)
        bg_color = np.mean(bg_pixels[bg_labels == np.bincount(bg_labels).argmax()], axis=0)

        text_labels = kmeans.fit_predict(text_pixels)
        text_pixel_color = np.mean(text_pixels[text_labels == np.bincount(text_labels).argmax()], axis=0)

        # Ước lượng alpha và màu chữ
        # Giả định màu chữ tối hơn (gần #4D4D4D), dùng kênh có tương phản lớn nhất
        alpha = None
        text_color = None
        try:
            # Tìm kênh RGB có độ lệch lớn nhất
            diffs = [abs(t - b) for t, b in zip(text_pixel_color, bg_color)]
            max_diff_channel = np.argmax(diffs)
            t, b = text_pixel_color[max_diff_channel], bg_color[max_diff_channel]
            # Ước lượng alpha: pixel = alpha * text + (1 - alpha) * bg
            assumed_text = 77  # Giá trị gần #4D4D4D (77/255)
            if abs(t - b) > 10:  # Đảm bảo đủ tương phản
                alpha = (t - b) / (assumed_text - b) if b != assumed_text else 1.0
                alpha = min(max(alpha, 0.1), 1.0)  # Giới hạn alpha [0.1, 1.0]
                # Ước lượng màu chữ
                text_color = [(t - (1 - alpha) * b) / alpha for t, b in zip(text_pixel_color, bg_color)]
                text_color = [min(max(int(c), 0), 255) for c in text_color]
            else:
                text_color = text_pixel_color  # Dùng màu pixel nếu không đủ tương phản
                alpha = 1.0
        except:
            text_color = text_pixel_color  # Fallback
            alpha = 1.0

        # Chuyển sang HEX
        bg_hex = '#{:02X}{:02X}{:02X}'.format(int(bg_color[0]), int(bg_color[1]), int(bg_color[2]))
        text_hex = '#{:02X}{:02X}{:02X}'.format(int(text_color[0]), int(text_color[1]), int(text_color[2]))

        return bg_hex, text_hex, alpha

# Chạy
get_color = GetColor()
bg_color, text_color, opacity = get_color.extract_colors("/Users/game/Desktop/chi/Detect_color/crop_image/crop_002_No bookmarks.png")
if bg_color and text_color and opacity is not None:
    print("Màu nền / Background color:", bg_color)
    print("Màu chữ / Text color:", text_color)
    print("Opacity của text / Text opacity:", round(opacity, 2))
else:
    print("Không lấy được màu hoặc opacity / Failed to get colors or opacity.")