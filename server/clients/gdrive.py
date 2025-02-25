from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.responses import log_exception


class GDrive:
    # Authenticate and create the PyDrive client
    # https://pypi.org/project/PyDrive2/
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    def upload(self, filename: str):
        try:
            file_drive = self.drive.CreateFile({"title": filename})
            file_drive.Upload()

            return "Image uploaded to Google Drive successfully!"

        except Exception as e:
            log_exception(
                message="Failed to upload to google drive",
                e=e,
            )
