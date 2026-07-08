from flask import Flask, render_template, request
import numpy as np
import base64
from PIL import Image
import io
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)

# ===========================
# Load model
# ===========================
MODEL_PATH = "keras_model.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = load_model(MODEL_PATH)

# ===========================
# Classes
# ===========================
CLASS_NAMES = ["USD", "WON", "BRITISH POUND", "YUAN", "EURO", "YEN"]

# Exchange rate → PHP
RATES = {
    "USD": 59.30,
    "WON": 0.041,
    "YEN": 0.37,
    "YUAN": 8.49,
    "BRITISH POUND": 79.45,
    "EURO": 68.9
}

# ===========================
# Crop function
# ===========================
def crop_banknote(pil_image, padding=0.05):
    w_img, h_img = pil_image.size
    w_box, h_box = int(w_img * 0.7), int(h_img * 0.4)
    x, y = (w_img - w_box) // 2, (h_img - h_box) // 2
    return pil_image.crop((x, y, x + w_box, y + h_box))

# ===========================
# Flask route
# ===========================
@app.route("/", methods=["GET", "POST"])
def index():
    detected_currency = None
    php_result = None

    if request.method == "POST":
        # Step 1: detect currency
        if "imageData" in request.form and request.form["imageData"] != "":
            try:
                image_data = request.form["imageData"].split(",")[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

                image = crop_banknote(image)
                image = image.resize((224, 224))
                img_array = np.array(image) / 255.0
                img_array = img_array.reshape(1, 224, 224, 3)

                prediction = model.predict(img_array)[0]
                detected_currency = CLASS_NAMES[int(np.argmax(prediction))]
            except Exception as e:
                detected_currency = f"Error detecting bill: {str(e)}"

        # Step 2: convert to PHP if user entered amount
        if "amount" in request.form and "currency_hidden" in request.form:
            try:
                amount = float(request.form["amount"])
                currency = request.form["currency_hidden"]
                if currency in RATES:
                    php_value = round(amount * RATES[currency], 2)
                    php_result = f"{amount} {currency} = {php_value} PHP"
            except Exception as e:
                php_result = f"Error: {str(e)}"

    return render_template(
        "index.html",
        detected_currency=detected_currency,
        php_result=php_result,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5003)
