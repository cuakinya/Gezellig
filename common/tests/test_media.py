import io
import os
import shutil
import tempfile
from datetime import datetime, timedelta

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from common.images import upload_image_multipart
from debug.helpers import HelperClient
from users.models.user import User

MEDIA_ROOT = tempfile.mkdtemp(prefix="club-media-test-")


def png_bytes(size=(64, 64)):
    out = io.BytesIO()
    Image.new("RGB", size, (200, 10, 10)).save(out, format="PNG")
    return out.getvalue()


@override_settings(MEDIA_ROOT=MEDIA_ROOT, MEDIA_UPLOAD_URL="/upload/", APP_HOST="http://club.test")
class TestLocalMediaUpload(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create(
            email="uploader@example.com",
            membership_started_at=datetime.utcnow(),
            membership_expires_at=datetime.utcnow() + timedelta(days=30),
            slug="uploader",
            moderation_status=User.MODERATION_STATUS_APPROVED,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def path_from_url(self, url):
        return os.path.join(MEDIA_ROOT, url.split("/media/", 1)[1])

    def test_member_uploads_image(self):
        client = HelperClient(user=self.member).authorise()
        response = client.post(reverse("upload_media"), {"media": SimpleUploadedFile("pic.png", png_bytes())})

        self.assertEqual(response.status_code, 200)
        url = response.json()["uploaded"][0]
        self.assertTrue(url.startswith("http://club.test/media/"))
        self.assertTrue(os.path.exists(self.path_from_url(url)))

    def test_anonymous_is_rejected(self):
        response = self.client.post(reverse("upload_media"), {"media": SimpleUploadedFile("pic.png", png_bytes())})

        self.assertEqual(response.status_code, 403)

    def test_not_an_image_is_rejected(self):
        client = HelperClient(user=self.member).authorise()
        response = client.post(reverse("upload_media"), {"media": SimpleUploadedFile("x.png", b"not an image")})

        self.assertEqual(response.status_code, 400)

    def test_avatar_resized_and_converted_locally(self):
        url = upload_image_multipart("ava.png", io.BytesIO(png_bytes((800, 600))), resize=(192, 192), convert_to="jpg")

        self.assertTrue(url.endswith(".jpg"))
        with Image.open(self.path_from_url(url)) as image:
            self.assertLessEqual(max(image.size), 192)
            self.assertEqual(image.format, "JPEG")
