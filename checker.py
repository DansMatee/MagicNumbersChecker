import os
import zipfile

EXTENSION_ALIASES = {
    "jpeg": "jpg",
    "jpe": "jpg",
    "mpeg": "mp4",
    "mpg": "mp4"
}

SIGNATURES = {
    "gif": {
        "signatures": ["47494638"],
        "offset": 0,
        "fileclass": "Picture"
    },
    "jpg": {
        "signatures": ["ffd8"],
        "offset": 0,
        "fileclass": "Picture"
    },
    "png": {
        "signatures": ["89504e470d0a1a0a"],
        "offset": 0,
        "fileclass": "Picture"
    },
    "exe": {
        "signatures": ["4d5a"],
        "offset": 0,
        "fileclass": "Windows"
    },
    "sh": {
        "signatures": ["2321"],
        "offset": 0,
        "fileclass": "Script"
    },
    "zip": {
        "signatures": [
            "504b0304",
            "504b0306",
            "504b0308"
        ],
        "offset": 0,
        "fileclass": "Compressed archive"
    },
    "mp4": {
        "signatures": [
            "6674797033677035",
            "667479704d534e56",
            "6674797069736f6d",
            "667479706d703432"
        ],
        "offset": 4,
        "fileclass": "Multimedia"
    }
}

def detect_zip_subtype(file_path):
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            names = z.namelist()

            if any(name.startswith("ppt/") for name in names):
                return "pptx"
            
            if any(name.startswith("word/") for name in names):
                return "docx"
            
            if any(name.startswith("xl/") for name in names):
                return "xlsx"
            
            if "META-INF/MANIFEST.MF" in names:
                return "jar"
            
        return "zip"
    except zipfile.BadZipFile:
        return "zip"

def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024

def magic_numbers_check(file_path):

    with open(file_path, "rb") as f:
        for file_type, data in SIGNATURES.items():
            signatures = data["signatures"]
            offset = data["offset"]

            for signature in signatures:
                f.seek(offset)

                bytes_to_read = int(len(signature) / 2)
                chunk = f.read(bytes_to_read).hex()

                if chunk.startswith(signature):
                    zip_subtype = None

                    if file_type == "zip":
                        subtype = detect_zip_subtype(file_path)
                        if subtype != "zip":
                            zip_subtype = subtype

                    return {
                        "file_type": file_type,
                        "file_subtype": zip_subtype,
                        "fileclass": data["fileclass"],
                        "signature": signature,
                        "offset": offset
                    }
            
        return {
            "file_type": "Unknown",
            "file_subtype": "Unknown",
            "fileclass": "Unknown",
            "signature": "None",
            "offset": 0
        }


def entry():
    while True:
        file = input("input file name and extension: ")

        if not os.path.exists(file):
            print("Specified file not found!")
            continue

        _, extension = os.path.splitext(file)
        file_extension = extension.replace(".", "").lower()
        file_extension = EXTENSION_ALIASES.get(file_extension, file_extension) # If alias is found, converts to its normalized version

        size = os.path.getsize(file)

        checked_type = magic_numbers_check(file)

        if checked_type["file_type"] == "Unknown":
            print("File type not defined in database")
            break


        print(f"Claimed extension: {file_extension}")
        print(f"Detected type: {checked_type['file_type']}")
        print(f"Detected Subtype: {checked_type['file_subtype'] or 'None'}")
        print(f"File Class: {checked_type['fileclass']}")
        print(f"Matched Signature: {checked_type['signature']}")
        print(f"Offset: {checked_type['offset']}")
        print(f"File Size: {format_size(size)}")
        
        if file_extension == checked_type["file_type"] or file_extension == checked_type["file_subtype"]:
            print("Result: MATCH")
        else:
            print("Result: WARNING")

        break


if __name__ == "__main__":
    entry()
    


        

    
