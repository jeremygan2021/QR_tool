from flask import Flask, render_template, request, send_file
import io
import qr_generator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url')
    if not url:
        return "Please enter a URL", 400
    
    style = request.form.get('style', 'rounded')
    try:
        size = int(request.form.get('size', 350))
    except ValueError:
        size = 350

    # Create a BytesIO object to hold the image data
    img_io = io.BytesIO()

    if style == 'gradient':
        # Use default gradient colors for now, or could extend form to accept colors
        qr_generator.generate_gradient_qr(
            data=url,
            output_file=img_io,
            img_size=(size, size),
            auto_adjust=True
        )
    else:
        # Default styles: rounded, circle, classic
        color = "#000000"
        if style == 'orange_circle':
             style = 'circle'
             color = "#FF5722"
        
        qr_generator.generate_styled_qr_code(
            data=url,
            output_file=img_io,
            style=style,
            color=color,
            img_size=(size, size),
            auto_adjust=True
        )

    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8711)
