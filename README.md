# Currency Recognition System

A Flask web application that uses a Keras/TensorFlow image classification model to detect banknote currency from a camera or uploaded image, then converts the recognized amount to Philippine Peso (PHP) using fixed exchange rates.

## Features

- **Currency detection** — Classifies a banknote image into one of six currencies using a trained Keras model (`keras_model.h5`).
- **Automatic cropping** — Crops the input image to the center region (70% width, 40% height) before classification to focus on the banknote area.
- **PHP conversion** — Converts a user-entered amount in the detected currency to its PHP equivalent using preset exchange rates.
- **Simple web UI** — Single-page interface (`index.html`) that submits a base64-encoded image and displays detection + conversion results.

## Supported Currencies

| Currency | Rate to PHP |
|---|---|
| USD | 59.30 |
| WON | 0.041 |
| YEN | 0.37 |
| YUAN | 8.49 |
| BRITISH POUND | 79.45 |
| EURO | 68.9 |

> Exchange rates are hardcoded in `RATES` and should be updated periodically to reflect current market rates.

## Requirements

- Python 3.x
- Flask
- NumPy
- Pillow (PIL)
- TensorFlow (Keras)

Install dependencies:

```bash
pip install flask numpy pillow tensorflow
```

## Project Structure

```
.
├── app.py                # Main Flask application (this file)
├── keras_model.h5        # Trained Keras classification model (required)
├── templates/
│   └── index.html        # Frontend page (image capture/upload + result display)
└── README.md
```

> **Note:** `keras_model.h5` must be present in the project root, or the app will raise a `FileNotFoundError` on startup.

## How It Works

1. **Image capture/upload** — The frontend sends a base64-encoded image via the `imageData` form field.
2. **Preprocessing**:
   - Decode the base64 string into a PIL image (converted to RGB).
   - Crop to the center region via `crop_banknote()`.
   - Resize to `224x224`.
   - Normalize pixel values to `[0, 1]`.
   - Reshape to `(1, 224, 224, 3)` for model input.
3. **Prediction** — The model outputs class probabilities; the highest-scoring class is mapped to a currency name via `CLASS_NAMES`.
4. **Conversion** — If the user submits an `amount` along with the detected currency (`currency_hidden`), the app computes the PHP equivalent using `RATES`.
5. **Render** — Results (`detected_currency`, `php_result`) are passed back to `index.html`.

## Running the App

```bash
python app.py
```

The server starts in debug mode on port **5003**:

```
http://localhost:5003
```

## API / Form Fields

The single route `/` (GET/POST) expects the following form fields on POST:

| Field | Purpose |
|---|---|
| `imageData` | Base64 data URL of the captured/uploaded image (e.g., `data:image/png;base64,...`) |
| `amount` | Numeric amount to convert (optional, used with `currency_hidden`) |
| `currency_hidden` | Currency code matching a key in `RATES` (optional, typically auto-filled from detection result) |

## Known Limitations / Notes

- **Fixed crop region**: The center-crop assumes the banknote is roughly centered and fills most of the frame; poorly framed images may reduce accuracy.
- **Static exchange rates**: Rates are not fetched live — update `RATES` manually or integrate a live FX API for production use.
- **Debug mode**: `app.run(debug=True, ...)` is intended for development only; disable debug mode before deploying to production.
- **Error handling**: Detection and conversion errors are caught and shown as strings in the UI rather than raising exceptions, which is convenient for demos but should be hardened for production use.

## Possible Improvements

- Add confidence score display alongside the detected currency.
- Replace static `RATES` with a live exchange rate API.
- Add image validation (file size/type checks) before processing.
- Add unit tests for `crop_banknote()` and the prediction pipeline.
