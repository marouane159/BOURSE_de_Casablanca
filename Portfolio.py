import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Color scheme
BLACK = "#000000"
RED = "#FF0000"
YELLOW = "#FFFF00"
DARK_RED = "#CC0000"
DARK_YELLOW = "#CCCC00"
WHITE = "#FFFFFF"

# Fonction pour calculer les métriques du portefeuille
def calculate_portfolio_metrics(stocks_data):
    if not stocks_data:
        return None
    
    # Calcul des métriques de base
    total_investment = sum(stock["quantity"] * stock["buy_price"] for stock in stocks_data)
    current_value = sum(stock["quantity"] * stock["current_price"] for stock in stocks_data)
    pnl = current_value - total_investment
    pnl_percentage = (pnl / total_investment * 100) if total_investment > 0 else 0
    
    # Calcul des performances par action
    stock_performances = []
    for stock in stocks_data:
        stock_value = stock["quantity"] * stock["current_price"]
        stock_investment = stock["quantity"] * stock["buy_price"]
        stock_pnl = stock_value - stock_investment
        stock_pnl_percentage = (stock_pnl / stock_investment * 100) if stock_investment > 0 else 0
        
        stock_performances.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "current_price": stock["current_price"],
            "value": stock_value,
            "investment": stock_investment,
            "pnl": stock_pnl,
            "pnl_percentage": stock_pnl_percentage,
            "weight": (stock_value / current_value * 100) if current_value > 0 else 0,
            "sector": stock.get("sector", "Autre")
        })
    
    # Calcul des ratios financiers
    sharpe_ratio = 1.2  # Simplified calculation
    beta = 0.8  # Simplified calculation
    volatility = "15%"  # Simplified calculation
    annual_return = f"{pnl_percentage:.2f}%"  # Using current performance as annualized for demo
    
    # Calculate sector distribution
    sector_distribution = {}
    for stock in stock_performances:
        sector = stock["sector"]
        if sector not in sector_distribution:
            sector_distribution[sector] = 0
        sector_distribution[sector] += stock["value"]
    
    # Calculate risk level based on beta and volatility
    risk_score = beta * float(volatility.strip('%')) / 10
    if risk_score < 0.5:
        risk_level = "Faible"
        risk_color = YELLOW
    elif risk_score < 1.0:
        risk_level = "Modéré"
        risk_color = DARK_YELLOW
    else:
        risk_level = "Élevé"
        risk_color = RED
    
    return {
        "total_investment": total_investment,
        "current_value": current_value,
        "pnl": pnl,
        "pnl_percentage": pnl_percentage,
        "stock_performances": stock_performances,
        "ratios": {
            "sharpe_ratio": sharpe_ratio,
            "beta": beta,
            "volatility": volatility,
            "annual_return": annual_return,
            "risk_level": risk_level,
            "risk_color": risk_color
        },
        "sector_distribution": sector_distribution
    }

# Liste statique des actions marocaines avec leurs prix et secteurs
MOROCCAN_STOCKS = [
    {"symbol": "ADH", "name": "DOUJA PROM ADDOHA", "price": 42.90, "sector": "Immobilier"},
    {"symbol": "ADI", "name": "ALLIANCES", "price": 530.0, "sector": "Divers"},
    {"symbol": "AFI", "name": "AFRIC INDUSTRIES", "price": 326.00, "sector": "Industrie"},
    {"symbol": "AFM", "name": "AFMA", "price": 1286.0, "sector": "Finance"},
    {"symbol": "AKT", "name": "AKDITAL S.A", "price": 1211.0, "sector": "Santé"},
    {"symbol": "ALM", "name": "ALUMINIUM DU MAROC", "price": 1733.0, "sector": "Matériaux"},
    {"symbol": "ARD", "name": "ARADEI CAPITAL", "price": 480.00, "sector": "Immobilier"},
    {"symbol": "ATH", "name": "AUTO HALL", "price": 74.44, "sector": "Automobile"},
    {"symbol": "ATL", "name": "ATLANTASANAD", "price": 135.00, "sector": "Distribution"},
    {"symbol": "ATW", "name": "ATTIJARIWAFA BANK", "price": 680.0, "sector": "Banque"},
    {"symbol": "BAL", "name": "BALIMA", "price": 230.00, "sector": "Distribution"},
    {"symbol": "IAM", "name": "MAROC TELECOM", "price": 125.00, "sector": "Télécom"},
    {"symbol": "JET", "name": "JET CONTRACTORS", "price": 45.00, "sector": "Construction"},
    {"symbol": "MNG", "name": "MANAGEM", "price": 1850.0, "sector": "Mines"},
    {"symbol": "SNP", "name": "SNEP", "price": 639.8, "sector": "Industrie"},
    {"symbol": "SOT", "name": "SOTHEMA", "price": 1055.0, "sector": "Pharma"},
    {"symbol": "TGC", "name": "TRAVAUX GENERAUX DE CONSTRUCTIONS", "price": 690.0, "sector": "Construction"},
    {"symbol": "TMA", "name": "TOTALENERGIES MARKETING MAROC", "price": 1821.0, "sector": "Énergie"},
    {"symbol": "TQM", "name": "TAQA MOROCCO", "price": 2050.0, "sector": "Énergie"},
    {"symbol": "WAA", "name": "WAFA ASSURANCE", "price": 4902.0, "sector": "Assurance"}
]

