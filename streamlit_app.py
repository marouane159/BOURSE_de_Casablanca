import streamlit as st
import sys
import os
import pandas as pd

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from Portfolio import (
    calculate_portfolio_metrics,
    get_moroccan_stocks,
    MOROCCAN_STOCKS,
    BLACK,
    RED,
    YELLOW,
    DARK_RED,
    DARK_YELLOW,
    WHITE
)

# Set page configuration
st.set_page_config(
    page_title="Portfolio Risk.MA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the new design
st.markdown(f"""
    <style>
    /* Main background */
    .main {{
        background-color: {BLACK};
    }}
    .stApp {{
        background-color: {BLACK};
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {YELLOW};
    }}
    
    /* Sidebar */
    .css-1lcbmhc {{
        background-color: {BLACK};
        color: {YELLOW};
        border: 2px solid {RED};
    }}
    .css-1lcbmhc h1, .css-1lcbmhc h2, .css-1lcbmhc h3 {{
        color: {YELLOW};
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {RED};
        color: {BLACK};
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {DARK_RED};
        color: {BLACK};
    }}
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: {BLACK};
        border: 1px solid {RED};
        color: {YELLOW};
    }}
    
    /* Metrics */
    .stMetric {{
        background-color: {BLACK};
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(255,0,0,0.2);
        border: 1px solid {RED};
    }}
    
    /* Cards */
    .card {{
        background-color: {BLACK};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(255,0,0,0.2);
        border: 1px solid {RED};
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {BLACK};
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        border: 1px solid {RED};
        color: {YELLOW};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {RED};
        color: {BLACK};
    }}
    
    /* Tables */
    .dataframe {{
        background-color: {BLACK};
        color: {YELLOW};
    }}
    </style>
    """, unsafe_allow_html=True)

# Header with logo and title
st.markdown(f"""
    <div style='background-color: {BLACK}; color: {YELLOW}; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid {RED};'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <h1 style='margin: 0; color: {YELLOW};'>Portfolio Risk.MA</h1>
                <p style='margin: 0;'>Tableau de bord d'investissement - Bourse de Casablanca</p>
            </div>
            <div style='display: flex; align-items: center; gap: 15px;'>
                <div style='background-color: {RED}; padding: 5px 10px; border-radius: 5px; color: {BLACK}; font-weight: bold;'>
                    <a href='https://risk.ma/bourse-de-casablanca' target='_blank' style='color: {BLACK}; text-decoration: none;'>www.risk.ma</a>
                </div>
                <div style='display: flex; gap: 10px;'>
                    <a href='https://instagram.com/risk.maroc' target='_blank' style='color: {YELLOW}; text-decoration: none;'>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" fill="{YELLOW}"/>
                        </svg>
                    </a>
                    <a href='https://tiktok.com/@risk.maroc' target='_blank' style='color: {YELLOW}; text-decoration: none;'>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" fill="{YELLOW}"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for data input
with st.sidebar:
    st.markdown(f"""
        <div style='background-color: {BLACK}; color: {YELLOW}; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid {RED};'>
            <h3 style='color: {YELLOW}; margin: 0;'>Configuration du Portefeuille</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Refresh button
    if st.button("🔄 Actualiser les cours", key="refresh_button"):
        with st.spinner("Chargement des données..."):
            stocks_df = get_moroccan_stocks()
            if stocks_df is not None and not stocks_df.empty:
                st.session_state.stocks_df = stocks_df
                st.success(f"Données chargées avec succès! {len(stocks_df)} actions disponibles.")
            else:
                st.error("Impossible de charger les données des actions.")
    
    # Initialize session state if not already done
    if 'stocks_df' not in st.session_state:
        st.session_state.stocks_df = pd.DataFrame(MOROCCAN_STOCKS)
    
    # Portfolio configuration
    st.markdown("#### Composition du Portefeuille")
    num_stocks = st.number_input("Nombre d'actions", min_value=1, max_value=20, value=1, step=1)
    
    stocks_data = []
    for i in range(num_stocks):
        st.markdown(f"**Action {i+1}**")
        
        # Stock selection
        stock_options = st.session_state.stocks_df.apply(
            lambda x: f"{x['symbol']} - {x['name']}", 
            axis=1
        ).tolist()
        
        selected_stock = st.selectbox(
            f"Sélectionnez l'action {i+1}",
            options=stock_options,
            key=f"stock_{i}"
        )
        
        # Extract stock info
        symbol = selected_stock.split(' - ')[0]
        stock_info = st.session_state.stocks_df[
            st.session_state.stocks_df['symbol'] == symbol
        ].iloc[0]
        
        # Quantity input
        quantity = st.number_input(
            "Quantité",
            min_value=1,
            value=1,
            key=f"quantity_{i}"
        )
        
        # Buy price input
        buy_price = st.number_input(
            "Prix d'achat (MAD)",
            min_value=0.0,
            value=float(stock_info['price']),
            key=f"buy_price_{i}"
        )
        
        # Display current price
        st.info(f"Prix actuel: {stock_info['price']} MAD | Secteur: {stock_info['sector']}")
        
        stocks_data.append({
            "symbol": symbol,
            "name": stock_info['name'],
            "quantity": quantity,
            "buy_price": buy_price,
            "current_price": stock_info['price'],
            "sector": stock_info['sector']
        })
    
    # Calculate portfolio button
    if st.button("📊 Analyser le Portefeuille", key="calculate_portfolio"):
        if not stocks_data:
            st.error("Veuillez ajouter au moins une action à votre portefeuille.")
        else:
            st.session_state.portfolio_metrics = calculate_portfolio_metrics(stocks_data)

# Main content area
if 'portfolio_metrics' in st.session_state:
    metrics = st.session_state.portfolio_metrics
    
    # Portfolio summary cards
    st.markdown(f"""
        <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(255,0,0,0.2);'>
            <h2 style='color: {YELLOW}; margin-top: 0;'>Résumé du Portefeuille</h2>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                    <div style='font-size: 14px; color: {YELLOW};'>Investissement Total</div>
                    <div style='font-size: 24px; font-weight: bold;'>{metrics['total_investment']:,.2f} MAD</div>
                </div>
                <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                    <div style='font-size: 14px; color: {YELLOW};'>Valeur Actuelle</div>
                    <div style='font-size: 24px; font-weight: bold;'>{metrics['current_value']:,.2f} MAD</div>
                </div>
                <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                    <div style='font-size: 14px; color: {YELLOW};'>Profit & Loss</div>
                    <div style='font-size: 24px; font-weight: bold; color: {RED};'>
                        {metrics['pnl']:,.2f} MAD ({metrics['pnl_percentage']:.2f}%)
                    </div>
                </div>
                <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                    <div style='font-size: 14px; color: {YELLOW};'>Niveau de Risque</div>
                    <div style='font-size: 24px; font-weight: bold; color: {RED};'>
                        {metrics['ratios']['risk_level']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style='background-color: {BLACK}; color: {YELLOW}; padding: 15px; border-radius: 10px; margin-top: 30px; text-align: center; border: 2px solid {RED};'>
        <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;'>
            <a href='https://risk.ma/bourse-de-casablanca' target='_blank' style='color: {YELLOW}; text-decoration: none;'>www.risk.ma</a>
            <a href='https://instagram.com/risk.maroc' target='_blank' style='color: {YELLOW}; text-decoration: none;'>Instagram</a>
            <a href='https://tiktok.com/@risk.maroc' target='_blank' style='color: {YELLOW}; text-decoration: none;'>TikTok</a>
        </div>
        <p style='margin: 0;'>© 2025 @risk.maroc - Plateforme d'analyse financière pour la Bourse de Casablanca</p>
        <p style='margin: 0; font-size: 12px;'>@dogofallstreets | @risk.maroc | www.risk.ma</p>
    </div>
    """, unsafe_allow_html=True) 
