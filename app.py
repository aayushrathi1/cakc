import streamlit as st
import random
from datetime import date, datetime
import hashlib
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import wave
import contextlib
import textwrap
import json
import base64
import datetime
import random
import time

# --- heart balloons via streamlit-extras ---
try:
    from streamlit_extras.let_it_rain import rain
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.add_vertical_space import add_vertical_space
except Exception:
    import sys, subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-extras"])
    from streamlit_extras.let_it_rain import rain
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.add_vertical_space import add_vertical_space

# ---------------------------
# APP CONFIG & STYLE
# ---------------------------
st.set_page_config(
    page_title="💖 Love Calculator", 
    layout="wide",
    page_icon="💖",
    initial_sidebar_state="expanded"
)
# --- Sidebar Section ---




# Enhanced CSS with animations and better styling
page_bg = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFDEE9 40%, #B5FAFC 90%);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
}

/* Headings with animations */
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif;
    text-align: center;
    color: #ff007f;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    animation: pulse 2s ease-in-out infinite alternate;
}

@keyframes pulse {
    0% { transform: scale(1); }
    100% { transform: scale(1.02); }
}

/* Enhanced result card with hover effects */
.result-card {
    background: linear-gradient(145deg, #ffffff, #f8f9ff);
    border-radius: 25px;
    padding: 60px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(255, 0, 127, 0.2);
    margin: 25px 0;
    font-size: 24px;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 0, 127, 0.1);
    position: relative;
}

/* Screenshot capture area - only the result box */
.screenshot-area {
    background: linear-gradient(145deg, #ffffff, #f8f9ff);
    border-radius: 25px;
    padding: 60px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(255, 0, 127, 0.2);
    margin: 25px 0;
    font-size: 24px;
    border: 2px solid rgba(255, 0, 127, 0.1);
}

.result-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 15px 40px rgba(255, 0, 127, 0.3);
}

.result-text {
    font-size: 82px;
    font-weight: 800;
    background: linear-gradient(45deg, #ff007f, #ff4da6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 10px 0;
    text-shadow: none;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { filter: drop-shadow(0 0 5px #ff007f); }
    to { filter: drop-shadow(0 0 20px #ff4da6); }
}

.sub-text {
    font-size: 28px;
    font-weight: 600;
    color: #333;
    margin-top: 15px;
}

.breakdown-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin: 25px 0;
}

.breakdown-item {
    background: linear-gradient(145deg, #fff0f6, #ffffff);
    border: 2px solid #ff4da6;
    border-radius: 20px;
    padding: 20px;
    font-size: 20px;
    line-height: 1.4;
    transition: all 0.3s ease;
}

.breakdown-item:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(255, 77, 166, 0.3);
}

.breakdown-item b {
    font-size: 24px;
    color: #ff007f;
}

/* Centered fortune and tips section */
.centered-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin: 0 auto;
    max-width: 800px;
}

.centered-section h3 {
    text-align: center;
    margin-bottom: 20px;
}

.fortune-tips-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
}

.fortune-box, .tips-box {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
}

/* Enhanced form styling */
.stTextInput > div > div > input,
.stDateInput > div > div > input {
    font-size: 20px !important;
    padding: 15px !important;
    border-radius: 15px !important;
    border: 2px solid #ffb3d6 !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: #ff007f !important;
    box-shadow: 0 0 10px rgba(255, 0, 127, 0.3) !important;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 15px !important;
    border: 2px solid #ffb3d6 !important;
}

.stSelectbox div[data-baseweb="select"] span {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #333 !important;
}

label {
    font-size: 24px !important;
    font-weight: 600 !important;
    color: #d1006b !important;
    margin-bottom: 8px !important;
}

/* Animated button */
.stButton button {
    font-size: 36px !important;
    padding: 20px 60px !important;
    background: linear-gradient(45deg, #ff4da6, #ff007f) !important;
    color: white !important;
    border-radius: 25px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 5px 20px rgba(255, 0, 127, 0.4) !important;
    transition: all 0.3s ease !important;
}

.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(255, 0, 127, 0.6) !important;
    background: linear-gradient(45deg, #e60073, #ff4da6) !important;
}

/* Sidebar enhancements - NO GIF */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f7, #f0f9ff);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 32px !important;
    color: #ff007f !important;
    font-family: 'Poppins', sans-serif;
}

/* Fun stats cards */
.stats-card {
    background: linear-gradient(135deg, #ffffff, #fff0f7);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border-left: 5px solid #ff4da6;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Loading animation */
.loading-heart {
    font-size: 48px;
    animation: heartbeat 1s ease-in-out infinite;
}

@keyframes heartbeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* Social share buttons */
.share-button {
    display: inline-block;
    padding: 15px 25px;
    margin: 10px;
    background: linear-gradient(45deg, #ff4da6, #ff007f);
    color: white;
    text-decoration: none;
    border-radius: 20px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.share-button:hover {
    background: linear-gradient(45deg, #e60073, #ff4da6);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4);
}

/* Screenshot download styling */
.download-section {
    text-align: center;
    margin: 20px 0;
    padding: 20px;
    background: linear-gradient(145deg, #fff0f7, #ffffff);
    border-radius: 15px;
    border: 2px solid #ff4da6;
}
</style>
"""
st.markdown(
    """
    <style>
    .love-tagline {
        font-size: 42px;
        font-style: italic;
        text-align: center;
        color: #ff007f;
        text-shadow: 0px 0px 8px rgba(255,0,127,0.7), 0px 0px 12px rgba(255,0,127,0.5);
        margin-bottom: 15px;
    }
    </style>

    <div class="love-tagline">
        💕 Test Your Love, Feel the Magic 🔮
    </div>
    """,
    unsafe_allow_html=True)
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------------------
# SESSION STATE & USER STATS
# ---------------------------
if 'total_calculations' not in st.session_state:
    st.session_state.total_calculations = 0
if 'user_history' not in st.session_state:
    st.session_state.user_history = []

# ---------------------------
# ENHANCED ALGORITHM WITH MORE FACTORS
# ---------------------------
def get_zodiac(month, day):
    zodiac_data = {
        "♈ Aries": [(3, 21), (4, 19)],
        "♉ Taurus": [(4, 20), (5, 20)],
        "♊ Gemini": [(5, 21), (6, 20)],
        "♋ Cancer": [(6, 21), (7, 22)],
        "♌ Leo": [(7, 23), (8, 22)],
        "♍ Virgo": [(8, 23), (9, 22)],
        "♎ Libra": [(9, 23), (10, 22)],
        "♏ Scorpio": [(10, 23), (11, 21)],
        "♐ Sagittarius": [(11, 22), (12, 21)],
        "♑ Capricorn": [(12, 22), (1, 19)],
        "♒ Aquarius": [(1, 20), (2, 18)],
        "♓ Pisces": [(2, 19), (3, 20)]
    }
    
    for sign, dates in zodiac_data.items():
        if len(dates) == 2:
            start_month, start_day = dates[0]
            end_month, end_day = dates[1]
            
            if start_month == end_month:
                if start_day <= day <= end_day and month == start_month:
                    return sign
            else:
                if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                    return sign
    
    return "♓ Pisces"

def _seeded_rng(*parts):
    seed_src = "|".join(map(str, parts)).lower()
    seed_int = int(hashlib.sha256(seed_src.encode()).hexdigest(), 16) % (2**32 - 1)
    return random.Random(seed_int)

def _bounded(x, lo, hi):
    return max(lo, min(hi, x))

def calculate_name_compatibility(name1, name2):
    """Name-based compatibility using letter frequencies"""
    name1_lower = name1.lower().replace(" ", "")
    name2_lower = name2.lower().replace(" ", "")
    
    # Count common letters
    common_letters = set(name1_lower) & set(name2_lower)
    total_unique = len(set(name1_lower) | set(name2_lower))
    
    if total_unique == 0:
        return 0
    
    return min(10, int((len(common_letters) / total_unique) * 15))

def calculate_age_compatibility(dob1, dob2):
    """Age difference factor"""
    age1 = (date.today() - dob1).days // 365
    age2 = (date.today() - dob2).days // 365
    age_diff = abs(age1 - age2)
    
    if age_diff <= 2:
        return 8
    elif age_diff <= 5:
        return 6
    elif age_diff <= 10:
        return 4
    else:
        return 2

def compute_breakdown_and_score(name1, name2, dob1, dob2, answers1, answers2):
    """Enhanced compatibility calculation"""
    rng = _seeded_rng(name1, name2, dob1, dob2, *answers1, *answers2)

    # Base score
    base = rng.randint(35, 85)

    # Quiz matching
    matches = sum(a1 == a2 for a1, a2 in zip(answers1, answers2))
    if matches >= 3:
        base += 12
    elif matches == 2:
        base += 6
    elif matches == 1:
        base += 2
    else:
        base -= 3

    # Zodiac compatibility
    z1, z2 = get_zodiac(dob1.month, dob1.day), get_zodiac(dob2.month, dob2.day)
    zodiac_pair = {z1.split()[1], z2.split()[1]}

    excellent_pairs = [
        {"Aries", "Leo"}, {"Gemini", "Libra"}, {"Cancer", "Pisces"},
        {"Taurus", "Cancer"}, {"Virgo", "Capricorn"}, {"Scorpio", "Pisces"},
        {"Sagittarius", "Aries"}, {"Aquarius", "Gemini"}, {"Leo", "Sagittarius"}
    ]
    
    good_pairs = [
        {"Aries", "Gemini"}, {"Taurus", "Virgo"}, {"Leo", "Libra"},
        {"Cancer", "Scorpio"}, {"Virgo", "Pisces"}, {"Libra", "Sagittarius"}
    ]

    if zodiac_pair in excellent_pairs:
        base += 8
    elif zodiac_pair in good_pairs:
        base += 5
    elif z1.split()[1] == z2.split()[1]:
        base += 3

    # Name compatibility
    name_compat = calculate_name_compatibility(name1, name2)
    base += name_compat

    # Age compatibility
    age_compat = calculate_age_compatibility(dob1, dob2)
    base += age_compat

    # Individual breakdown scores
    romance = _bounded(rng.randint(6, 10) + (2 if "❤️" in answers1[1] or "❤️" in answers2[1] else 0), 1, 10)
    memes = _bounded(rng.randint(5, 10) + (3 if ("😂" in answers1[1] and "😂" in answers2[1]) else 0), 1, 10)
    music = _bounded(rng.randint(5, 10) + (3 if answers1[2] == answers2[2] else 0), 1, 10)
    texting = _bounded(rng.randint(5, 10) + (2 if answers1[1] == answers2[1] else 0), 1, 10)

    # Date preferences bonus
    if answers1[0] == answers2[0]:
        base += 4
        romance = _bounded(romance + 1, 1, 10)

    love_percent = _bounded(base, 10, 99)

    # Easter eggs
    easter = None
    n1, n2 = name1.lower(), name2.lower()
    
    celebrity_pairs = {
        "taylor swift": "🎶 This love story might just be legendary! ✨",
        "ryan reynolds": "💫 Deadpool-level chemistry detected!",
        "brad pitt": "🎬 Hollywood romance vibes incoming!",
        "beyonce": "👑 Queen-level love energy!",
        "elon musk": "🚀 Your love could reach Mars!",
    }
    
    for celeb, message in celebrity_pairs.items():
        if celeb in n1 or celeb in n2:
            easter = message
            love_percent = max(love_percent, 85)
            break

    # Special zodiac combinations
    if {"Aries", "Scorpio"} == zodiac_pair:
        easter = "🔥 Explosive passion detected! Handle with care!"
        romance = min(10, romance + 2)
    elif {"Gemini", "Sagittarius"} == zodiac_pair:
        easter = "✈️ Adventure couple alert! Pack your bags!"

    breakdown = {
        "🔥 Romance Potential": romance,
        "😂 Meme Compatibility": memes,
        "🎶 Playlist Vibes": music,
        "💬 Texting Energy": texting,
        "📛 Name Harmony": min(10, name_compat + 3),
        "🎂 Age Sync": min(10, age_compat + 2),
    }

    quiz_note = f"Quiz alignment: {matches}/4 • Name compatibility: {name_compat}/10 • Age factor: {age_compat}/10"
    return love_percent, breakdown, quiz_note, easter

# ---------------------------
# PERSONALIZED FORTUNES & TIPS
# ---------------------------
def todays_fortune(name1, name2, love_percent):
    high_score_fortunes = [
        "💍 Wedding bells may not be far away — destiny is smiling on you both.",
        "💖 The universe just whispered: perfect match alert!",
        "🌹 A timeless romance — like wine, it only gets better.",
        "✨ Stars align for your love — cosmic blessings ahead.",
        "🔥 Passion + trust = an unbreakable bond.",
        "💘 This is the kind of love poets write about.",
        "🌈 Your souls are dancing in perfect harmony.",
        "🌟 A match written in stardust and moonlight.",
        "💕 This love has all the makings of forever.",
        "🎶 Even Cupid’s playlist is jealous of this connection."
    ]
    
    medium_score_fortunes = [
       "🌱 A little patience and this love could bloom beautifully.",
        "⚡ Sparks are there — now it’s about keeping the flame alive.",
        "🌙 A story still unfolding… the ending is in your hands.",
        "💕 Potential is strong, nurture it with care.",
        "🌹 Sweet, but it could use more watering.",
        "✨ Magic is there — but every spell needs belief.",
        "💖 Two hearts that need a little fine-tuning.",
        "🔥 Chemistry exists… now build the trust.",
        "🎢 Love’s rollercoaster — thrilling, but hold on tight.",
        "🌈 Rainbow ahead, but a few clouds may pass first."
    ]
    
    low_score_fortunes = [
        "🌱 A little patience and this love could bloom beautifully.",
        "⚡ Sparks are there — now it’s about keeping the flame alive.",
        "🌙 A story still unfolding… the ending is in your hands.",
        "💕 Potential is strong, nurture it with care.",
        "🌹 Sweet, but it could use more watering.",
        "✨ Magic is there — but every spell needs belief.",
        "💖 Two hearts that need a little fine-tuning.",
        "🔥 Chemistry exists… now build the trust.",
        "🎢 Love’s rollercoaster — thrilling, but hold on tight.",
        "🌈 Rainbow ahead, but a few clouds may pass first."
    ]
    
    rng = _seeded_rng(name1, name2, date.today().isoformat())
    
    if love_percent >= 75:
        return rng.choice(high_score_fortunes)
    elif love_percent >= 50:
        return rng.choice(medium_score_fortunes)
    else:
        return rng.choice(low_score_fortunes)

def get_relationship_tips(breakdown, love_percent):
    """Personalized tips based on results"""
    tips = []
    
    if breakdown["🔥 Romance Potential"] < 6:
        tips.append("💡 Try planning surprise micro-dates: coffee, sunset walks, or stargazing!")
    
    if breakdown["😂 Meme Compatibility"] < 6:
        tips.append("📱 Share funny content that reminds you of each other - inside jokes build bonds!")
    
    if breakdown["🎶 Playlist Vibes"] < 6:
        tips.append("🎵 Create a collaborative playlist and add one song each week!")
    
    if breakdown["💬 Texting Energy"] < 6:
        tips.append("💬 Try voice messages instead of texts - tone conveys so much more emotion!")
    
    if love_percent >= 80:
        tips.append("🌟 Your compatibility is amazing! Focus on building deeper emotional intimacy.")
    elif love_percent >= 60:
        tips.append("💪 You have great potential! Work on communication and shared experiences.")
    else:
        tips.append("🌱 Take it slow and focus on friendship first - the best relationships grow naturally!")
    
    return tips[:3]  # Return top 3 most relevant tips

# ---------------------------
# SCREENSHOT & SHARING FUNCTIONS
# ---------------------------
def generate_share_text(name1, name2, love_percent):
    """Generate shareable social media text"""
    if love_percent >= 80:
        return f"🔥 {name1} + {name2} = {love_percent}% compatibility! We're basically soulmates! 💕 #LoveCalculator #Soulmates"
    elif love_percent >= 60:
        return f"✨ {name1} + {name2} scored {love_percent}%! Not bad at all 😏 #LoveCalculator #Compatibility"
    else:
        return f"🤷‍♀️ {name1} + {name2} got {love_percent}%... guess we'll stick to being friends! 😂 #LoveCalculator #JustFriends"

def create_result_screenshot(name1, name2, love_percent, breakdown, message, zodiac1, zodiac2):
    """Create a screenshot-ready image of just the result box"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Image dimensions
        width, height = 800, 900
        
        # Create image with gradient background
        img = Image.new('RGB', (width, height), '#ffffff')
        draw = ImageDraw.Draw(img)
        
        # Load font (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", 40)
            score_font = ImageFont.truetype("arial.ttf", 80)
            text_font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = score_font = text_font = small_font = ImageFont.load_default()
        
        # Draw background with rounded corners effect
        draw.rounded_rectangle([20, 20, width-20, height-20], radius=25, fill="#f8f9ff", outline="#ff4da6", width=3)
        
        # Title
        title = f"💌 {name1} ❤️ {name2} 💌"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 50), title, fill="#ff007f", font=title_font)
        
        # Score
        score_text = f"{love_percent}%"
        score_bbox = draw.textbbox((0, 0), score_text, font=score_font)
        score_width = score_bbox[2] - score_bbox[0]
        draw.text(((width - score_width) // 2, 120), score_text, fill="#ff007f", font=score_font)
        
        # Compatibility text
        compat_text = "Compatibility"
        compat_bbox = draw.textbbox((0, 0), compat_text, font=text_font)
        compat_width = compat_bbox[2] - compat_bbox[0]
        draw.text(((width - compat_width) // 2, 220), compat_text, fill="#666", font=text_font)
        
        # Breakdown grid
        y_start = 280
        items = list(breakdown.items())
        for i, (category, score) in enumerate(items):
            x = 60 + (i % 2) * 340
            y = y_start + (i // 2) * 80
            
            # Category box
            draw.rounded_rectangle([x, y, x + 300, y + 60], radius=15, fill="#fff0f7", outline="#ff4da6", width=2)
            
            # Category text
            cat_short = category.split()[1] if len(category.split()) > 1 else category
            text = f"{cat_short}: {score}/10"
            draw.text((x + 15, y + 20), text, fill="#d1006b", font=text_font)
        
        # Message
        y_msg = 520
        # Wrap message text
        max_chars = 60
        if len(message) > max_chars:
            words = message.split()
            lines = []
            current_line = []
            for word in words:
                if len(" ".join(current_line + [word])) <= max_chars:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
        else:
            lines = [message]
        
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text(((width - line_width) // 2, y_msg), line, fill="#333", font=text_font)
            y_msg += 35
       # --- Zodiac compatibility messages ---
# Zodiac messages (randomized instead of always the same)
        zodiac_messages = [
    "🌌 Cosmic Chemistry ✨",
    "💖 A celestial match made in the stars!",
    "🔥 Passion written in the constellations!",
    "🌹 The universe approves of this duo!",
    "✨ Fated to find each other!",
    "💫 Sparks shining brighter than starlight!",
    "🌟 Guided by destiny itself!",
    "💕 The cosmos sings for this love!",
    "🌙 A lunar-blessed connection!",
    "☀️ A solar-charged romance!",
    "🌈 Love written in rainbow skies!",
    "⭐ A stellar bond beyond time!",
    "🌠 Shooting stars celebrate this union!",
    "🔮 Destiny weaves your paths together!",
    "🌍 A grounded yet cosmic connection!",
    "🪐 Love orbiting in perfect harmony!",
]
        
        zodiac_message = random.choice(zodiac_messages)

        zodiac_text = f"{zodiac1} ✨ + {zodiac2} = {zodiac_message}"
        zodiac_bbox = draw.textbbox((0, 0), zodiac_text, font=text_font)
        zodiac_width = zodiac_bbox[2] - zodiac_bbox[0]
        draw.text(((width - zodiac_width) // 2, y_msg + 20), zodiac_text, fill="#ff007f", font=text_font)

        # Footer
        footer = "✨ Love Calculator Results ✨"
        footer_bbox = draw.textbbox((0, 0), footer, font=small_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        draw.text(((width - footer_width) // 2, height - 50), footer, fill="#999", font=small_font)
        
        # Convert to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
        
    except Exception as e:
        st.error(f"Error creating screenshot: {e}")
        return None

# ---------------------------
# ENHANCED SIDEBAR (WITHOUT GIF)
# ---------------------------
def display_enhanced_sidebar():
    # Local imports to avoid conflicts with the global "import datetime"
    import time
    from datetime import date, datetime as dt

    st.sidebar.title("💘 Love Calculator Stats")

    # --- Dynamic Global Stats ---
    launch_date = date(2024, 1, 1)  # pretend launch date
    days_running = (date.today() - launch_date).days

    # Use safe defaults if session keys aren't set yet
    total_calc = st.session_state.get("total_calculations", 0)

    base_total_couples = 50_000
    couples_per_day = 300

    # Small live bump that changes each hour so numbers feel "alive"
    rng_hourly_bump = random.Random(dt.now().strftime("%Y-%m-%d-%H-bump"))
    live_bump = rng_hourly_bump.randint(0, 120)

    total_couples = base_total_couples + days_running * couples_per_day + live_bump + total_calc

    # Stable accuracy per hour (94–98%)
    rng_hourly_acc = random.Random(dt.now().strftime("%Y-%m-%d-%H-acc"))
    accuracy_rate = rng_hourly_acc.randint(94, 98)

    # Stable perfect matches per day (30–40% of total)
    rng_daily = random.Random(date.today().isoformat() + "-pm")
    perfect_share = 0.30 + 0.10 * rng_daily.random()
    perfect_matches = int(total_couples * perfect_share)

    # --- Sidebar HTML ---
    html = f"""
    <div class="stats-card">
        <h4>🌟 Global Stats</h4>
        <p><strong>{total_couples:,}</strong> couples analyzed</p>
        <p><strong>{perfect_matches:,}</strong> perfect matches found</p>
        <p><strong>{accuracy_rate}%</strong> accuracy rate</p>
    </div>
    """
    st.sidebar.markdown(html, unsafe_allow_html=True)

    # --- Live Ticker ---
    st.sidebar.markdown("### 🔔 Latest Updates")
    ticker_placeholder = st.sidebar.empty()
    ticker_messages = [
        "💖 A new couple just matched!",
        "💕 Love score calculated!",
        "🌹 Sparks are flying for two people!",
        "🔥 Another perfect match found!",
        "✨ Someone just tested their love destiny!"
    ]

    # Show a few quick updates without needing any global imports
    for _ in range(3):
        ticker_placeholder.write(random.choice(ticker_messages))
        time.sleep(0.4)

    # Fun facts with rotation
    fun_facts = [
         "💘 Couples who laugh together are more likely to have a stronger bond.",
    "💖 Holding hands can reduce stress and lower blood pressure.",
    "🌹 Kissing boosts your immune system and burns calories (about 2–3 per kiss!).",
    "💕 The longest marriage on record lasted over 86 years!",
    "😂 Men are more likely to say 'I love you' first in a relationship.",
    "✨ When you look at someone you love, your pupils dilate.",
    "💡 Hugs release oxytocin, also known as the ‘love hormone’.",
    "🌍 Ancient Greeks had 7 different words for love, each describing a different type.",
    "🎶 Listening to music together strengthens emotional bonds.",
    "💌 Couples who share new experiences together build stronger memories.",
    "🌙 Falling in love activates the same part of the brain as addictive substances.",
    "💕 People with strong social and romantic connections live longer on average.",
    "😂 The heart symbol ♥️ was first used to represent love in the 13th century.",
    "🌹 Cuddling before sleep can help you rest better and feel happier.",
    "💖 Couples who make fun of each other in a playful way are often happier.",
    "✨ Saying ‘thank you’ often is proven to improve relationships.",
    "🎶 Your heartbeat can synchronize with your partner’s when you hug or hold hands.",
    "🌍 In Japan, Valentine’s Day is celebrated by women giving chocolates to men!",
    "💌 Writing love letters can increase happiness — even if you never send them.",
    "😂 The average person will fall in love about 3 times in their lifetime.",
    "💕 Love can relieve pain — even looking at a picture of your partner can ease discomfort.",
    "🌙 Long-distance couples often report stronger communication skills.",
    "💡 Sharing food increases bonding (yes, even if you steal fries!).",
    "💖 Studies show that happily married couples have healthier hearts.",
    "🌹 Couples who smile in their wedding photos are less likely to divorce.",
    "✨ Butterflies in your stomach are caused by adrenaline when you see your crush.",
    "😂 Penguins propose with a pebble — they give one to their mate as a gift!",
    "💕 Saying your partner’s name often strengthens intimacy.",
    "🌍 In some cultures, couples plant trees together as a symbol of lasting love.",
    "🎶 Listening to love songs actually increases romantic feelings.",
    "💌 Couples who text playful or funny messages report higher satisfaction.",
    "🌙 Eye contact for just 4 minutes can increase feelings of love.",
    "💖 People who believe in love at first sight are more likely to experience it."
    ]
    
    fact_index = (st.session_state.total_calculations % len(fun_facts))
    st.sidebar.info(fun_facts[fact_index])
    
    st.sidebar.markdown("---")
    
    # Daily love quote
    love_quotes = [
         "💖 Love is not about how many days you’ve been together, but how much you love each other every single day.",
    "🌹 A true relationship is two imperfect people refusing to give up on each other.",
    "✨ Sometimes, the little things are the biggest things in love.",
    "😂 Love is sharing your popcorn… even if you want it all for yourself.",
    "💌 A simple text saying ‘I miss you’ can brighten someone’s entire day.",
    "🎶 Every love story is beautiful, but ours will always be my favorite.",
    "💡 Tip: Surprise them today — even a small gesture can make big memories!",
    "💕 Falling in love is easy. Staying in love takes effort and kindness every day.",
    "🌙 The best feeling is when you look at them, and they’re already looking at you.",
    "😂 Love is when you go out to eat and give them most of your fries without making them ask.",
    "💖 When I follow my heart, it always leads me to you.",
    "🌹 A kiss is a lovely trick designed by nature to stop speech when words become superfluous.",
    "💡 Tip: Write them a short handwritten note — old-fashioned love never goes out of style.",
    "💘 Distance means so little when someone means so much.",
    "😂 A relationship is just two people constantly asking what they want to eat, until one of them dies.",
    "✨ Love is like the wind, you can’t see it but you can feel it.",
    "🌹 The greatest happiness of life is the conviction that we are loved.",
    "💡 Tip: Take a moment to say ‘thank you’ — gratitude strengthens love.",
    "💖 Love doesn’t make the world go round. Love is what makes the ride worthwhile.",
    "😂 If you love someone, let them nap. Always let them nap. 💤",
    "🌙 You’re my favorite notification.",
    "🎶 With you, every love song suddenly makes sense.",
    "💡 Tip: Hug longer today. A 20-second hug can release happy hormones.",
    "🌹 To love is nothing. To be loved is something. But to love and be loved, that’s everything.",
    "💖 You are my today and all of my tomorrows.",
    "😂 Couples who laugh together, last together.",
    "💡 Tip: Call them, even for a minute — your voice might be the highlight of their day.",
    "✨ A successful relationship requires falling in love many times, always with the same person.",
    "💕 A heart that loves is always young.",
    "🌙 Forever is a long time, but I wouldn’t mind spending it with you."
    ]
    
    quote_index = hash(str(date.today())) % len(love_quotes)
    st.sidebar.success(f"**Today's Quote:** {love_quotes[quote_index]}")
    
    # NO GIF IMAGE - Removed this section completely
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 About Love Calculator")
    st.sidebar.info("Our advanced algorithm considers zodiac compatibility, personality traits, name harmony, and age factors to give you the most accurate love prediction!")

# ---------------------------
# ENHANCED QUIZ QUESTIONS
# ---------------------------
def get_enhanced_quiz_questions():
    """Return more sophisticated quiz questions"""
    return {
        "date_options": [
            "🌹 A candlelight dinner at a cozy restaurant",
    "☕ A cute coffee shop with board games",
    "🎬 A movie night under the stars (outdoor cinema or rooftop)",
    "🏞️ A walk in the park or botanical garden",
    "🍦 Ice cream date at a local shop",
    "🎡 A funfair or amusement park",
    "🏖️ A beach picnic at sunset",
    "🎶 A live music concert or open mic night",
    "🍕 Making homemade pizza together",
    "🖼️ Visiting an art gallery or museum",
    "🎳 Bowling or mini-golf night",
    "🌙 Stargazing with blankets and hot cocoa",
    "🚴 A bike ride adventure",
    "🍓 Fruit picking at a farm",
    "🔥 A cozy bonfire night"
        ],
        "text_styles": [
            "📲 Short & sweet",
            "😂 Meme master mode", 
            "❤️ Long heartfelt messages",
            "⏳ Thoughtful & slow",
            "📸 Pictures speak louder",
            "🎵 Song lyrics & quotes"
            "⚡ Fast & Correct"
        ],
        "music_vibes": [
            "🎧 Chill lo-fi beats",
            "🎸 Indie & alternative", 
            "🎤 Pop & mainstream hits",
            "🎻 Classical & orchestral",
            "🤘 Rock & metal energy",
            "🎺 Jazz & blues soul",
            "💔 Heartbreaking"
        ],
        "conflict_styles": [
            "🕊️ Talk it out calmly",
            "🧊 Need space to think", 
            "😂 Humor defuses tension",
            "⏱️ Quick apology & move on",
            "📝 Write out feelings first",
            "🤗 Physical affection helps"
        ],
        "weekend_plans": [
            "🏠 Netflix & chill at home",
            "🌲 Outdoor adventures",
            "🛍️ Shopping & exploring city",
            "👥 Hanging with friends",
            "📚 Quiet reading & relaxation",
            "🎪 Trying new experiences"
            "😴 Sleeping and cuddle"
        ]
    }

# ---------------------------
# MAIN APP
# ---------------------------

# Enhanced header with animation
colored_header(
    label="💖 Ultimate Love Calculator 💖",
    description="✨ Discover your romantic compatibility with advanced algorithms ✨",
    color_name="red-70"
)

# Sidebar (WITHOUT GIF)
display_enhanced_sidebar()

add_vertical_space(2)

# ---------------------------
# ENHANCED INPUT FORM
# ---------------------------
with st.form("enhanced_love_form", clear_on_submit=False):
    st.markdown("### 👫 Tell us about yourselves!")
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### 💁 About You")
        name1 = st.text_input("Your Name", placeholder="Enter your first name", key="name1")
        gender1 = st.selectbox("Your Gender", ["Select Gender", "Male 👨", "Female 👩", "Other 🌈"], index=0, key="gender1")
        dob1 = st.date_input("Your Birthday", min_value=date(1500,1,1), max_value=date(2100,12,31), key="dob1")

        st.markdown("#### 🎭 Your Preferences")
        quiz_data = get_enhanced_quiz_questions()
        
        q1_date_1 = st.selectbox("Perfect date idea:", quiz_data["date_options"], key="q1a")
        q2_text_1 = st.selectbox("Your texting style:", quiz_data["text_styles"], key="q2a")
        q3_music_1 = st.selectbox("Music taste:", quiz_data["music_vibes"], key="q3a")
        q4_conf_1 = st.selectbox("How you handle conflict:", quiz_data["conflict_styles"], key="q4a")
        q5_weekend_1 = st.selectbox("Ideal weekend:", quiz_data["weekend_plans"], key="q5a")

    with col2:
        st.markdown("#### 🥰 About Your Crush")
        name2 = st.text_input("Their Name", placeholder="Enter their first name", key="name2")
        gender2 = st.selectbox("Their Gender", ["Select Gender", "Male 👨", "Female 👩", "Other 🌈"], index=0, key="gender2")
        dob2 = st.date_input("Their Birthday", min_value=date(1500,1,1), max_value=date(2100,12,31), key="dob2")

        st.markdown("#### 🎭 Their Preferences (your best guess)")
        
        q1_date_2 = st.selectbox("Their perfect date idea:", quiz_data["date_options"], key="q1b")
        q2_text_2 = st.selectbox("Their texting style:", quiz_data["text_styles"], key="q2b")
        q3_music_2 = st.selectbox("Their music taste:", quiz_data["music_vibes"], key="q3b")
        q4_conf_2 = st.selectbox("How they handle conflict:", quiz_data["conflict_styles"], key="q4b")
        q5_weekend_2 = st.selectbox("Their ideal weekend:", quiz_data["weekend_plans"], key="q5b")

    add_vertical_space(2)
    
    
    # Enhanced submit button
    submitted = st.form_submit_button("💘 Calculate Our Love Compatibility! 💘", use_container_width=True)

# ---------------------------
if submitted:
    if (name1.strip() == "" or name2.strip() == "" or 
        gender1 == "Select Gender" or gender2 == "Select Gender"):
        st.error("⚠️ Please fill in all the required information!")
    else:
        # Show loading animation with progress bar
        with st.spinner('🔮 Consulting the love algorithms...'):
            progress_placeholder = st.empty()
            progress = progress_placeholder.progress(0)

            for percent in range(0, 101, 10):
                time.sleep(0.1)  # smooth animation
                progress.progress(percent)

            # ✅ Clear progress bar after completion
            progress_placeholder.empty()

        # 🎉 Random fun success message
        success_messages = [
            "✨ Love destiny calculated! 💖",
            "💕 Cupid just delivered the results!",
            "🌹 Sparks of destiny revealed!",
            "🔥 The chemistry has been analyzed!",
            "💘 The love connection has been unlocked!",
            "⭐ Your cosmic love score is ready!"
        ]
        st.success(random.choice(success_messages))

        
        # Update session state
        st.session_state.total_calculations += 1
        
        answers1 = [q1_date_1, q2_text_1, q3_music_1, q4_conf_1, q5_weekend_1]
        answers2 = [q1_date_2, q2_text_2, q3_music_2, q4_conf_2, q5_weekend_2]

        love_percent, breakdown, quiz_note, easter = compute_breakdown_and_score(
            name1, name2, dob1, dob2, answers1, answers2
        )

        # Store in history
        st.session_state.user_history.append({
            'names': f"{name1} + {name2}",
            'score': love_percent,
            'date': date.today().isoformat()
        })

        zodiac1 = get_zodiac(dob1.month, dob1.day)
        zodiac2 = get_zodiac(dob2.month, dob2.day)

        # Enhanced fun messages based on score
        if love_percent >= 85:
            fun_messages = [
               "💖 Your hearts are basically twins!",
    "🌹 True soulmates! Nothing can break this bond.",
    "✨ A love written in the stars ✨",
    "💕 Your connection is legendary!",
    "🔥 Sparks are flying everywhere!",
    "🎶 Every love song was written for you two.",
    "💌 Perfect match alert!",
    "🌍 The universe approves of your love!",
    "🌙 Love this strong shines brighter than the moon.",
    "💖 You two are couple goals forever.",
    "💕 Together, you’re unstoppable.",
    "🌹 The kind of love poets dream about.",
    "🎉 Happily ever after has already begun!",
    "💡 You’re destined for each other.",
    "💖 Cupid deserves a raise for this match!",
    "🍯 Sweet as honey, strong as fire.",
    "🌊 Like the ocean and the shore — inseparable.",
    "🔥 A fiery love that will never burn out.",
    "💌 Two hearts, one soul.",
    "✨ Your love story could make a bestseller."
            ]
        elif love_percent >= 75:
            fun_messages = [
                "💕 Love is definitely in the air!",
    "🌹 You two bring out the best in each other.",
    "💖 A strong match with endless potential!",
    "🔥 Sparks are there — keep them alive!",
    "🎶 You make each other’s hearts sing.",
    "🌙 A love that shines bright at night.",
    "💌 You’re a love story in progress.",
    "🍫 Sweet and strong — just like chocolate.",
    "💕 Your love has the power to last forever.",
    "✨ A magical connection worth keeping.",
    "🌍 The world looks brighter when you’re together.",
    "🎉 There’s so much happiness in store for you!",
    "🌹 You two make a beautiful team.",
    "💡 A little effort makes this love unbreakable.",
    "💖 Happiness loves your company.",
    "🍯 Sweet, steady, and growing stronger.",
    "🔥 A spark that can become a flame.",
    "💕 You’re perfect for each other’s quirks.",
    "🎶 Like a melody and lyrics — complete together.",
    "🌙 Love that glows like starlight."
            ]
        elif love_percent >= 60:
            fun_messages = [
                "💫 There’s definitely something special here!",
    "🌹 A good match with room to grow.",
    "💕 Love is budding — nurture it well.",
    "🔥 The spark is there, let it shine brighter!",
    "🎶 You’re in sync more than you realize.",
    "🌍 You two could be a strong couple with time.",
    "💌 Patience makes the heart grow stronger.",
    "💕 With effort, this can be forever.",
    "🌙 You make each other smile — that’s love!",
    "✨ A promising connection worth exploring.",
    "🍫 Sweet beginnings often lead to true love.",
    "🔥 You’re almost in soulmate territory.",
    "🎉 Love is in progress — enjoy the journey!",
    "🌹 A little push could make this magical.",
    "💖 Something amazing is forming here.",
    "💡 Communication is your superpower.",
    "🌙 Your story is still being written.",
    "💕 Keep the spark alive — it’s worth it.",
    "🎶 Love grows when you share the rhythm.",
    "🌹 A beautiful start to something lasting."
            ]
        else:
            fun_messages = [
                "😂 Well… at least you’re friends, right?",
    "🌱 Every big tree starts as a small seed!",
    "💕 Maybe this love just needs a little fertilizer (aka effort).",
    "🎉 Hey, love is full of surprises!",
    "🔥 Slow flame, but it can still burn bright.",
    "🍫 Not super sweet yet… but who doesn’t like a challenge?",
    "💖 You’ve got potential — love isn’t always instant.",
    "🎶 Practice makes perfect — even in love!",
    "🌹 A little extra romance can change everything.",
    "💡 Love is 90% effort, 10% fate.",
    "😂 Well… you’d definitely win ‘Cutest Friends Award’.",
    "✨ Who says low numbers can’t lead to big feelings?",
    "💕 All love stories have to start somewhere.",
    "🌙 Sometimes it’s about the journey, not the score.",
    "🌍 Maybe destiny is still cooking this one.",
    "🎉 Love is unpredictable — keep going!",
    "🍦 Even ice cream melts slowly — be patient.",
    "💌 Not fireworks yet, but maybe a sparkler 🎇.",
    "🔥 Potential detected, needs more fuel.",
    "😂 At least you won’t fight over Netflix shows.",
    "🌹 Friendship first, love second — not a bad start!",
    "🎶 Harmony takes practice.",
    "💖 Low score, high possibilities.",
    "🌙 Love sometimes sneaks in when least expected.",
    "🍯 Needs more sweetness — try adding hugs!",
    "🎉 Every number is just a number… but love is magic.",
    "😂 Well, opposites attract, right?",
    "💕 A little effort could change the whole story.",
    "🔥 Not hot yet… but maybe simmering.",
    "🌹 Even small sparks can start a fire.",
    "💡 Focus on connection, not the score.",
    "🎶 Play the right tune and love might dance along.",
    "💖 You never know — today’s 40% could be tomorrow’s 100%.",
    "😂 The calculator might be broken… your heart knows better.",
    "🌍 Love can’t always be measured — give it time!"
            ]
        
        message = easter if easter else random.choice(fun_messages)

        # Heart balloons animation
        rain(emoji="💗", font_size=54, falling_speed=5, animation_length="infinite")
        rain(emoji="💖", font_size=38, falling_speed=7, animation_length="infinite")

        # MAIN RESULT DISPLAY (This will be captured in screenshot)
        st.markdown(
            f"""
            <div class="screenshot-area" id="result-box">
                <h2>💌 {name1} ❤️ {name2} 💌</h2>
                <p class="result-text">{love_percent}% ⭐</p>
                <div class="breakdown-grid">
                    <div class="breakdown-item">🔥 Romance<br><b>{breakdown["🔥 Romance Potential"]}/10</b></div>
                    <div class="breakdown-item">😂 Memes<br><b>{breakdown["😂 Meme Compatibility"]}/10</b></div>
                    <div class="breakdown-item">🎶 Music<br><b>{breakdown["🎶 Playlist Vibes"]}/10</b></div>
                    <div class="breakdown-item">💬 Texting<br><b>{breakdown["💬 Texting Energy"]}/10</b></div>
                    <div class="breakdown-item">📛 Names<br><b>{breakdown["📛 Name Harmony"]}/10</b></div>
                    <div class="breakdown-item">🎂 Age Match<br><b>{breakdown["🎂 Age Sync"]}/10</b></div>
                </div>
                <p class="sub-text" style="margin-top:18px;">{message}</p>
                <p class="sub-text"><b>{zodiac1}</b> ✨ + <b>{zodiac2}</b> = Cosmic Chemistry 🔮</p>
                <p style="color:#8a2a52;margin-top:10px;font-size:16px;">{quiz_note}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

       
        # CENTERED FORTUNE & TIPS SECTION
        add_vertical_space(2)
        
        # Create centered container for fortune and tips
        st.markdown('<div class="centered-section">', unsafe_allow_html=True)
        
        # Fortune section - centered
        st.markdown("### 🔮 Your Personalized Love Fortune")
        fortune = todays_fortune(name1, name2, love_percent)
        st.success(fortune)
        
        add_vertical_space(1)
        
        # Tips section - centered  
        st.markdown("### 💡 Relationship Tips Just For You")
        tips = get_relationship_tips(breakdown, love_percent)
        for i, tip in enumerate(tips, 1):
            st.info(f"**Tip {i}:** {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
add_vertical_space(3)
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #ff4da6, #ff007f); 
            border-radius: 15px; color: white; margin-top: 50px;">
    <h2>💖 Made with Love & Code</h2>
    <p>Share with your friends and spread the love! ✨</p>
    <p style="font-size: 12px; opacity: 0.8;"><b>
        Results are for entertainment purposes. Real relationships require communication, trust, and effort! 💕
    </b></p>
</div>
""", unsafe_allow_html=True)
