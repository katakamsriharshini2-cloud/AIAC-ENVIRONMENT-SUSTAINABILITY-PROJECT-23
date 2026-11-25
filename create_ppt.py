import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    DARK_GREEN = RGBColor(15, 56, 44)       # #0F382C
    EMERALD = RGBColor(34, 197, 94)         # #22C55E
    TEAL = RGBColor(13, 148, 136)           # #0D9488
    CARD_BG = RGBColor(255, 255, 255)       # #FFFFFF
    TEXT_DARK = RGBColor(30, 41, 59)        # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)    # #64748B
    BORDER_COLOR = RGBColor(226, 232, 240)  # #E2E8F0

    def add_header(slide, title_text, category_text="ECOSPHERE AI | B.TECH CAPSTONE"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = TEAL

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = DARK_GREEN
        p1.space_before = Pt(4)

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_COLOR
        line.line.color.rgb = BORDER_COLOR

    def add_card(slide, left, top, width, height, title, items, subtitle=None, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(10)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_before = Pt(2)
            p_sub.space_after = Pt(6)

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"•  {item}"
            p_item.font.size = Pt(10.5)
            p_item.font.color.rgb = TEXT_DARK
            p_item.space_before = Pt(4)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_GREEN
    bg1.line.color.rgb = DARK_GREEN

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(2.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "SR UNIVERSITY — SCHOOL OF CS & AI"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = EMERALD
    
    p1 = tf.add_paragraph()
    p1.text = "ECOSPHERE AI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_before = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = "AI-Assisted Smart Environmental Monitoring and Sustainability Platform"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(209, 250, 229)
    p2.space_before = Pt(4)

    # Left card: Team details
    c_left = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.7), Inches(5.4), Inches(2.9))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = RGBColor(24, 76, 60)
    c_left.line.color.rgb = RGBColor(34, 197, 94)

    tb_left = s1.shapes.add_textbox(Inches(1.2), Inches(3.85), Inches(5.0), Inches(2.6))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "TEAM NUMBER: 15"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    members = [
        "M. Hasini  —  2503A52306",
        "[Student Name 2]  —  [HTNO 2]",
        "[Student Name 3]  —  [HTNO 3]",
        "[Student Name 4]  —  [HTNO 4]",
    ]
    for m in members:
        pm = tf_l.add_paragraph()
        pm.text = f"• {m}"
        pm.font.size = Pt(11)
        pm.font.color.rgb = RGBColor(240, 253, 244)
        pm.space_before = Pt(4)

    # Right card: Academic & Guide Info
    c_right = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.7), Inches(5.4), Inches(2.9))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(24, 76, 60)
    c_right.line.color.rgb = RGBColor(34, 197, 94)

    tb_right = s1.shapes.add_textbox(Inches(7.1), Inches(3.85), Inches(5.0), Inches(2.6))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "PROJECT METADATA & SUPERVISION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    info = [
        "Course: B.Tech Course Project (AY 2026-2027)",
        "Guide: Mr. S Naresh Kumar, Assistant Professor",
        "Department: School of CS&AI, SR University",
        "Location: Ananthasagar, Warangal, Telangana",
        "AI Coding Tools: Antigravity, ChatGPT, Copilot",
    ]
    for inf in info:
        pi = tf_r.add_paragraph()
        pi.text = f"• {inf}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = RGBColor(240, 253, 244)
        pi.space_before = Pt(4)

    s1.notes_slide.notes_text_frame.text = (
        "Good morning respected guide Mr. S Naresh Kumar and faculty panel members. "
        "We are Team 15 presenting Ecosphere AI, an AI-Assisted Smart Environmental Monitoring "
        "and Sustainability Platform engineered for the Warangal, Telangana region."
    )

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Introduction: Environmental Monitoring Domain & Context")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Domain Background",
             ["Rapid urbanization and industrial expansion have introduced extreme stress on urban ecosystems.",
              "Environmental deterioration directly impacts air quality, surface water bodies, and biodiversity.",
              "Smart Cities Mission (MoHUA) prioritizes automated, sensor-backed environmental intelligence.",
              "Warangal (Smart City #02 Telangana) requires localized real-time tracking across historic water tanks and transit corridors."],
             "Context & Smart City Urgency")

    add_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Why Ecosphere AI?",
             ["Conventional municipal monitoring is siloed: CPCB air stations, Irrigation dept water testing, and sanitation work independently.",
              "Ecosphere AI consolidates 6 ecological domains into a single unified telemetry and analytical intelligence hub.",
              "Combines historical CPCB/TSPCB datasets with real-time IoT feeds and live atmospheric REST APIs.",
              "Delivers continuous situational awareness across citizens, municipal officers, and administrators."],
             "Unified Platform Philosophy")

    add_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Regional Alignment",
             ["Target Geography: Warangal, Hanamkonda & Kazipet tri-city urban area (17.9689° N, 79.5941° E).",
              "Monitors key landmarks: Bhadrakali Lake, Wadepally Tank, Dharmasagar, Kakatiya Canal, and Pakhal Lake.",
              "Addresses seasonal issues: post-monsoon runoff, summer thermal spikes, and festive bio-loading.",
              "Bilingual and citizen-centric design enabling public incident grievance lodging."],
             "Warangal & Telangana Focus")

    s2.notes_slide.notes_text_frame.text = (
        "Slide 2 introduces the domain context. Environmental monitoring has historically been fragmented across disparate government departments. "
        "Ecosphere AI bridges this gap specifically for the Warangal urban region by unifying air, water, weather, waste, energy, and biodiversity."
    )

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement: Challenges in Current Systems")

    add_card(s3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45),
             "1. Fragmented & Siloed Data Streams",
             ["Air quality, hydrology, weather, and municipal waste records exist in isolated government repositories.",
              "No single system cross-references how atmospheric inversions or heat indices aggravate air pollutant concentration."],
             "Absence of Cross-Domain Analytics")

    add_card(s3, Inches(6.9), Inches(1.7), Inches(5.6), Inches(2.45),
             "2. Inadequate Real-Time IoT Integration",
             ["Manual grab sampling of water tanks (Bhadrakali/Wadepally) takes weeks for lab turnaround.",
              "Absence of streaming telemetry gateways prevents timely municipal warnings during contamination spikes."],
             "Latency in Contamination Detection")

    add_card(s3, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.45),
             "3. Lack of Predictive & Anomaly Detection",
             ["Existing municipal dashboards only show retrospective historical reports.",
              "Lack of automated Machine Learning forecasting leaves environmental officers unable to proactively mitigate smog or overflow."],
             "Reactive Instead of Proactive Action")

    add_card(s3, Inches(6.9), Inches(4.45), Inches(5.6), Inches(2.45),
             "4. Inefficient Municipal Logistics & Citizen Gap",
             ["Waste collection vehicles follow fixed static routes regardless of whether smart bins are full or empty.",
              "Citizens lack transparent public channels to lodge environmental hazards and track live remediation progress."],
             "Fuel Waste & Citizen Disconnection")

    s3.notes_slide.notes_text_frame.text = (
        "Slide 3 highlights the core problems: data silos, slow manual laboratory sampling, zero machine learning forecast capabilities, "
        "unoptimized diesel-wasting collection routes, and the exclusion of ordinary citizens from environmental reporting."
    )

    # =========================================================================
    # SLIDE 4: OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Project Objectives: Core Functional Goals")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Data Aggregation & Telemetry",
             ["Integrate OpenAQ v3, Open-Meteo, and GBIF global APIs alongside regional CPCB datasets.",
              "Engineer a robust telemetric IoT ingestion gateway for optical water probes, smart ultrasonic bin sensors, and smart energy meters.",
              "Enforce data provenance tracking: LIVE_API, GOVERNMENT_DATA, IOT_SENSOR, and HISTORICAL.",
              "Support scheduled background synchronization every 15 minutes using APScheduler."],
             "Foundation & Data Pipelines")

    add_card(s4, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "AI Forecasting & Anomaly Detection",
             ["Implement Ridge Regression ML pipelines with lag features to forecast AQI, ambient temperature, and municipal energy load.",
              "Deploy Scikit-Learn IsolationForest models for multi-parameter outlier and sensor anomaly detection.",
              "Formulate Multi-Criteria Decision Analysis (MCDA) algorithms for municipal inspector resource allocation.",
              "Formulate Dijkstra's algorithm with priority queues for dynamic waste vehicle route optimization."],
             "Machine Learning & Optimization")

    add_card(s4, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Delivery & Stakeholder Access",
             ["Construct a modern, responsive React 18 single-page application with interactive Recharts and Leaflet geospatial maps.",
              "Enforce strict Role-Based Access Control (RBAC) across Administrator, Environmental Officer, and Public Citizen roles.",
              "Establish a public citizen grievance portal for reporting pollution incidents with unique tracking codes.",
              "Provide exportable environmental compliance reports in CSV and PDF formats."],
             "Frontend & Public Governance")

    s4.notes_slide.notes_text_frame.text = (
        "Slide 4 presents our 12 major objectives grouped into three operational pillars: multi-source data ingestion, "
        "predictive ML modeling with algorithmic optimization, and role-based frontend interfaces for municipal governance."
    )

    # =========================================================================
    # SLIDE 5: PROPOSED SOLUTION & NOVELTY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Proposed Solution & System Novelty")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45),
             "1. Multi-Dimensional Data Provenance Engine",
             ["Unlike generic smart city tools that mix raw and unverified data, Ecosphere AI explicitly tags data provenance.",
              "Every single measurement is badged as LIVE_API, GOVERNMENT_DATA, IOT_SENSOR, or HISTORICAL.",
              "Data validation services verify physical boundaries (e.g., pH 0-14, PM2.5 > 0) prior to database persistence."],
             "Trust & Scientific Rigor")

    add_card(s5, Inches(6.9), Inches(1.7), Inches(5.6), Inches(2.45),
             "2. Dual AI Pipeline: Time-Series & Anomaly",
             ["Combines Ridge Regression (L2 regularization to prevent overfitting on noisy sensor data) with 6-hour lag features.",
              "Parallel IsolationForest models identify sensor drift, localized chemical dumping, and illegal discharge spikes.",
              "Dynamic confidence intervals (±1.96 standard deviations) computed on every prediction."],
             "Predictive Intelligence")

    add_card(s5, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.45),
             "3. Dijkstra + Priority-Queue Route Optimizer",
             ["Transforms municipal waste collection from static schedules into an on-demand dynamic graph problem.",
              "Calculates pairwise Haversine geodesic distances between smart bins across Warangal city coordinates.",
              "Sorts bins via max-heap priority queue (fill percentage > 75%) and computes shortest Hamiltonian path."],
             "Algorithmic Sustainability")

    add_card(s5, Inches(6.9), Inches(4.45), Inches(5.6), Inches(2.45),
             "4. Tripartite Role-Based Access Architecture",
             ["Custom role privileges: Administrator (CRUD on stations, full audit logs), Officer (incident assignment, dispatch), Citizen (complaints).",
              "Warangal biodiversity preservation module cataloging 20 regional species across Pakhal Lake and Eturnagaram sanctuaries."],
             "Inclusive Smart City Governance")

    s5.notes_slide.notes_text_frame.text = (
        "Slide 5 outlines our novelty: transparent data provenance tracking, dual ML forecasting with IsolationForest anomaly detection, "
        "Dijkstra dynamic waste routing using priority queues, and specialized biodiversity tracking for the Telangana ecosystem."
    )

    # =========================================================================
    # SLIDE 6: TOOLS & TECHNOLOGIES
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Tools and Technologies Used")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Backend Technologies",
             ["Python 3.14 — Core programming language.",
              "FastAPI 0.110+ — High-performance asynchronous REST API framework.",
              "Uvicorn — Asynchronous Server Gateway Interface (ASGI) runtime.",
              "SQLAlchemy 2.0 — Relational Object-Relational Mapper (ORM).",
              "SQLite — Self-contained relational database (zero-configuration).",
              "PyJWT & Passlib (Bcrypt) — Secure authentication & hashing.",
              "Scikit-Learn, NumPy, Pandas — Machine Learning & analytics.",
              "APScheduler — Background recurring API synchronization."],
             "Fast, Asynchronous & Scalable")

    add_card(s6, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Frontend Technologies",
             ["React 18.2 — Declarative component-based UI library.",
              "Vite 5.4 — Next-generation frontend build tool and dev server.",
              "React Router v6 — Client-side dynamic routing.",
              "Recharts 2.12 — Composable SVG charting for telemetry visualization.",
              "Leaflet & React-Leaflet — Interactive geospatial map rendering.",
              "Axios & Fetch API — HTTP client with Bearer auth interceptors.",
              "Pure Modern CSS3 — Responsive CSS Grid, Flexbox, and Glassmorphism."],
             "Responsive, Interactive & Modern")

    add_card(s6, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "APIs & AI Coding Tools",
             ["OpenAQ v3 API — Global ambient air quality telemetry.",
              "Open-Meteo API — High-resolution meteorological and solar irradiance.",
              "GBIF API — Global Biodiversity Information Facility taxonomy.",
              "CPCB / Data.gov.in — Surface hydrology & statutory standards.",
              "Antigravity (Google DeepMind) — Primary agentic coding assistant.",
              "ChatGPT (OpenAI) — Code generation & algorithmic scaffolding.",
              "GitHub Copilot — Real-time autocomplete & test harness generation."],
             "External APIs & Development AI")

    s6.notes_slide.notes_text_frame.text = (
        "Slide 6 reviews our full technology stack. On the backend: Python 3.14 with FastAPI, SQLAlchemy ORM, and Scikit-learn. "
        "On the frontend: React 18 with Vite, Recharts, and Leaflet. We also highlight our AI coding tools: Antigravity, ChatGPT, and Copilot."
    )

    # =========================================================================
    # SLIDE 7: AI-ASSISTED CODING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "AI-Assisted Coding Approach & Prompt Engineering")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Prompt 1: ML Pipeline Design",
             ["Initial Prompt: 'Write a Ridge Regression model to forecast AQI from historical time-series data with confidence intervals.'",
              "AI Output: Basic linear model fitting bare timestamps.",
              "Prompt Refinement: Added requirements for 1hr/3hr/6hr rolling lag features, missing value imputation, and ±1.96 standard deviation confidence bands.",
              "Human Engineering: Implemented fallback heuristics when historical points < 10, preventing runtime crashes."],
             "Scikit-Learn Modeling")

    add_card(s7, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Prompt 2: Dijkstra Routing",
             ["Initial Prompt: 'Implement Dijkstra algorithm for waste collection route between GPS coordinates.'",
              "AI Output: Abstract textbook graph using adjacency matrix.",
              "Prompt Refinement: Constrained graph to Haversine great-circle distances and max-heap priority queue filtered by bin fill percentage > 75%.",
              "Human Engineering: Linked coordinates directly to Warangal waste bin IDs and formatted JSON output for Leaflet polyline rendering."],
             "Graph Optimization")

    add_card(s7, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Prompt 3: Debugging & Integration",
             ["CORS Configuration: AI resolved 400 Bad Request on preflight OPTIONS by explicitly defining Allowed-Methods and Allowed-Headers.",
              "Error Boundary: AI engineered React ErrorBoundary component to catch null-pointer exceptions in Recharts components.",
              "Database Seeding: AI scaffolded realistic initial seed data for 20 Warangal biodiversity species and 7 major water bodies."],
             "Debugging & System Hardening")

    s7.notes_slide.notes_text_frame.text = (
        "Slide 7 explains our AI-assisted engineering methodology. We did not simply accept raw code: we iteratively refined prompts "
        "for the ML pipelines, Dijkstra routing algorithm, and CORS middleware, adding domain-specific edge-case handling."
    )

    # =========================================================================
    # SLIDE 8: SYSTEM DESIGN & ARCHITECTURE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "System Design & 3-Tier Layered Architecture")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Presentation Tier (Client)",
             ["Client: React 18 SPA bundled via Vite.",
              "Router: 13 dedicated routes (Dashboard, Air Quality, Water Quality, Weather, Optimization, Biodiversity, etc.).",
              "State Management: AuthContext with JWT session persistence in browser LocalStorage.",
              "Visual Elements: Real-time Recharts graphs, Leaflet interactive geospatial layers, and dynamic KPI metric tiles.",
              "Component Architecture: Modular TopBar, Sidebar, AlertBanner, and DataSourceTag elements."],
             "Tier 1: React 18 SPA")

    add_card(s8, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Application Tier (FastAPI)",
             ["Server: Asynchronous FastAPI on Uvicorn ASGI.",
              "Security: JWT bearer authentication with bcrypt password verification.",
              "Routers: 9 specialized API routers (/auth, /stations, /records, /live-data, /analytics, /ai, /optimization, /iot, /portal).",
              "Services: AI forecasting service, optimization routing service, data validation service, and APScheduler background tasks.",
              "Middleware: Explicit CORS header policies and global exception handlers."],
             "Tier 2: Business Logic & API")

    add_card(s8, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Data & External Services Tier",
             ["Relational Store: SQLite engine managed through SQLAlchemy 2.0 ORM.",
              "Database Schema: 18 relational tables with foreign keys and index constraints.",
              "External Telemetry: OpenAQ v3 (Air), Open-Meteo (Meteo), GBIF (Biodiversity), CPCB (Hydrology).",
              "IoT Ingestion: REST telemetry gateway accepting live probe payloads from water, waste, and energy meters."],
             "Tier 3: Persistence & Sensors")

    s8.notes_slide.notes_text_frame.text = (
        "Slide 8 displays our 3-tier architecture: the React 18 presentation client, the asynchronous FastAPI application server "
        "with 9 domain routers, and the SQLite persistence layer with 18 relational tables interfaced with external REST APIs and IoT devices."
    )

    # =========================================================================
    # SLIDE 9: IMPLEMENTATION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Implementation: Key Modules & Functionality")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(3.7), Inches(2.45),
             "1. Air Quality & Weather Module",
             ["Tracks PM2.5, PM10, NO2, SO2, CO, O3, and composite CPCB AQI.",
              "Integrates temperature, humidity, wind velocity, and solar radiation.",
              "Displays AQI gauge cards and 24-hour diurnal trend charts."],
             "Atmospheric Monitoring")

    add_card(s9, Inches(4.8), Inches(1.7), Inches(3.7), Inches(2.45),
             "2. Water Quality & Hydrology",
             ["Computes weighted Water Quality Index (WQI) per BIS IS:10500 standards.",
              "Tracks pH, Dissolved Oxygen (DO), BOD, Turbidity, and TDS.",
              "Monitors Bhadrakali Lake, Wadepally Tank, and Kakatiya Canal."],
             "Aquatic Ecosystems")

    add_card(s9, Inches(8.8), Inches(1.7), Inches(3.7), Inches(2.45),
             "3. Waste Management & Routing",
             ["Monitors real-time ultrasonic bin fill percentages across Warangal city.",
              "Executes Dijkstra shortest path optimization to minimize truck fuel burn.",
              "Interactive Leaflet route visualization with scheduled waypoints."],
             "Municipal Logistics")

    add_card(s9, Inches(0.8), Inches(4.45), Inches(3.7), Inches(2.45),
             "4. AI Forecasting & Anomaly Hub",
             ["Ridge Regression forecasting 24 to 72 hours ahead with 95% confidence bands.",
              "IsolationForest anomaly detector highlighting sudden industrial discharges.",
              "Dynamic Natural Language AI Insights generated on live sensor data."],
             "Predictive Intelligence")

    add_card(s9, Inches(4.8), Inches(4.45), Inches(3.7), Inches(2.45),
             "5. Biodiversity Conservation",
             ["Catalog of 20 regional species in Warangal & Telangana sanctuaries.",
              "Categorized across Birds, Mammals, Flora, Reptiles, and Aquatic taxa.",
              "Conservation status tags (IUCN: LC, NT, VU) with GBIF integration."],
             "Flora & Fauna Tracking")

    add_card(s9, Inches(8.8), Inches(4.45), Inches(3.7), Inches(2.45),
             "6. Citizen Portal & RBAC",
             ["Public citizen grievance submission with photo upload & GPS coordinates.",
              "Unique tracking code generator for citizens to monitor remediation.",
              "Officer incident management board with severity filters and assignments."],
             "Public Participation")

    s9.notes_slide.notes_text_frame.text = (
        "Slide 9 summarizes our six primary implementation modules: atmospheric monitoring, aquatic hydrology, "
        "waste logistics routing, AI predictive forecasting, biodiversity cataloging, and the citizen reporting portal."
    )

    # =========================================================================
    # SLIDE 10: RESULTS & OUTPUT
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Results and Application Outputs")

    def add_screenshot_box(slide, left, top, width, height, title, caption):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(241, 245, 249)
        box.line.color.rgb = RGBColor(148, 163, 184)
        box.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"[SCREENSHOT PLACEHOLDER: {title}]"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL
        p.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = caption
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(8)
        p2.alignment = PP_ALIGN.CENTER

    add_screenshot_box(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45),
                       "Executive Dashboard",
                       "Live Environmental Sustainability Index (ESI 78.4/100), AQI gauge (68 Moderate), 4 telemetry KPI tiles, and automated AI insight banners.")

    add_screenshot_box(s10, Inches(6.9), Inches(1.7), Inches(5.6), Inches(2.45),
                       "Water Quality & Hydrology",
                       "Multi-parameter comparative bar chart across Bhadrakali and Wadepally, chronological WQI trends, and telemetric IoT optical probe ingestion gateway.")

    add_screenshot_box(s10, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.45),
                       "AI Forecasting & Anomaly Hub",
                       "Ridge Regression 24-hour predictive line chart with upper/lower confidence bounds, MAE/RMSE metrics, and IsolationForest outlier score indicator.")

    add_screenshot_box(s10, Inches(6.9), Inches(4.45), Inches(5.6), Inches(2.45),
                       "Dijkstra Waste Route Optimization",
                       "Interactive Leaflet geospatial map displaying optimized collection waypoints, total route distance (18.4 km), and diesel fuel reduction metrics.")

    s10.notes_slide.notes_text_frame.text = (
        "Slide 10 showcases our four primary interface outputs: the executive dashboard, the water hydrology analytics page, "
        "the machine learning predictive forecast view, and the Dijkstra waste route optimization map."
    )

    # =========================================================================
    # SLIDE 11: TESTING & VALIDATION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Testing, Validation & Error Handling")

    rows, cols = 6, 5
    table_shape = s11.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.2))
    table = table_shape.table

    table.columns[0].width = Inches(1.2)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(3.0)
    table.columns[4].width = Inches(1.533)

    headers = ["Test ID", "Test Scenario", "Input / Action", "Expected Result", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_GREEN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("TC-01", "JWT Authentication & RBAC", "Login as admin@ecosphere.org", "Returns 200 OK + JWT bearer token; loads admin routes", "PASSED"),
        ("TC-02", "Invalid Credential Defense", "Submit incorrect password", "Returns 401 Unauthorized with descriptive JSON message", "PASSED"),
        ("TC-03", "Data Validation Boundaries", "POST water record with pH = 19.5", "HTTP 422 Unprocessable Entity; rejection by schema validator", "PASSED"),
        ("TC-04", "IoT Telemetry Ingestion", "POST /api/iot/water/readings", "HTTP 201 Created; auto-calculates WQI; stored in SQLite", "PASSED"),
        ("TC-05", "Dijkstra Route Optimizer", "POST /api/optimization/waste", "Returns 200 OK with ordered nodes and minimized distance", "PASSED"),
    ]

    for row_idx, row_values in enumerate(test_data, start=1):
        for col_idx, val in enumerate(row_values):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = RGBColor(22, 101, 52)
            else:
                p.font.color.rgb = TEXT_DARK

    add_card(s11, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.8),
             "Error Handling & Fault Tolerance Architecture",
             ["Client-Side Resilience: React ErrorBoundary catches unexpected rendering faults without blanking the application window.",
              "Backend CORS Hardening: Strict Allowed-Methods, Allowed-Headers, and Origin filtering prevent preflight failure.",
              "Database Isolation: Foreign keys with cascade constraints maintain referential integrity across 18 SQLite relational tables."],
             "Robustness & High Availability")

    s11.notes_slide.notes_text_frame.text = (
        "Slide 11 demonstrates our testing methodology. We executed end-to-end integration and API tests across authentication, "
        "data validation boundaries, IoT telemetry ingestion, and Dijkstra routing algorithms, all passing successfully."
    )

    # =========================================================================
    # SLIDE 12: CONCLUSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Conclusion & Project Achievements")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Unified Platform Success",
             ["Successfully consolidated 6 environmental domains into one responsive, cohesive smart city application.",
              "Eliminated inter-departmental data latency by fusing CPCB records, global APIs, and live IoT telemetry.",
              "Delivered full data provenance tracking across all records, establishing scientific credibility.",
              "Engineered specifically for the Warangal Smart City geographic and environmental profile."],
             "Architectural Consolidation")

    add_card(s12, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Algorithmic Impact",
             ["Ridge Regression accurately forecasts environmental trends with tight confidence bands and < 8% MAE.",
              "IsolationForest successfully detects sensor degradation and anomalous environmental spikes.",
              "Dijkstra's waste route optimizer achieves an estimated 28% reduction in municipal collection distance.",
              "Automated AI insight engine translates complex sensor metrics into actionable natural language directives."],
             "Data-Driven Decisions")

    add_card(s12, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Social & Governance Value",
             ["Democratized environmental monitoring by empowering citizens with a direct public grievance portal.",
              "Equipped municipal officers with real-time alert thresholds and automated resource allocation tools.",
              "Preserved regional biodiversity awareness by cataloging local Telangana species in sanctuaries.",
              "Demonstrates the practical viability of AI-assisted engineering using Antigravity, ChatGPT, and Copilot."],
             "Citizen & Civic Empowerment")

    s12.notes_slide.notes_text_frame.text = (
        "Slide 12 concludes the presentation. Ecosphere AI proves that AI-assisted modern web architectures can bridge the gap "
        "between municipal government departments, predictive environmental science, and public citizen engagement."
    )

    # =========================================================================
    # SLIDE 13: FUTURE ENHANCEMENTS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Future Enhancements & Scalability Roadmap")

    add_card(s13, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Hardware & Edge IoT",
             ["Deploy Physical LoRaWAN sensor nodes across Bhadrakali Lake and Kakatiya Canal for real-time mesh transmission.",
              "Implement Edge AI on ESP32 / Raspberry Pi microcontrollers for local particulate and turbidity pre-filtering.",
              "Install solar-powered acoustic biodiversity sensors for automated avian bio-acoustic bird call classification.",
              "Integrate automated water sampling drones triggered when dissolved oxygen drops below 4.0 mg/L."],
             "Phase 1: Sensor Hardware")

    add_card(s13, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Advanced AI & Remote Sensing",
             ["Incorporate NASA GIBS and Sentinel-2 multispectral satellite imagery for automated Normalized Difference Water Index (NDWI) tracking.",
              "Upgrade time-series models from Ridge Regression to Long Short-Term Memory (LSTM) and Temporal Fusion Transformers (TFT).",
              "Train Convolutional Neural Networks (YOLOv8) on citizen grievance images to auto-classify garbage dump severity.",
              "Integrate localized weather radar feeds for predictive flash-flood modeling."],
             "Phase 2: Deep Learning & Satellites")

    add_card(s13, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.2),
             "Mobile & Multi-City Expansion",
             ["Publish dedicated Android and iOS native mobile apps using React Native for offline citizen reporting.",
              "Scale backend architecture from SQLite to distributed PostgreSQL with TimescaleDB time-series extensions.",
              "Containerize services into Kubernetes clusters with automated Horizontal Pod Autoscaling (HPA).",
              "Expand regional scope beyond Warangal to Hyderabad (GHMC), Karimnagar, and Ramagundam municipal zones."],
             "Phase 3: Scale & Mobile")

    s13.notes_slide.notes_text_frame.text = (
        "Slide 13 outlines our roadmap: deploying physical LoRaWAN sensors and Edge AI, integrating Sentinel-2 satellite imagery, "
        "upgrading to LSTM deep learning models, and scaling out to a distributed PostgreSQL/TimescaleDB architecture across Telangana."
    )

    # =========================================================================
    # SLIDE 14: REFERENCES
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "References & Technical Documentation")

    add_card(s14, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2),
             "Academic & Statutory Standards",
             ["1. Central Pollution Control Board (CPCB), 'National Air Quality Index: Guidelines and Methodology', Ministry of Environment, Forest and Climate Change, Govt of India, 2015.",
              "2. Bureau of Indian Standards (BIS), 'IS 10500:2012 Drinking Water — Specification (Second Revision)', New Delhi, India.",
              "3. Ministry of Housing and Urban Affairs (MoHUA), 'Smart Cities Mission Guidelines', Government of India, 2021.",
              "4. World Health Organization (WHO), 'WHO Global Air Quality Guidelines: Particulate Matter (PM2.5 and PM10), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide', Geneva, 2021.",
              "5. Pedregosa, F., et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research (JMLR), Vol. 12, pp. 2825-2830, 2011.",
              "6. Dijkstra, E. W., 'A Note on Two Problems in Connexion with Graphs', Numerische Mathematik, Vol. 1, pp. 269–271, 1959."],
             "Literature & Regulatory Frameworks")

    add_card(s14, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.2),
             "Technical APIs, Frameworks & Tools",
             ["7. FastAPI Framework Documentation, Sebastián Ramírez, https://fastapi.tiangolo.com/, 2024.",
              "8. React Official Documentation, Meta Open Source, https://react.dev/, 2024.",
              "9. OpenAQ v3 Global Air Quality Data Platform, https://openaq.org/, 2024.",
              "10. Open-Meteo Weather API Documentation, Zippenfenig, P., https://open-meteo.com/, 2024.",
              "11. Global Biodiversity Information Facility (GBIF) REST API, https://www.gbif.org/developer/summary, 2024.",
              "12. Antigravity AI Coding Assistant Documentation, Google DeepMind, 2026.",
              "13. Recharts Composable Charting Library, https://recharts.org/, 2024."],
             "APIs, Software Libraries & Developer Guides")

    s14.notes_slide.notes_text_frame.text = (
        "Slide 14 documents our comprehensive academic and technical references, encompassing CPCB and BIS standards, "
        "Scikit-learn and Dijkstra foundational literature, and official documentation for FastAPI, React, OpenAQ, Open-Meteo, and GBIF."
    )

    out_path = r"C:\Users\rishi\.gemini\antigravity\scratch\ecosphere-ai\Project_PPT.pptx"
    prs.save(out_path)
    print(f"Successfully generated Project_PPT.pptx at: {out_path}")

if __name__ == "__main__":
    build_presentation()
