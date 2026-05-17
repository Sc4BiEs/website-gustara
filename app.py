import json
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'gustara_cv_secret_key_2026'

# Load translations
with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

LANGUAGES = {
    'en': 'English',
    'id': 'Indonesia',
    'nl': 'Nederlands',
    'de': 'Deutsch',
    'ja': '日本語',
    'zh': '中文'
}

def get_translations(lang='en'):
    """Get translations for the given language, fallback to English."""
    if lang not in translations:
        lang = 'en'
    return translations[lang]

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    lang = session.get('lang', 'en')
    t = get_translations(lang)
    return dict(
        t=t,
        lang=lang,
        languages=LANGUAGES,
        current_path=request.path
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = session.get('lang', 'en')
    t = get_translations(lang)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        success_msg = t['contact_success'].replace('{name}', name)
        flash(success_msg, 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/set-language/<lang>')
def set_language(lang):
    """Change site language."""
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route('/set-theme/<theme>')
def set_theme(theme):
    """Change theme (light/dark)."""
    if theme in ['light', 'dark']:
        session['theme'] = theme
    return redirect(request.referrer or url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)