import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os
import io

# ==========================================
# 1. INITIAL SETUP
# ==========================================
st.set_page_config(page_title="Color Metamerism Viewer", layout="wide", initial_sidebar_state="collapsed")

if 'app_state' not in st.session_state:
    st.session_state.app_state = 'splash'
if 'file_bytes' not in st.session_state:
    st.session_state.file_bytes = None
if 'upload_key' not in st.session_state:
    st.session_state.upload_key = 0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_of_bin_file(filename):
    filepath = os.path.join(SCRIPT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

def get_text_file(filename):
    filepath = os.path.join(SCRIPT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            svg_content = f.read()
            return svg_content.replace('<svg ', '<svg style="width: 100%; height: auto;" ')
    return ""

# Load Assets
font_medium_b64 = get_base64_of_bin_file("NeueHaasDisplayMediu.ttf") 
bg_b64 = get_base64_of_bin_file("Background python app.jpg")
icon_files = ["Calculator Icon.txt", "Bulb Icon.txt", "Coms Icon.txt", "Graph1 Icon.txt", "Graph2 Icon.txt", "Graph3 Icon.txt"]

# ==========================================
# 2. GLOBAL FONT LOADER & ICON SHIELD
# ==========================================
if font_medium_b64:
    st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'NeueHaas';
        src: url(data:font/truetype;base64,{font_medium_b64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}

    /* Apply Medium font to absolutely everything */
    html, body, p, span, div, h1, h2, h3, h4, h5, h6,
    .stApp, .stButton, .stSelectbox, .stMarkdown, 
    .stExpander, .stSlider, .stTextInput, .stMultiSelect,
    .stMetric, .stRadio, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        font-family: 'NeueHaas', sans-serif !important;
        font-weight: normal !important;
    }}

    /* PROTECT STREAMLIT ICONS (Fixes the broken menu labels) */
    .material-symbols-rounded, 
    .material-symbols-outlined, 
    .material-icons, 
    [data-testid="stIconMaterial"] {{
        font-family: "Material Symbols Rounded", "Material Icons" !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 3. PAGE 1: THE SPLASH SCREEN
# ==========================================
if st.session_state.app_state == 'splash':
    
    if bg_b64:
        bg_css = f"background-image: url(data:image/jpeg;base64,{bg_b64});background-size: cover; background-position: center 41%;"
    else:
        bg_css = "background-color: #1a1a1a;"

    st.markdown(f"""
        <style>
        /* Hide Headers */
        header, [data-testid="stHeader"] {{ display: none !important; }}
        [data-testid="stToolbar"] {{ display: none !important; }}
        .splash-container .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        
        /* Main Container */
        .splash-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            {bg_css}
            z-index: 1;
            text-align: center;
            pointer-events: none !important; 
        }}
        
        .title-wrapper {{
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-top: 30px;
            margin-bottom: 5px;
        }}
        
        /* ICON CAROUSEL SETTINGS */
        .splash-container .icon-wrapper {{
            position: absolute;
            width: 147px;
            left: 995px;
            top: -0px;
            margin-top: 0px;
        }}
        
        .splash-container .icon-item {{
            position: absolute;
            width: 100%;
            opacity: 0;
            animation: cycle 4.2s infinite;
        }}
        
        /* Icon Timing (4.2s Total Cycle) */
        .splash-container .icon-item:nth-child(4) {{ animation-delay: 0.7s; }}
        .splash-container .icon-item:nth-child(1) {{ animation-delay: 1.4s; }}
        .splash-container .icon-item:nth-child(6) {{ animation-delay: 2.1s; }}
        .splash-container .icon-item:nth-child(3) {{ animation-delay: 2.8s; }}
        .splash-container .icon-item:nth-child(5) {{ animation-delay: 3.5s; }}
        .splash-container .icon-item:nth-child(2) {{ animation-delay: 4.2s; }}

        @keyframes cycle {{
            0%, 16.66% {{ opacity: 1; }}
            16.67%, 100% {{ opacity: 0; }}
        }}

        /* Splash Text Styling */
        h1.splash-title, .stMarkdown h1.splash-title {{
            font-size: 7.5rem !important; 
            color: #FFFFFF; 
            margin: 0; 
            font-family: 'NeueHaas', sans-serif !important;
            font-weight: normal !important; 
            letter-spacing: 0px;
            white-space: pre-wrap;
        }}
        
        .splash-container .splash-subtitle {{
            font-size: 1rem;
            color: #FFFFFF;
            margin-top: -180px !important;
            margin-bottom: 450px;
            font-weight: 300;
            opacity: 0.70;
        }}

        /* Invisible File Hitbox */
        div:has(> [data-testid="stFileUploader"]) {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 99999 !important;
            opacity: 0.001 !important; 
        }}
        
        [data-testid="stFileUploader"], [data-testid="stFileUploadDropzone"] {{
            position: absolute !important;
            top: 0 !important; left: 0 !important;
            width: 100% !important; height: 100% !important;
            z-index: 99999 !important; border: none !important;
            padding: 0 !important; margin: 0 !important;
        }}
        
        [data-testid="stFileUploader"] label {{ display: none !important; }}
        [data-testid="stFileUploader"] * {{ cursor: pointer !important; width: 100% !important; height: 100% !important; }}
        </style>
    """, unsafe_allow_html=True)

    icons_html = "".join([f'<div class="icon-item">{get_text_file(f)}</div>' for f in icon_files])
    
    st.markdown(f"""
    <div class="splash-container">
        <p class="splash-subtitle">Click anywhere or drag an Excel file to begin</p>
        <div class="title-wrapper">
            <div class="icon-wrapper">{icons_html}</div>
            <h1 class="splash-title">see your color with         .</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload", 
        type=['xlsx', 'xls'], 
        key=f"splash_uploader_{st.session_state.upload_key}"
    )
    
    if uploaded_file is not None:
        st.session_state.file_bytes = uploaded_file.getvalue()
        st.session_state.app_state = 'graph'
        st.rerun()


# ==========================================
# 4. PAGE 2: THE GRAPHING INTERFACE
# ==========================================
elif st.session_state.app_state == 'graph':
    
    st.markdown("""
        <style>
        .block-container { padding-top: 3rem !important; }
        </style>
    """, unsafe_allow_html=True)

    col_back, col_space = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Back to Upload"):
            st.session_state.app_state = 'splash'
            st.session_state.file_bytes = None
            st.session_state.upload_key += 1 
            st.rerun()

    st.markdown("""
        <div style="font-family: 'NeueHaas', sans-serif !important; font-weight: normal !important; font-size: 2.5rem; padding-bottom: 15px; -webkit-font-smoothing: antialiased;">
            Color Reflectance Data Viewer
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    try:
        xls = pd.ExcelFile(io.BytesIO(st.session_state.file_bytes))
        
        ref_sheet_name = next((sheet for sheet in xls.sheet_names if "reference lighting" in sheet.lower()), None)
        color_sheets = [sheet for sheet in xls.sheet_names if "reference lighting" not in sheet.lower()]
        
        if not color_sheets:
            st.error("No valid color tabs found in the uploaded file.")
        else:
            selected_color = st.selectbox("Color Name:", color_sheets)
            df_color = pd.read_excel(xls, sheet_name=selected_color)
            
            # --- DYNAMICALLY FIND NORMALIZED COLUMNS ---
            normalized_cols = [col for col in df_color.columns if "normalized" in str(col).lower()]
            
            df_ref = None
            ref_options = []
            if ref_sheet_name:
                df_ref = pd.read_excel(xls, sheet_name=ref_sheet_name)
                ref_x_col = df_ref.columns[0]
                ref_options = df_ref.columns[1:].tolist()

            # --- STREAMLIT TOGGLES ---
            selected_refs = []
            if ref_options:
                st.markdown("### Reference Lighting Overlays")
                cols = st.columns(len(ref_options))
                for i, ref_name in enumerate(ref_options):
                    with cols[i]:
                        if st.toggle(ref_name):
                            selected_refs.append(ref_name)
            
            with st.expander("⚙️ Graph Settings"):
                st.markdown("#### Line Colors")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Color Data Series**")
                    data_color_picks = {}
                    default_data_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
                    
                    if normalized_cols:
                        for i, col_name in enumerate(normalized_cols):
                            default_hex = default_data_colors[i % len(default_data_colors)]
                            data_color_picks[col_name] = st.color_picker(col_name, default_hex)
                    else:
                        st.info("No 'Normalized' columns found to configure.")
                        
                with col2:
                    st.markdown("**Reference Lighting Series**")
                    light_color_picks = {}
                    default_light_colors = ['#2ca02c', '#d62728', '#9467bd', '#8c564b']
                    if ref_options:
                        for i, ref_name in enumerate(ref_options):
                            default_hex = default_light_colors[i % len(default_light_colors)]
                            light_color_picks[ref_name] = st.color_picker(ref_name, default_hex)
                
                st.divider()
                
                # --- SPLIT TRUNCATE TOGGLES ---
                st.markdown("#### View Options")
                truncate_color_bounds = st.toggle("Truncate Color Wavelength Bounds (400nm - 700nm)", value=True)
                truncate_lighting_bounds = st.toggle("Truncate Lighting Wavelength Bounds (400nm - 700nm)", value=True)
                
                st.divider()
                
                st.markdown("#### Image Export")
                st.markdown("*Adjust these dimensions, then hover over the graph and click the **Camera Icon** to download.*")
                img_col1, img_col2, img_col3 = st.columns(3)
                with img_col1:
                    export_width = st.number_input("Width (px)", min_value=500, value=1920, step=100)
                with img_col2:
                    export_height = st.number_input("Height (px)", min_value=300, value=1080, step=100)
                with img_col3:
                    export_scale = st.number_input("Resolution Scale", min_value=1.0, value=2.0, step=0.5)

            if 'WL (nm)' in df_color.columns and len(normalized_cols) > 0:
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                # --- DATA SERIES GRAPHING WITH INDEPENDENT TRUNCATION LOGIC ---
                for col_name in normalized_cols:
                    if truncate_color_bounds:
                        mask = (df_color['WL (nm)'] >= 400) & (df_color['WL (nm)'] <= 700)
                        plot_x = df_color.loc[mask, 'WL (nm)']
                        plot_y = df_color.loc[mask, col_name]
                    else:
                        plot_x = df_color['WL (nm)']
                        plot_y = df_color[col_name]
                        
                    fig.add_trace(go.Scatter(
                        x=plot_x, y=plot_y, 
                        mode='lines', name=col_name, line=dict(width=2, color=data_color_picks[col_name])
                    ), secondary_y=False)
                
                # --- LIGHTING OVERLAYS GRAPHING WITH INDEPENDENT TRUNCATION LOGIC ---
                if selected_refs and df_ref is not None:
                    for ref in selected_refs:
                        if truncate_lighting_bounds:
                            ref_mask = (df_ref[ref_x_col] >= 400) & (df_ref[ref_x_col] <= 700)
                            plot_x_ref = df_ref.loc[ref_mask, ref_x_col]
                            plot_y_ref = df_ref.loc[ref_mask, ref]
                        else:
                            plot_x_ref = df_ref[ref_x_col]
                            plot_y_ref = df_ref[ref]
                            
                        fig.add_trace(go.Scatter(
                            x=plot_x_ref, y=plot_y_ref, 
                            mode='lines', name=f"💡 {ref}",
                            line=dict(width=2, dash='dash', color=light_color_picks[ref]), hoverinfo='x+y+name'
                        ), secondary_y=True)
                
                fig.update_layout(
                    title=f"Normalized Reflectance Data: {selected_color}",
                    xaxis_title="Wavelength (nm)",
                    hovermode="x unified",
                    template="plotly_white",
                    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                    margin=dict(l=40, r=40, t=80, b=40),
                    uirevision=selected_color
                )
                
                # --- EXPLICIT AXIS RANGE OVERRIDE ---
                # Locks the X-axis to the original data bounds so it doesn't auto-zoom when truncated
                if truncate_color_bounds or truncate_lighting_bounds:
                    x_min = df_color['WL (nm)'].min()
                    x_max = df_color['WL (nm)'].max()
                    fig.update_xaxes(range=[x_min, x_max])
                
                fig.update_yaxes(title_text="Reflectance/Transmittance", secondary_y=False)
                
                plot_config = {
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f"{selected_color}_Reflectance_Graph",
                        'height': export_height,
                        'width': export_width,
                        'scale': export_scale
                    }
                }
                
                st.plotly_chart(fig, use_container_width=True, config=plot_config)
                
            else:
                st.error(f"The tab '{selected_color}' is missing 'WL (nm)' or 'Normalized' columns.")

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
