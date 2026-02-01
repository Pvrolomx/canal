# 🔭 WEAK SIGNALS - SPEC v1.0
## 5 Sistemas de Detección Temprana de Eventos

---

> **Versión:** 1.0  
> **Fecha:** 31 Enero 2026  
> **Autor:** CD12 + Humano  
> **Estado:** SPEC COMPLETO - Pendiente implementación

---

## TABLA DE CONTENIDOS

1. [Visión General](#1-visión-general)
2. [Arquitectura Común](#2-arquitectura-común)
3. [SISTEMA 1: CORPORATE DECAY](#3-sistema-1-corporate-decay)
4. [SISTEMA 2: SUPPLY SHOCK](#4-sistema-2-supply-shock)
5. [SISTEMA 3: BANK STRESS](#5-sistema-3-bank-stress)
6. [SISTEMA 4: REAL ESTATE TREMOR](#6-sistema-4-real-estate-tremor)
7. [SISTEMA 5: GEOTENSION](#7-sistema-5-geotension)
8. [APIs y Fuentes de Datos](#8-apis-y-fuentes-de-datos)
9. [Implementación](#9-implementación)
10. [Backtest y Validación](#10-backtest-y-validación)

---

## 1. VISIÓN GENERAL

### 1.1 Concepto Core

> **"Los eventos importantes nunca llegan sin avisar. Los avisos están escondidos a plena vista."**

Sistema de monitoreo automatizado que detecta **señales débiles** en datos públicos para anticipar eventos significativos antes de que sean noticia mainstream.

### 1.2 Los 5 Sistemas

| Sistema | Codename | Detecta | Anticipación | Frecuencia |
|---------|----------|---------|--------------|------------|
| 1 | **CORPORATE DECAY** | Quiebras corporativas | 30-90 días | Diario |
| 2 | **SUPPLY SHOCK** | Disrupciones supply chain | 2-4 semanas | Cada 6h |
| 3 | **BANK STRESS** | Crisis bancarias | 24-72 horas | Cada hora |
| 4 | **REAL ESTATE TREMOR** | Corrección inmobiliaria | 2-6 meses | Semanal |
| 5 | **GEOTENSION** | Escalada geopolítica | 24-72 horas | Cada hora |

### 1.3 Principios de Diseño

1. **Solo datos públicos** - APIs gratuitas, sin información privilegiada
2. **Automatizable** - Cron jobs, sin intervención manual
3. **Accionable** - Cada alerta tiene acciones concretas asociadas
4. **Backtesteable** - Verificable contra eventos históricos
5. **Modular** - Cada sistema funciona independiente

### 1.4 Sistema de Scoring Universal

Todos los sistemas usan score normalizado **0-100**:

| Score | Nivel | Color | Acción |
|-------|-------|-------|--------|
| 0-25 | NORMAL | 🟢 | Sin acción |
| 26-50 | ATENCIÓN | 🟡 | Monitorear más frecuente |
| 51-75 | ALERTA | 🟠 | Preparar posiciones |
| 76-100 | CRÍTICO | 🔴 | Actuar inmediatamente |

---

## 2. ARQUITECTURA COMÚN

### 2.1 Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA                           │
├─────────────────────────────────────────────────────────────┤
│  FRONTEND         │  BACKEND         │  ALERTAS            │
│  ─────────────    │  ─────────────   │  ─────────────      │
│  • HTML/JS/CSS    │  • Python 3.11+  │  • Telegram Bot     │
│  • Chart.js       │  • FastAPI       │  • Email (SMTP)     │
│  • TailwindCSS    │  • SQLite        │  • Webhook          │
│                   │  • Schedule      │                      │
├─────────────────────────────────────────────────────────────┤
│                      DATA LAYER                             │
│  ─────────────────────────────────────────────────────────  │
│  • yfinance (precios)      • pytrends (Google Trends)      │
│  • fredapi (FRED)          • GDELT API (noticias)          │
│  • finnhub (insider)       • requests (scraping)           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Estructura de Directorios

```
weak-signals/
├── config/
│   ├── settings.py          # Configuración global
│   └── alerts.py             # Sistema de alertas
├── systems/
│   ├── corporate_decay.py    # Sistema 1
│   ├── supply_shock.py       # Sistema 2
│   ├── bank_stress.py        # Sistema 3
│   ├── real_estate.py        # Sistema 4
│   └── geotension.py         # Sistema 5
├── utils/
│   ├── data_fetcher.py       # Funciones de fetch
│   └── scoring.py            # Sistema de scoring
├── data/
│   └── historical/           # Backtest data
├── frontend/
│   └── index.html            # Dashboard
├── requirements.txt
└── run_all.py
```

### 2.3 Flujo de Datos

```
[APIs Externas] → [Fetcher] → [Normalizer] → [Scorer] → [Alerter]
      ↓                                           ↓
   Datos raw                                  Score 0-100
   (precio, %)                                    ↓
                                          [Dashboard + Log]
```

### 2.4 Cron Jobs Sugeridos

```cron
# BANK STRESS - cada hora (crítico)
0 * * * * python -m systems.bank_stress

# GEOTENSION - cada hora
30 * * * * python -m systems.geotension

# SUPPLY SHOCK - cada 6 horas
0 */6 * * * python -m systems.supply_shock

# CORPORATE DECAY - diario 7am
0 7 * * * python -m systems.corporate_decay

# REAL ESTATE - lunes 8am
0 8 * * 1 python -m systems.real_estate
```

---

## 3. SISTEMA 1: CORPORATE DECAY

### 3.1 Descripción

Detecta empresas públicas en espiral hacia quiebra/Chapter 11 **30-90 días antes** del evento.

**Hipótesis:** Las empresas mueren lentamente en público. Antes de que sea noticia:
- Empleados se quejan (Glassdoor)
- Insiders venden (SEC Form 4)
- Job postings desaparecen
- Tráfico web cae
- Short interest explota

### 3.2 Casos de Validación Histórica

| Empresa | Fecha Evento | Señales Visibles | Anticipación |
|---------|-------------|------------------|--------------|
| Bed Bath & Beyond | Abr 2023 | Glassdoor ↓, Jobs -80%, Insiders vendiendo | 90 días |
| WeWork | Nov 2023 | Reviews "sinking ship", CFO salió | 60 días |
| SVB | Mar 2023 | Glassdoor chaos +300%, Blind posts | 45 días |

### 3.3 Señales y Pesos

| ID | Señal | Fuente | Peso | Threshold Crítico |
|----|-------|--------|------|-------------------|
| D1 | **Precio 3M** | Yahoo Finance | 20% | Caída >50% |
| D2 | **Distancia 52W High** | Yahoo Finance | 15% | >70% abajo |
| D3 | **Insider Selling** | Finnhub/SEC | 20% | Ratio sell/buy >5:1 |
| D4 | **Short Interest** | FINRA | 15% | >25% del float |
| D5 | **Google "[ticker] bankruptcy"** | pytrends | 15% | Spike >3x |
| D6 | **Volumen anómalo** | Yahoo Finance | 10% | >3x promedio |
| D7 | **Volatilidad** | Yahoo Finance | 5% | >100% anualizada |

### 3.4 Fórmula de Scoring

```python
def score_corporate_decay(ticker):
    signals = {}
    
    # D1: Precio 3M
    change_3m = get_price_change(ticker, days=66)
    if change_3m <= -60: signals['D1'] = 20
    elif change_3m <= -40: signals['D1'] = 15
    elif change_3m <= -20: signals['D1'] = 8
    else: signals['D1'] = 0
    
    # D2: Distancia desde máximo
    pct_from_high = get_pct_from_52w_high(ticker)
    if pct_from_high <= -80: signals['D2'] = 15
    elif pct_from_high <= -60: signals['D2'] = 10
    elif pct_from_high <= -40: signals['D2'] = 5
    else: signals['D2'] = 0
    
    # D3: Insider selling
    sells, buys = get_insider_trades(ticker, days=90)
    ratio = sells / max(buys, 1)
    if ratio >= 5: signals['D3'] = 20
    elif ratio >= 3: signals['D3'] = 12
    elif ratio >= 2: signals['D3'] = 6
    else: signals['D3'] = 0
    
    # D4: Short interest
    short_pct = get_short_interest(ticker)
    if short_pct >= 30: signals['D4'] = 15
    elif short_pct >= 20: signals['D4'] = 10
    elif short_pct >= 10: signals['D4'] = 5
    else: signals['D4'] = 0
    
    # D5: Google Trends
    spike = get_google_spike(f"{ticker} bankruptcy")
    if spike >= 5: signals['D5'] = 15
    elif spike >= 3: signals['D5'] = 10
    elif spike >= 2: signals['D5'] = 5
    else: signals['D5'] = 0
    
    # D6: Volumen
    vol_ratio = get_volume_anomaly(ticker)
    if vol_ratio >= 5: signals['D6'] = 10
    elif vol_ratio >= 3: signals['D6'] = 6
    else: signals['D6'] = 0
    
    # D7: Volatilidad
    volatility = get_volatility(ticker)
    if volatility >= 150: signals['D7'] = 5
    elif volatility >= 100: signals['D7'] = 3
    else: signals['D7'] = 0
    
    return sum(signals.values())  # Max 100
```

### 3.5 Watchlist Sugerida

```python
CORPORATE_DECAY_WATCHLIST = [
    # Retail distressed
    "GME", "AMC", "BBBY", "M", "KSS",
    # Tech unprofitable
    "SNAP", "LYFT", "PTON", "W", "WISH",
    # SPACs post-merger
    "LCID", "RIVN", "NKLA", "QS",
    # High debt
    "T", "VZ", "DIS",
]
```

### 3.6 Acciones Cuando Dispara

| Score | Acción |
|-------|--------|
| 50-75 | Revisar posiciones, preparar exit |
| 76-100 | **SALIR INMEDIATAMENTE**, considerar puts |

---

## 4. SISTEMA 2: SUPPLY SHOCK

### 4.1 Descripción

Detecta disrupciones de supply chain y escasez de commodities **2-4 semanas antes** de que impacten precios de consumidor.

**Hipótesis:** Los commodities no viajan instantáneamente. Cuando hay disrupción:
- Barcos se desvían/acumulan (AIS)
- Fletes spot suben antes que contratos
- Inventarios caen
- Tiempos de entrega aumentan

### 4.2 Casos de Validación Histórica

| Evento | Fecha | Señales Visibles | Anticipación |
|--------|-------|------------------|--------------|
| Bloqueo Suez | Mar 2021 | Congestión AIS 12h antes, oil +6% | 2 días |
| Escasez chips | 2021 | Lead times +100%, autos +30% | 3 meses |
| Crisis contenedores | 2021 | Baltic Dry +400%, fletes x10 | 2 meses |
| Gas Europa | 2022 | Inventarios -30%, TTF +500% | 3 semanas |

### 4.3 Señales y Pesos

| ID | Señal | Fuente | Peso | Threshold |
|----|-------|--------|------|-----------|
| S1 | **Precio commodity 1M** | Yahoo Finance | 20% | Subida >15% |
| S2 | **Z-Score precio** | Yahoo Finance | 20% | >2σ vs histórico |
| S3 | **Volatilidad** | Yahoo Finance | 10% | >50% anualizada |
| S4 | **Google "[commodity] shortage"** | pytrends | 25% | Spike >3x |
| S5 | **ETFs relacionados** | Yahoo Finance | 10% | Confirmación +5% |
| S6 | **Baltic Dry Index** | Yahoo Finance | 15% | Subida >20% 1M |

### 4.4 Commodities a Monitorear

```python
COMMODITIES = {
    # Energía
    "CL=F": {"name": "Crude Oil", "keywords": ["oil shortage", "oil price"]},
    "NG=F": {"name": "Natural Gas", "keywords": ["gas shortage", "gas price"]},
    
    # Metales
    "GC=F": {"name": "Gold", "keywords": ["gold price"]},
    "HG=F": {"name": "Copper", "keywords": ["copper shortage"]},
    
    # Agrícolas
    "ZW=F": {"name": "Wheat", "keywords": ["wheat shortage", "bread price"]},
    "ZC=F": {"name": "Corn", "keywords": ["corn shortage"]},
    "ZS=F": {"name": "Soybeans", "keywords": ["soybean shortage"]},
}

SHIPPING_INDICATORS = {
    "Baltic Dry": "^BDI",  # Proxy
    "Container": ["ZIM", "MATX"],  # Shipping stocks
}
```

### 4.5 Fórmula de Scoring

```python
def score_supply_shock(commodity):
    signals = {}
    
    # S1: Precio 1M
    change_1m = get_price_change(commodity, days=22)
    if change_1m >= 25: signals['S1'] = 20
    elif change_1m >= 15: signals['S1'] = 12
    elif change_1m >= 10: signals['S1'] = 6
    else: signals['S1'] = 0
    
    # S2: Z-Score
    z = get_price_zscore(commodity, lookback=252)
    if z >= 3: signals['S2'] = 20
    elif z >= 2: signals['S2'] = 12
    elif z >= 1.5: signals['S2'] = 6
    else: signals['S2'] = 0
    
    # S3: Volatilidad
    vol = get_volatility(commodity)
    if vol >= 80: signals['S3'] = 10
    elif vol >= 50: signals['S3'] = 5
    else: signals['S3'] = 0
    
    # S4: Google shortage
    name = COMMODITIES[commodity]['name'].lower()
    spike = get_google_spike(f"{name} shortage")
    if spike >= 5: signals['S4'] = 25
    elif spike >= 3: signals['S4'] = 15
    elif spike >= 2: signals['S4'] = 8
    else: signals['S4'] = 0
    
    # S5: ETF confirmation
    # ... similar logic
    
    # S6: Baltic Dry
    bdi_change = get_price_change("^BDI", days=22)
    if bdi_change >= 30: signals['S6'] = 15
    elif bdi_change >= 20: signals['S6'] = 10
    else: signals['S6'] = 0
    
    return sum(signals.values())
```

### 4.6 Rutas Críticas (Futuro con AIS)

```python
CRITICAL_ROUTES = {
    "suez": {"impact": "Europe-Asia", "commodities": ["oil", "goods"]},
    "panama": {"impact": "US East-Asia", "commodities": ["goods"]},
    "hormuz": {"impact": "Global", "commodities": ["oil"], "severity": 1.0},
    "malacca": {"impact": "Asia", "commodities": ["oil", "goods"]},
}
```

### 4.7 Acciones Cuando Dispara

| Score | Acción |
|-------|--------|
| 50-75 | Evaluar posiciones en commodity, alertar operaciones |
| 76-100 | **Posición larga en commodity**, stockear inventario |

---

## 5. SISTEMA 3: BANK STRESS

### 5.1 Descripción

Detecta crisis bancarias y corridas **24-72 horas antes** del colapso.

**Hipótesis:** Los bancos son instituciones de confianza. Cuando la confianza se erosiona:
- CDS spreads suben (mercado de crédito sabe primero)
- Menciones en redes explotan
- Búsquedas de "withdraw + [bank]" aumentan
- Flujos van a money markets

### 5.2 Caso de Validación: SVB (Marzo 2023)

| Timeline | Señal | Valor |
|----------|-------|-------|
| Miércoles 8 Mar | CDS spread | 100 → 200 bps |
| Jueves 9 Mar AM | Twitter mentions | +500% |
| Jueves 9 Mar PM | Google "SVB withdraw" | +2000% |
| Viernes 10 Mar | **COLAPSO** | - |

**Ventana de acción: ~36 horas**

### 5.3 Señales y Pesos

| ID | Señal | Fuente | Peso | Threshold |
|----|-------|--------|------|-----------|
| B1 | **KRE (Regional Banks ETF) 1D** | Yahoo Finance | 20% | Caída >5% |
| B2 | **KRE 5D** | Yahoo Finance | 15% | Caída >10% |
| B3 | **VIX** | Yahoo Finance | 15% | >30 |
| B4 | **Google "bank run"** | pytrends | 20% | Spike >3x |
| B5 | **Google "FDIC insurance"** | pytrends | 10% | Spike >2x |
| B6 | **TLT (flight to safety)** | Yahoo Finance | 10% | Subida >2% 1D |
| B7 | **Peor banco regional** | Yahoo Finance | 10% | Caída >10% 1D |

### 5.4 Bancos a Monitorear

```python
REGIONAL_BANKS = [
    "KRE",   # ETF (benchmark)
    "WAL",   # Western Alliance
    "PACW",  # PacWest
    "ZION",  # Zions
    "CMA",   # Comerica
    "KEY",   # KeyCorp
    "CFG",   # Citizens Financial
    "FITB",  # Fifth Third
    "RF",    # Regions Financial
]

SYSTEMIC_BANKS = [
    "JPM", "BAC", "WFC", "C", "GS", "MS"
]
```

### 5.5 Fórmula de Scoring

```python
def score_bank_stress():
    signals = {}
    
    # B1: KRE 1D
    kre_1d = get_price_change("KRE", days=1)
    if kre_1d <= -8: signals['B1'] = 20
    elif kre_1d <= -5: signals['B1'] = 15
    elif kre_1d <= -3: signals['B1'] = 8
    else: signals['B1'] = 0
    
    # B2: KRE 5D
    kre_5d = get_price_change("KRE", days=5)
    if kre_5d <= -15: signals['B2'] = 15
    elif kre_5d <= -10: signals['B2'] = 10
    elif kre_5d <= -7: signals['B2'] = 5
    else: signals['B2'] = 0
    
    # B3: VIX
    vix = get_current_price("^VIX")
    if vix >= 40: signals['B3'] = 15
    elif vix >= 30: signals['B3'] = 10
    elif vix >= 25: signals['B3'] = 5
    else: signals['B3'] = 0
    
    # B4: Google "bank run"
    spike = get_google_spike("bank run")
    if spike >= 10: signals['B4'] = 20
    elif spike >= 5: signals['B4'] = 15
    elif spike >= 3: signals['B4'] = 10
    elif spike >= 2: signals['B4'] = 5
    else: signals['B4'] = 0
    
    # B5: Google "FDIC"
    spike_fdic = get_google_spike("FDIC insurance")
    if spike_fdic >= 3: signals['B5'] = 10
    elif spike_fdic >= 2: signals['B5'] = 5
    else: signals['B5'] = 0
    
    # B6: TLT (flight to safety)
    tlt_1d = get_price_change("TLT", days=1)
    if tlt_1d >= 3: signals['B6'] = 10
    elif tlt_1d >= 2: signals['B6'] = 6
    else: signals['B6'] = 0
    
    # B7: Worst regional bank
    worst = min(get_price_change(b, days=1) for b in REGIONAL_BANKS)
    if worst <= -15: signals['B7'] = 10
    elif worst <= -10: signals['B7'] = 6
    else: signals['B7'] = 0
    
    return sum(signals.values())
```

### 5.6 Acciones Cuando Dispara

| Score | Acción |
|-------|--------|
| 50-75 | Verificar depósitos <$250k, monitorear cada 2h |
| 76-100 | **MOVER FONDOS A BANCOS SISTÉMICOS**, puts en KRE |

---

## 6. SISTEMA 4: REAL ESTATE TREMOR

### 6.1 Descripción

Detecta correcciones en mercado inmobiliario **2-6 meses antes** de que impacten precios.

**Hipótesis:** El real estate es lento pero predecible. Los indicadores líderes:
- Días en mercado aumentan
- Ratio precio/lista cae
- Inventario sube
- Permisos de construcción colapsan
- REITs caen ANTES que precios reales

### 6.2 Caso de Validación: Phoenix 2022

| Timeline | Señal | Cambio |
|----------|-------|--------|
| May 2022 | Días en mercado | 18 → 45 días |
| Jun 2022 | Inventario | +250% |
| Jul 2022 | VNQ | -25% YTD |
| Oct 2022 | **Precios caen** | -15% |

**Anticipación: 5 meses**

### 6.3 Señales y Pesos

| ID | Señal | Fuente | Peso | Threshold |
|----|-------|--------|------|-----------|
| R1 | **VNQ (REIT ETF) 3M** | Yahoo Finance | 20% | Caída >15% |
| R2 | **XHB (Homebuilders) 3M** | Yahoo Finance | 20% | Caída >20% |
| R3 | **Mortgage Rate 30Y** | FRED | 20% | >7% o +1.5pp en 6M |
| R4 | **VNQ vs SPY (relativo)** | Yahoo Finance | 10% | Underperform >10% |
| R5 | **Google "housing crash"** | pytrends | 15% | Spike >2x |
| R6 | **Google "sell my house"** | pytrends | 10% | Spike >2x |
| R7 | **Worst homebuilder** | Yahoo Finance | 5% | Caída >20% 3M |

### 6.4 Datos de FRED

```python
FRED_SERIES = {
    "MORTGAGE30US": "30-Year Fixed Rate Mortgage Average",
    "PERMIT": "New Private Housing Units Authorized",
    "HOUST": "Housing Starts",
    "MSACSR": "Monthly Supply of Houses",
}
```

### 6.5 Fórmula de Scoring

```python
def score_real_estate():
    signals = {}
    
    # R1: VNQ 3M
    vnq_3m = get_price_change("VNQ", days=66)
    if vnq_3m <= -25: signals['R1'] = 20
    elif vnq_3m <= -15: signals['R1'] = 14
    elif vnq_3m <= -10: signals['R1'] = 8
    else: signals['R1'] = 0
    
    # R2: XHB 3M
    xhb_3m = get_price_change("XHB", days=66)
    if xhb_3m <= -30: signals['R2'] = 20
    elif xhb_3m <= -20: signals['R2'] = 14
    elif xhb_3m <= -12: signals['R2'] = 8
    else: signals['R2'] = 0
    
    # R3: Mortgage rate
    rate = get_fred_latest("MORTGAGE30US")
    if rate >= 8: signals['R3'] = 20
    elif rate >= 7: signals['R3'] = 14
    elif rate >= 6.5: signals['R3'] = 8
    else: signals['R3'] = 0
    
    # R4: Relative performance
    vnq_3m = get_price_change("VNQ", days=66)
    spy_3m = get_price_change("SPY", days=66)
    relative = vnq_3m - spy_3m
    if relative <= -15: signals['R4'] = 10
    elif relative <= -10: signals['R4'] = 6
    else: signals['R4'] = 0
    
    # R5: Google "housing crash"
    spike = get_google_spike("housing crash")
    if spike >= 4: signals['R5'] = 15
    elif spike >= 2: signals['R5'] = 8
    else: signals['R5'] = 0
    
    # R6: Google "sell my house"
    spike_sell = get_google_spike("sell my house")
    if spike_sell >= 3: signals['R6'] = 10
    elif spike_sell >= 2: signals['R6'] = 5
    else: signals['R6'] = 0
    
    # R7: Worst homebuilder
    builders = ["LEN", "DHI", "PHM", "TOL"]
    worst = min(get_price_change(b, days=66) for b in builders)
    if worst <= -30: signals['R7'] = 5
    elif worst <= -20: signals['R7'] = 3
    else: signals['R7'] = 0
    
    return sum(signals.values())
```

### 6.6 Acciones Cuando Dispara

| Score | Acción |
|-------|--------|
| 50-75 | Si compras: ESPERAR. Si vendes: Acelerar |
| 76-100 | **Reducir exposición REITs**, no comprar |

---

## 7. SISTEMA 5: GEOTENSION

### 7.1 Descripción

Detecta escaladas geopolíticas y conflictos **24-72 horas antes** de anuncios oficiales.

**Hipótesis:** Los gobiernos y militares dejan rastros operacionales antes de actuar:
- Cierran espacio aéreo (FlightRadar24)
- Mueven buques (AIS)
- Defensa sube antes de noticias
- Commodities sensibles se mueven
- Safe havens suben

### 7.2 Caso de Validación: Invasión Ucrania (Feb 2022)

| Timeline | Señal | Valor |
|----------|-------|-------|
| 22 Feb | Defensa +8% 5D | LMT, RTX, NOC |
| 23 Feb | Petróleo +10% 5D | WTI |
| 23 Feb | Oro +3% | GC=F |
| 23 Feb | NOTAM Bielorrusia | Espacio aéreo cerrado |
| 24 Feb | **INVASIÓN** | - |

**Ventana de acción: ~48 horas**

### 7.3 Señales y Pesos

| ID | Señal | Fuente | Peso | Threshold |
|----|-------|--------|------|-----------|
| G1 | **Defensa stocks promedio 5D** | Yahoo Finance | 25% | Subida >5% |
| G2 | **Petróleo 5D** | Yahoo Finance | 20% | Subida >8% |
| G3 | **Oro 5D** | Yahoo Finance | 15% | Subida >3% |
| G4 | **VIX** | Yahoo Finance | 10% | >25 |
| G5 | **Google [hotspot]** | pytrends | 20% | Spike >3x |
| G6 | **Correlación triple** | Calculated | 10% | Defensa+Oil+Gold alineados |

### 7.4 Hotspots Geopolíticos

```python
HOTSPOTS = {
    "taiwan": {
        "keywords": ["taiwan strait", "china taiwan"],
        "commodities": ["semiconductors"],
        "severity": 1.0
    },
    "ukraine": {
        "keywords": ["ukraine russia", "nato ukraine"],
        "commodities": ["oil", "gas", "wheat"],
        "severity": 0.9
    },
    "middle_east": {
        "keywords": ["israel iran", "strait hormuz"],
        "commodities": ["oil"],
        "severity": 0.95
    },
    "north_korea": {
        "keywords": ["north korea missile", "pyongyang"],
        "commodities": [],
        "severity": 0.7
    },
}
```

### 7.5 Fórmula de Scoring

```python
def score_geotension():
    signals = {}
    
    # G1: Defense stocks
    defense = ["LMT", "RTX", "NOC", "GD"]
    avg_defense = mean(get_price_change(d, days=5) for d in defense)
    if avg_defense >= 10: signals['G1'] = 25
    elif avg_defense >= 5: signals['G1'] = 15
    elif avg_defense >= 3: signals['G1'] = 8
    else: signals['G1'] = 0
    
    # G2: Oil
    oil_5d = get_price_change("CL=F", days=5)
    if oil_5d >= 15: signals['G2'] = 20
    elif oil_5d >= 8: signals['G2'] = 12
    elif oil_5d >= 5: signals['G2'] = 6
    else: signals['G2'] = 0
    
    # G3: Gold
    gold_5d = get_price_change("GC=F", days=5)
    if gold_5d >= 5: signals['G3'] = 15
    elif gold_5d >= 3: signals['G3'] = 10
    elif gold_5d >= 2: signals['G3'] = 5
    else: signals['G3'] = 0
    
    # G4: VIX
    vix = get_current_price("^VIX")
    if vix >= 35: signals['G4'] = 10
    elif vix >= 25: signals['G4'] = 6
    else: signals['G4'] = 0
    
    # G5: Google hotspots
    max_spike = 0
    for hotspot, data in HOTSPOTS.items():
        for keyword in data['keywords']:
            spike = get_google_spike(keyword)
            max_spike = max(max_spike, spike * data['severity'])
    
    if max_spike >= 5: signals['G5'] = 20
    elif max_spike >= 3: signals['G5'] = 12
    elif max_spike >= 2: signals['G5'] = 6
    else: signals['G5'] = 0
    
    # G6: Triple correlation
    if avg_defense > 3 and oil_5d > 3 and gold_5d > 1:
        signals['G6'] = 10
    else:
        signals['G6'] = 0
    
    return sum(signals.values())
```

### 7.6 Acciones Cuando Dispara

| Score | Acción |
|-------|--------|
| 50-75 | Monitorear cada 2h, evaluar exposición a región |
| 76-100 | **Posiciones en defensa/oro**, hedges VIX, reducir exposición región |

---

## 8. APIs Y FUENTES DE DATOS

### 8.1 APIs Gratuitas Confirmadas

| API | Uso | Rate Limit | Auth |
|-----|-----|------------|------|
| **Yahoo Finance** (yfinance) | Precios, volumen | Ilimitado | No |
| **FRED** (fredapi) | Datos macro, tasas | 120/min | API Key (gratis) |
| **Google Trends** (pytrends) | Búsquedas | ~100/día | No |
| **CoinGecko** | Crypto, Fear&Greed | 50/min | No |
| **Finnhub** | Insider trading | 60/min | API Key (gratis) |
| **GDELT** | Noticias globales | Ilimitado | No |
| **Alternative.me** | Fear & Greed Index | Ilimitado | No |

### 8.2 Obtener API Keys

```bash
# FRED (Federal Reserve)
# https://fred.stlouisfed.org/docs/api/api_key.html
# Gratis, instantáneo

# Finnhub
# https://finnhub.io/register
# Gratis, 60 calls/min

# NewsAPI (opcional)
# https://newsapi.org/register
# Gratis, 100 requests/día
```

### 8.3 Código de Fetcher Universal

```python
import yfinance as yf
from fredapi import Fred
from pytrends.request import TrendReq
import requests

def get_price_change(symbol: str, days: int) -> float:
    """Retorna cambio porcentual en N días"""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=f"{days+5}d")
    if len(hist) >= days:
        return ((hist['Close'].iloc[-1] / hist['Close'].iloc[-days-1]) - 1) * 100
    return 0

def get_google_spike(keyword: str) -> float:
    """Retorna ratio actual vs promedio 7 días"""
    pytrends = TrendReq()
    pytrends.build_payload([keyword], timeframe='now 7-d')
    df = pytrends.interest_over_time()
    if not df.empty:
        current = df[keyword].iloc[-1]
        avg = df[keyword].iloc[:-1].mean()
        return current / max(avg, 1)
    return 1.0

def get_fred_latest(series_id: str, api_key: str) -> float:
    """Retorna último valor de serie FRED"""
    fred = Fred(api_key=api_key)
    data = fred.get_series(series_id)
    return data.iloc[-1]
```

---

## 9. IMPLEMENTACIÓN

### 9.1 Instalación

```bash
# Clonar
git clone https://github.com/Pvrolomx/weak-signals.git
cd weak-signals

# Instalar dependencias
pip install -r requirements.txt

# Configurar
cp config/settings.example.py config/settings.py
# Editar settings.py con API keys y Telegram token
```

### 9.2 requirements.txt

```
yfinance>=0.2.28
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
fredapi>=0.5.1
pytrends>=4.9.2
finnhub-python>=2.4.18
python-telegram-bot>=20.6
schedule>=1.2.1
loguru>=0.7.2
```

### 9.3 Configuración de Telegram

```python
# config/settings.py

# 1. Habla con @BotFather → /newbot
# 2. Guarda el token
# 3. Habla con @userinfobot → obtén chat_id

TELEGRAM_BOT_TOKEN = "tu_token_aqui"
TELEGRAM_CHAT_ID = "tu_chat_id"
```

### 9.4 Ejecutar

```bash
# Test de un sistema
python -m systems.bank_stress --test

# Ejecutar con alertas
python -m systems.bank_stress

# Ejecutar todos
python run_all.py

# Dashboard (opcional)
python -m http.server 8000 --directory frontend
```

---

## 10. BACKTEST Y VALIDACIÓN

### 10.1 Eventos para Backtest

| Evento | Fecha | Sistema | Score Esperado |
|--------|-------|---------|----------------|
| SVB Colapso | 10 Mar 2023 | BANK_STRESS | >75 (48h antes) |
| Invasión Ucrania | 24 Feb 2022 | GEOTENSION | >70 (72h antes) |
| WeWork Chapter 11 | Nov 2023 | CORPORATE_DECAY | >60 (60d antes) |
| Crisis contenedores | 2021 | SUPPLY_SHOCK | >65 (30d antes) |
| Phoenix RE crash | 2022 | REAL_ESTATE | >55 (90d antes) |

### 10.2 Métricas de Evaluación

```
Precision = True Positives / (True Positives + False Positives)
Recall = True Positives / (True Positives + False Negatives)
Lead Time = Tiempo entre alerta y evento
```

### 10.3 Validación Continua

```python
# Guardar cada alerta para tracking
def log_alert(system, score, signals, timestamp):
    with open('data/alerts.jsonl', 'a') as f:
        f.write(json.dumps({
            'system': system,
            'score': score,
            'signals': signals,
            'timestamp': timestamp,
            'outcome': None  # Llenar después manualmente
        }) + '\n')
```

---

## APÉNDICE A: CHECKLIST DE IMPLEMENTACIÓN

- [ ] Configurar settings.py con API keys
- [ ] Configurar Telegram bot
- [ ] Probar cada sistema en modo --test
- [ ] Configurar cron jobs
- [ ] Crear dashboard frontend
- [ ] Documentar watchlists personalizadas
- [ ] Backtest con eventos históricos
- [ ] Ajustar thresholds según backtests

---

## APÉNDICE B: EXPANSIONES FUTURAS

1. **AIS Tracking** - MarineTraffic API para tráfico marítimo real
2. **Satellite Data** - Imágenes satelitales de puertos/instalaciones
3. **Blind/Glassdoor** - Scraping de reviews de empleados
4. **Options Flow** - Unusual options activity
5. **CDS Spreads** - Credit Default Swaps (requiere Bloomberg)
6. **NOTAM Parser** - Alertas de espacio aéreo
7. **Social Sentiment** - Twitter/Reddit sentiment analysis

---

**Hecho por duendes.app 2026**
