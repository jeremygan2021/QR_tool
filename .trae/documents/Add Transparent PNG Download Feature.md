# Add Transparent Background Download & Feature Roadmap

## Part 1: Implementation Plan - Transparent PNG Support

I will implement a feature to allow users to generate and download QR codes with a transparent background (removing the white background).

### 1. Backend Updates (`qr_generator.py`)

* Modify `generate_styled_qr_code` and `generate_gradient_qr` functions.

* Add logic to handle a specific `bg_color="transparent"` value.

* When transparent is selected, ensure the image is created in `RGBA` mode with a `(0, 0, 0, 0)` background color instead of white.

### 2. API Updates (`app.py`)

* Update the `/generate` route to accept a new form parameter: `transparent`.

* If `transparent` is true, pass `bg_color="transparent"` to the generator functions.

### 3. Frontend Updates (`templates/index.html`)

* **Visual Feedback**: Add a CSS checkerboard pattern behind the QR code preview area so users can verify the transparency.

* **Controls**: Add a "Remove Background" (背景去色) checkbox to the generation form.

* **Download Action**: Add a dedicated "Download Transparent PNG" button in the result section that specifically requests a transparent version of the current QR code.

## Part 2: Feature Recommendations

Here are practical features to consider for future updates, based on the current codebase:

1. **Custom Logo Upload**: The backend (`logo_path`) already supports this! You just need a file input in the HTML form to let users upload their own center icon.
2. **Color Pickers**: Replace the preset dropdowns with `<input type="color">` to allow users to pick *any* foreground/background color.
3. **Rich Content Types**: Add tabs for different data types:

   * **Wi-Fi**: Auto-connect to network.

   * **vCard**: Save contact info to phone.

   * **Email/SMS**: Pre-filled message templates.
4. **Vector Export**: Add support for SVG export (infinite scaling for print).
5. **Dynamic QR Codes**: (Advanced) Create a database to store short URLs that redirect to the actual content, allowing you to change the destination *after* printing the QR code.
6. 增加把logo嵌入qr code 并且不影响code 内容

   <br />

