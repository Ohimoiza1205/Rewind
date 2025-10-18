import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('dzfrvzos4'),
    api_key=os.getenv('164893845881115'),
    api_secret=os.getenv('reM4Bp3RsHPUMvknYj-fSUUGx5s')
)

print("✅ Cloudinary configured!")
print(f"Cloud name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
