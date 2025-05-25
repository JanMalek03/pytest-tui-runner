import pytest
import time

@pytest.mark.images
# @pytest.mark.parametrize(
#     "mode, image_name",
#     [
#         ("Add image", "image1.jpg"),
#         ("Add image", "image2.png"),
#         ("Delete image", "image1.jpg"),
#         ("Delete image", "image2.png"),
#         ("Copy image", "image1.jpg"),
#         ("Copy image", "image2.png")
#     ]
# )
def test_mode(mode, image_name):
    print(f"Mode: {mode}, Image name: {image_name}")
    time.sleep(1)
    assert True
