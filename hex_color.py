import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
from PIL import Image

class GetColor:
    def __init__(self):
        pass

    def extract_colors(self, image_path):
        # Mở ảnh và chuyển sang RGB
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image).reshape(-1, 3)

        # Dùng KMeans để chia thành 2 cụm màu
        kmeans = KMeans(n_clusters=2, random_state=0)
        labels = kmeans.fit_predict(pixels)

        cluster0 = pixels[labels == 0]
        cluster1 = pixels[labels == 1]

        # Lấy màu phổ biến nhất trong mỗi cụm
        try:
            mode0 = self.get_mode_color(cluster0)
            mode1 = self.get_mode_color(cluster1)
        except Exception as e:
            print("Lỗi khi tính màu phổ biến:", e)
            return None

        # Cụm nhiều pixel hơn là nền
        if len(cluster0) > len(cluster1):
            background_color = mode0
            text_color = mode1
        else:
            background_color = mode1
            text_color = mode0

        # Convert RGB -> HEX
        background_hex = self.rgb_to_hex(background_color)
        text_hex = self.rgb_to_hex(text_color)

        return background_hex, text_hex

    def get_mode_color(self, pixels):
        color_counts = defaultdict(int)
        for pixel in pixels:
            color_counts[tuple(pixel)] += 1
        return max(color_counts, key=color_counts.get)

    def rgb_to_hex(self, rgb):
        return '#{:02X}{:02X}{:02X}'.format(*rgb)


# Ví dụ sử dụng:
get_color_ = GetColor()
bg_color, text_color = get_color_.extract_colors("/Users/game/Desktop/chi/Detect_color/crop_image/crop_002_No bookmarks.png")
print("Background color:", bg_color)
print("Text color:", text_color)
