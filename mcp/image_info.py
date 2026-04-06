from pathlib import Path
from PIL import Image, ImageFilter
from typing import Optional


def getImageInfo(image_path: str) -> dict:
    """이미지 파일 정보를 조회합니다."""
    try:
        # 이미지 파일을 열기
        with Image.open(image_path) as img:
            return {
                "success": True,
                "path": image_path,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": Path(image_path).stat().st_size,
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    info = getImageInfo(r"C:\Users\bluedove\Pictures\icon_me.png")

    print("\n💬 image:", info)
    