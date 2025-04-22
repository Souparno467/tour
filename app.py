from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField
from auth import auth_bp
from models import get_user_by_id
from ml.recommender import generate_detailed_itinerary  # ✅ AI-powered itinerary function
from database import init_db
from reportlab.pdfgen import canvas
import io
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_key")

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Register auth blueprint
app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

class RecommendationForm(FlaskForm):
    hidden_tag = HiddenField()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    form = RecommendationForm()

    if request.method == 'POST':
        days = request.form.get('days', '7').strip()
        budget = request.form.get('budget', '').strip()
        climate = request.form.get('climate', '').strip()
        landscape = request.form.get('landscape', '').strip()
        transport = request.form.get('transport', '').strip()
        interests = request.form.get('preferences', '').strip()

        # ✅ AI selects a destination based on preferences and generates a full itinerary
        itinerary = generate_detailed_itinerary(days, budget, climate, landscape, transport, interests)

        print(f"DEBUG: AI-Suggested Destination and Itinerary Generated={bool(itinerary)}")

        return redirect(url_for('result', itinerary=itinerary, days=days))

    return render_template("recommendation_form.html", form=form)

@app.route('/result', methods=['GET'])
@login_required
def result():
    itinerary = request.args.get('itinerary', '')

    return render_template("result.html", itinerary=itinerary)

@app.route('/itinerary-pdf', methods=['GET', 'POST'])
@login_required
def itinerary_pdf():
    if request.method == "POST":
        itinerary = request.form.get('itinerary', '')
    else:
        itinerary = request.args.get('itinerary', '')

    if not itinerary.strip():
        return "❌ ERROR: No itinerary available to generate PDF."

    pdf_path = "static/travel_itinerary.pdf"
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "AI-Generated Travel Itinerary")

    pdf.setFont("Helvetica", 12)
    y_position = 730
    line_spacing = 20

    for paragraph in itinerary.split("\n\n"):  # ✅ Preserve paragraph breaks
        lines = paragraph.split("\n")
        for line in lines:
            pdf.drawString(100, y_position, line.strip())
            y_position -= line_spacing
            if y_position < 50:  # ✅ Prevent text overflow
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = 750

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())

    return send_file(pdf_path, as_attachment=True, download_name="Travel_Itinerary.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    print("🚀 Starting AI Travel Planner...")
    init_db()
    print("✅ Database initialized.")
    app.run(debug=True)
