from flask import Flask, request, jsonify
import boto3
from config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_BUCKET,
    AWS_REGION
)

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:

        return jsonify({
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    s3.upload_fileobj(
        file,
        AWS_BUCKET,
        file.filename
    )

    url = (
        f"https://{AWS_BUCKET}.s3."
        f"{AWS_REGION}.amazonaws.com/"
        f"{file.filename}"
    )

    return jsonify({
        "message": "Upload Successful",
        "url": url
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True)
