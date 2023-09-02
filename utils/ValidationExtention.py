

ALLOWED_EXTENSIONS = set(
    [
        ".png",
        ".jpeg",
        ".jpg",
        ".gif",
        ".tiff",
        ".pdf",
        ".heic",
        ".bmp",
        ".svg",
        ".ico",
    ]
)
# checking if the file are under the allowed format
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS