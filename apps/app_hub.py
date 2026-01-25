import streamlit as st
import math

BANNER_URL = "assets/corvigil_banner.jepg"  # or "https://your-image-url.com/banner.png"

APP_DIRECTORY = [
    {
        "title": "Cardiac Risk Assessment",
        "description": "Comprehensive screening tool analyzing vitals and lifestyle factors to predict general cardiac risk.",
        "icon": "",
        "url": "https://anice-tools-cardiac-report.streamlit.app/",
        "button_text": "Launch Assessment",
        "theme_color": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "image_url": 'assets/cardiac_problem.jpg',
    },
    {
        "title": "Heart Attack Predictor",
        "description": "Advanced AI model focused specifically on detecting immediate myocardial infarction probability.",
        "icon": "",
        "url": "https://anice-tools-heart-attack-predict.streamlit.app/",
        "button_text": "Check Risk",
        "theme_color": "linear-gradient(135deg, #FF6B9D 0%, #C9184A 100%)",
        "image_url": 'assets/heart_attack.jpg'
    },
    {
        "title": "ECG Analysis Tool",
        "description": "Upload and analyze ECG waveforms for arrhythmia detection (Coming Soon).",
        "icon": "",
        "url": "#",
        "button_text": "Coming Soon",
        "theme_color": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
        "image_url": None
    },
]

# -----------------------------------------------------------------------------
# 2. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CorVigil Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 3. CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
    }

    /* Remove default top padding so banner sits flush */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }

    /* Banner Styling */
    .banner-container {
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .banner-img {
        width: 100%;
        height: auto;
        display: block;
    }

    /* Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #2c3e50, #4ca1af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 4rem;
    }

    div[data-testid="column"] {
        background: transparent;
    }

    /* Card Styling */
    .app-card {
        background: white;
        border-radius: 20px;
        padding: 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .app-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        border-color: #dee2e6;
    }

    .card-thumbnail {
        height: 160px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: white;
        position: relative;
    }

    .thumbnail-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .card-content {
        padding: 1.5rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #212529;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .card-desc {
        color: #6c757d;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
        flex-grow: 1;
    }

    .stLinkButton > a {
        display: block;
        width: 100%;
        text-align: center;
        border-radius: 10px;
        font-weight: 600;
        background: white;
        border: 2px solid #e9ecef;
        color: #495057;
        transition: all 0.2s;
    }

    .stLinkButton > a:hover {
        background: #f8f9fa;
        border-color: #ced4da;
        color: #212529;
    }

    .footer {
        text-align: center;
        padding: 4rem 0 2rem 0;
        color: #adb5bd;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. MAIN LAYOUT LOGIC
# -----------------------------------------------------------------------------
def main():
    # --- BANNER SECTION ---
    # We display the image if the variable is set
    if BANNER_URL:
        try:
            st.image(BANNER_URL, use_container_width=True)
        except:
            # Fallback if image not found (just to prevent crash)
            st.warning(f"Banner image not found at: {BANNER_URL}")

    # Header
    st.markdown('<div class="main-header">CorVigil Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Centralized Cardiovascular Health Intelligence Platform</div>',
                unsafe_allow_html=True)

    # Grid System
    COLS_PER_ROW = 3
    total_apps = len(APP_DIRECTORY)
    rows = math.ceil(total_apps / COLS_PER_ROW)

    for row in range(rows):
        cols = st.columns(COLS_PER_ROW, gap="large")

        for i in range(COLS_PER_ROW):
            app_index = row * COLS_PER_ROW + i

            if app_index < total_apps:
                app = APP_DIRECTORY[app_index]

                with cols[i]:
                    if app.get("image_url"):
                        thumb_html = f'<img src="{app["image_url"]}" class="thumbnail-img">'
                    else:
                        thumb_html = f'{app["icon"]}'

                    st.markdown(f"""
                    <div class="app-card">
                        <div class="card-thumbnail" style="background: {app['theme_color']}">
                            {thumb_html}
                        </div>
                        <div class="card-content">
                            <div class="card-title">{app['title']}</div>
                            <div class="card-desc">{app['description']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.link_button(
                        label=app["button_text"],
                        url=app["url"],
                        use_container_width=True
                    )
            else:
                with cols[i]:
                    st.write("")

    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="footer">© 2024 CorVigil Health Systems • <a href="#" style="color:#adb5bd;">Documentation</a> • <a href="#" style="color:#adb5bd;">Support</a></div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()