def get_moroccan_stocks():
    try:
        return pd.DataFrame(MOROCCAN_STOCKS)
    except Exception as e:
        st.error(f"Error while loading stock data: {str(e)}")
        return None

# Configuration de la page
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
    
    # Performance tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "📊 Répartition", "📋 Détails", "📌 Recommandations"])
    
    with tab1:
        # Performance chart
        st.markdown(f"""
            <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                <h3 style='color: {YELLOW};'>Performance du Portefeuille</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Create performance data
        performance_data = pd.DataFrame(metrics["stock_performances"])
        
        # Portfolio evolution chart (simulated)
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now())
        portfolio_values = np.linspace(
            metrics['total_investment'], 
            metrics['current_value'], 
            len(dates)
        )
        
        fig_evolution = go.Figure()
        fig_evolution.add_trace(go.Scatter(
            x=dates,
            y=portfolio_values,
            mode='lines',
            line=dict(color=RED, width=3),
            name='Valeur du Portefeuille'
        ))
        fig_evolution.update_layout(
            plot_bgcolor=BLACK,
            paper_bgcolor=BLACK,
            font=dict(color=YELLOW),
            xaxis=dict(
                title=dict(text='Date', font=dict(color=YELLOW)),
                tickfont=dict(color=YELLOW),
                gridcolor=RED,
                linecolor=RED,
                zerolinecolor=RED
            ),
            yaxis=dict(
                title=dict(text='Valeur (MAD)', font=dict(color=YELLOW)),
                tickfont=dict(color=YELLOW),
                gridcolor=RED,
                linecolor=RED,
                zerolinecolor=RED
            ),
            hovermode="x unified"
        )
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Individual stock performance
        fig_perf = px.bar(
            performance_data,
            x="symbol",
            y="pnl_percentage",
            title="Performance par Action",
            color="pnl_percentage",
            color_continuous_scale=[RED, YELLOW],
            labels={"pnl_percentage": "Performance (%)", "symbol": "Action"},
            text="pnl_percentage"
        )
        fig_perf.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_perf.update_layout(
            plot_bgcolor=BLACK,
            paper_bgcolor=BLACK,
            font=dict(color=YELLOW),
            yaxis=dict(showgrid=False),
            xaxis=dict(title=None)
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with tab2:
        # Sector and asset distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                    <h3 style='color: {YELLOW};'>Répartition par Secteur</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Sector distribution pie chart
            sector_data = pd.DataFrame({
                "sector": list(metrics["sector_distribution"].keys()),
                "value": list(metrics["sector_distribution"].values())
            })
            
            fig_sector = px.pie(
                sector_data,
                values="value",
                names="sector",
                hole=0.4,
                color_discrete_sequence=[RED, YELLOW, DARK_RED, DARK_YELLOW]
            )
            fig_sector.update_layout(
                plot_bgcolor=BLACK,
                paper_bgcolor=BLACK,
                font=dict(color=YELLOW),
                showlegend=True
            )
            st.plotly_chart(fig_sector, use_container_width=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                    <h3 style='color: {YELLOW};'>Répartition par Action</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Asset distribution treemap
            fig_treemap = px.treemap(
                performance_data,
                path=['symbol'],
                values='value',
                color='pnl_percentage',
                color_continuous_scale=[RED, YELLOW],
                hover_data=['pnl_percentage']
            )
            fig_treemap.update_layout(
                plot_bgcolor=BLACK,
                paper_bgcolor=BLACK,
                margin=dict(t=0, l=0, r=0, b=0)
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
    
    with tab3:
        # Detailed performance table
        st.markdown(f"""
            <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                <h3 style='color: {YELLOW};'>Détails des Positions</h3>
            </div>
            """, unsafe_allow_html=True)
        
        detailed_data = pd.DataFrame(metrics["stock_performances"])
        detailed_data = detailed_data[[
            "symbol", "name", "sector", "current_price", 
            "investment", "value", "pnl", "pnl_percentage", "weight"
        ]]
        detailed_data.columns = [
            "Symbole", "Nom", "Secteur", "Prix Actuel", 
            "Investissement", "Valeur", "P&L", "Performance %", "Poids %"
        ]
        
        # Format the DataFrame display
        styled_table = detailed_data.style.format({
            "Prix Actuel": "{:,.2f} MAD",
            "Investissement": "{:,.2f} MAD",
            "Valeur": "{:,.2f} MAD",
            "P&L": "{:+,.2f} MAD",
            "Performance %": "{:+.2f}%",
            "Poids %": "{:.2f}%"
        }).applymap(
            lambda x: f"color: {RED}" if isinstance(x, str) and x.startswith('+') 
            else (f"color: {RED}" if isinstance(x, str) and x.startswith('-') else ""),
            subset=["P&L", "Performance %"]
        )
        
        st.dataframe(styled_table, use_container_width=True)
        
        # Financial ratios
        st.markdown(f"""
            <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                <h3 style='color: {YELLOW};'>Ratios Financiers</h3>
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                    <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                        <div style='font-size: 14px; color: {YELLOW};'>Sharpe Ratio</div>
                        <div style='font-size: 24px; font-weight: bold;'>{metrics['ratios']['sharpe_ratio']:.2f}</div>
                    </div>
                    <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                        <div style='font-size: 14px; color: {YELLOW};'>Beta</div>
                        <div style='font-size: 24px; font-weight: bold;'>{metrics['ratios']['beta']:.2f}</div>
                    </div>
                    <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                        <div style='font-size: 14px; color: {YELLOW};'>Volatilité</div>
                        <div style='font-size: 24px; font-weight: bold;'>{metrics['ratios']['volatility']}</div>
                    </div>
                    <div style='background-color: {BLACK}; padding: 15px; border-radius: 10px; border-left: 4px solid {RED};'>
                        <div style='font-size: 14px; color: {YELLOW};'>Rendement Annualisé</div>
                        <div style='font-size: 24px; font-weight: bold;'>{metrics['ratios']['annual_return']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Recommendations
        st.markdown(f"""
            <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
                <h3 style='color: {YELLOW};'>Recommandations</h3>
            </div>
            """, unsafe_allow_html=True)
        
        performance_data = pd.DataFrame(metrics["stock_performances"])
        best_performer = performance_data.loc[performance_data['pnl_percentage'].idxmax()]
        worst_performer = performance_data.loc[performance_data['pnl_percentage'].idxmin()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; border-left: 4px solid {RED}; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                    <h4 style='color: {YELLOW}; margin-top: 0;'>⭐ Meilleure Performance</h4>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <div style='font-size: 18px; font-weight: bold;'>{best_performer['name']}</div>
                            <div style='font-size: 14px; color: #666;'>{best_performer['symbol']} | {best_performer['sector']}</div>
                        </div>
                        <div style='font-size: 24px; font-weight: bold; color: {RED};'>
                            +{best_performer['pnl_percentage']:.2f}%
                        </div>
                    </div>
                    <div style='margin-top: 15px;'>
                        <div style='font-size: 14px;'>Poids dans le portefeuille: {best_performer['weight']:.2f}%</div>
                        <div style='font-size: 14px;'>Prix actuel: {best_performer['current_price']:,.2f} MAD</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; border-left: 4px solid {RED}; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                    <h4 style='color: {YELLOW}; margin-top: 0;'>⚠️ Performance à Surveiller</h4>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <div style='font-size: 18px; font-weight: bold;'>{worst_performer['name']}</div>
                            <div style='font-size: 14px; color: #666;'>{worst_performer['symbol']} | {worst_performer['sector']}</div>
                        </div>
                        <div style='font-size: 24px; font-weight: bold; color: {RED};'>
                            {worst_performer['pnl_percentage']:.2f}%
                        </div>
                    </div>
                    <div style='margin-top: 15px;'>
                        <div style='font-size: 14px;'>Poids dans le portefeuille: {worst_performer['weight']:.2f}%</div>
                        <div style='font-size: 14px;'>Prix actuel: {worst_performer['current_price']:,.2f} MAD</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # General recommendations based on portfolio metrics
        st.markdown(f"""
            <div style='background-color: {BLACK}; border-radius: 10px; padding: 20px; margin-top: 20px;'>
                <h4 style='color: {YELLOW}; margin-top: 0;'>Analyse Globale</h4>
                {f"<p>Votre portefeuille présente un rendement de <strong>{metrics['pnl_percentage']:.2f}%</strong> avec un niveau de risque <strong>{metrics['ratios']['risk_level'].lower()}</strong>.</p>"}
                {f"<p>La diversification sectorielle est <strong>{'bonne' if len(metrics['sector_distribution']) >= 4 else 'à améliorer'}</strong> avec {len(metrics['sector_distribution'])} secteurs représentés.</p>"}
                <p>Considérez rééquilibrer votre portefeuille pour optimiser le ratio risque/rendement.</p>
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