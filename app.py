from flask import Flask, render_template, request, send_file
import io
import qr_generator
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Content processing
    content_type = request.form.get('content_type', 'url')
    data = ""
    
    if content_type == 'url':
        data = request.form.get('url', '')
        # Basic prefixing
        if data and not data.startswith(('http://', 'https://')):
            data = 'https://' + data
            
    elif content_type == 'wifi':
        ssid = request.form.get('wifi_ssid', '')
        password = request.form.get('wifi_password', '')
        encryption = request.form.get('wifi_encryption', 'WPA')
        hidden = request.form.get('wifi_hidden', 'false')
        data = f"WIFI:S:{ssid};T:{encryption};P:{password};H:{hidden};;"
        
    elif content_type == 'vcard':
        name = request.form.get('vcard_name', '')
        phone = request.form.get('vcard_phone', '')
        email = request.form.get('vcard_email', '')
        org = request.form.get('vcard_org', '')
        # Simple vCard 3.0 construction
        data = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nFN:{name}\nORG:{org}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
        
    elif content_type == 'email':
        email = request.form.get('email_address', '')
        subject = request.form.get('email_subject', '')
        body = request.form.get('email_body', '')
        data = f"mailto:{email}?subject={subject}&body={body}"
        
    elif content_type == 'text':
        data = request.form.get('text_content', '')

    if not data:
        return "Please enter valid content", 400

    # Styles and Colors
    style = request.form.get('style', 'rounded')
    bg_color_input = request.form.get('bg_color', '#FFFFFF')
    fg_color_input = request.form.get('fg_color', '#000000')
    is_transparent = request.form.get('transparent') == 'true'
    
    bg_color = "transparent" if is_transparent else bg_color_input
    color = fg_color_input

    # Size
    try:
        size = int(request.form.get('size', 350))
    except ValueError:
        size = 350
        
    # Logo Handling
    logo_obj = None
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename != '':
            try:
                logo_obj = Image.open(file.stream)
            except Exception as e:
                print(f"Error loading logo: {e}")

    # Format
    download_format = request.form.get('format', 'png')
    
    img_io = io.BytesIO()
    
    if download_format == 'svg':
        # Generate SVG
        svg_content = qr_generator.generate_svg_qr_code(
            data=data,
            output_file=img_io,
            color=color,
            bg_color=bg_color,
            style=style, # classic, rounded, circle
            box_size=max(10, size // 25), # approximate box size for svg
            logo_obj=logo_obj
        )
        img_io.seek(0)
        return send_file(img_io, mimetype='image/svg+xml', as_attachment=False, download_name='qrcode.svg')

    else:
        # Generate PNG
        if style == 'gradient':
            start_color = request.form.get('gradient_start', '#1E88E5')
            end_color = request.form.get('gradient_end', '#8BC34A')
            
            qr_generator.generate_gradient_qr(
                data=data,
                output_file=img_io,
                start_color=start_color,
                end_color=end_color,
                bg_color=bg_color,
                img_size=(size, size),
                auto_adjust=True,
                logo_obj=logo_obj
            )
        else:
            if style == 'orange_circle':
                 style = 'circle'
                 color = "#FF5722"
                 
            qr_generator.generate_styled_qr_code(
                data=data,
                output_file=img_io,
                style=style,
                color=color,
                bg_color=bg_color,
                img_size=(size, size),
                auto_adjust=True,
                logo_obj=logo_obj
            )

        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8711)
