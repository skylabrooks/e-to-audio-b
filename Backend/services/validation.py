from werkzeug.utils import secure_filename

class ValidationService:
    @staticmethod
    def validate_file_upload(file):
        if not file or file.filename == "":
            return False, "No file selected"

        filename = secure_filename(file.filename)
        if not filename.lower().endswith((".txt", ".md")):
            return False, "Only .txt and .md files are allowed"

        return True, None