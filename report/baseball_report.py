import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                                 PageBreak, Image, Table, TableStyle)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

os.chdir(r"C:\Users\camde\Desktop\baseball_analytics")

# Document setup
doc = SimpleDocTemplate(
    "outputs/baseball_report.pdf",
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

# Styles
styles = getSampleStyleSheet()
style_title = ParagraphStyle('title', fontSize=18, alignment=TA_CENTER, spaceAfter=12, fontName='Helvetica-Bold')
style_subtitle = ParagraphStyle('subtitle', fontSize=14, alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica')
style_h1 = ParagraphStyle('h1', fontSize=16, spaceAfter=10, spaceBefore=16, fontName='Helvetica-Bold')
style_h2 = ParagraphStyle('h2', fontSize=12, spaceAfter=8, spaceBefore=10, fontName='Helvetica-Bold')
style_body = ParagraphStyle('body', fontSize=10, spaceAfter=6, fontName='Helvetica', leading=14)
style_code = ParagraphStyle('code', fontSize=8, fontName='Courier', spaceAfter=6, leading=12)

# Story — everything gets appended here
story = []

# ── Cover Page ───────────────────────────────────────────────
story.append(Spacer(1, 2*inch))
story.append(Paragraph("Baseball Analytics &amp; Player Performance Prediction", style_title))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Camden Johnson", style_subtitle))
story.append(Paragraph("March 2026", style_subtitle))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Tools: Python · SQL · SQLite · scikit-learn · XGBoost · SHAP", style_subtitle))
story.append(PageBreak())

# ── Project Overview ─────────────────────────────────────────
story.append(Paragraph("Project Overview", style_h1))
story.append(Paragraph(
    "In this project, we will apply industry-level data science techniques to the Lahman Baseball Database, " \
    "a historical record of Major League Baseball statistics dating back to 1871. This project demonstrates an " \
    "end-to-end data analytics pipeline including database creation, " \
    "SQL querying, data cleaning and feature selection, exploratory data analysis, and machine learning modeling." \
    "The goal is to predict the OPS for a players next season, and their probability of making the Hall of Fame",
    style_body))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Two predictive models were developed:", style_body))
story.append(Paragraph(
    "<b>1. OPS Prediction</b> — five models were trained and compared including Linear Regression, "
    "Ridge, Lasso, Random Forest, and XGBoost. Ridge Regression performed best with an RMSE "
    "of 0.079 and R² of 0.432.", style_body))
story.append(Paragraph(
    "<b>2. Hall of Fame Prediction</b> — Logistic Regression and XGBoost Classifier were compared. "
    "Logistic Regression achieved the best AUC-ROC of 0.896 with an 87% recall on inducted players.",
    style_body))


# ── Data & Methods ───────────────────────────────────────────
story.append(Paragraph("Data & Methods", style_h1))
story.append(Paragraph("<b>Data Source</b>", style_h2))
story.append(Paragraph(
    "The Lahman Baseball Database is a wide historical record of Major League Baseball " \
    "statistics from 1871 to 2025 that is constantly updated. It is maintained by Sam Lahman "
    "and the Chadwick Baseball Bureau. This database contains 28 tables including batting, pitching, " \
    "salaries, and more for over 24,000 players.",
    style_body))

story.append(Paragraph("<b>Technical Stack</b>", style_h2))
story.append(Paragraph(
    "SQLite was utilized for storage and querying the raw database. Python was used for data cleaning, " \
    "feature engineering, modeling, and visualization. Important libraries that were used include pandas," \
    " numpy, matplotlib, scikit-learn, and more for the prior mentioned tasks. ",
    style_body))

story.append(Paragraph("<b>Project Structure</b>", style_h2))
story.append(Paragraph(
    "The project is organized into four phases: (1) SQL database design and exploratory queries, "
    "(2) Python data cleaning and feature engineering, (3) exploratory data analysis and "
    "visualization, and (4) machine learning modeling. All code is available on GitHub.",
    style_body))

# ── SQL & Database Design ────────────────────────────────────
story.append(Paragraph("SQL & Database Design", style_h1))
story.append(Paragraph(
    "The Lahman CSV files were ingested into a SQLite database. Six analytical views were " \
    "created using industry-standard SQl techniques such as CTE’s. Window functions, and joins." \
    " One additional view (v_primary_position) was created and utilized in the data cleaning process. " \
    "Two key examples will be shown below",
    style_body))

story.append(Paragraph("<b>Year-Over-Year Home Run Change</b>", style_h2))
story.append(Paragraph(
    "This view uses the LAG() window function to compare each player's home run total to their "
    "previous season, partitioned by playerID to show year-over-year comparisons.",
    style_body))
story.append(Paragraph(
    "CREATE VIEW IF NOT EXISTS v_hr_yoy_change AS<br/>"
    "WITH hr_stats AS (<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;SELECT yearID, playerID, AB,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;SUM(HR) AS total_hr,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;LAG(SUM(HR)) OVER (PARTITION BY playerID ORDER BY yearID) AS lag_hr<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;FROM batting<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;WHERE AB >= 300<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;GROUP BY playerID, yearID<br/>"
    ")<br/>"
    "SELECT p.nameFirst || ' ' || p.nameLast AS player_name,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;h.yearID, h.total_hr, h.lag_hr,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;h.total_hr - h.lag_hr AS lag_diff<br/>"
    "FROM people p<br/>"
    "JOIN hr_stats h ON p.playerID = h.playerID<br/>"
    "WHERE h.yearID >= 2010<br/>"
    "ORDER BY lag_diff DESC;",
    style_code))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Primary Position</b>", style_h2))
story.append(Paragraph(
    "This view identifies each player's primary defensive position by finding the position "
    "with the most games played using a RANK() window function partitioned by player.",
    style_body))
story.append(Paragraph(
    "CREATE VIEW IF NOT EXISTS v_primary_position AS<br/>"
    "WITH pos_counts AS (<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;SELECT playerID, POS,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;SUM(G) AS total_games,<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;RANK() OVER (PARTITION BY playerID ORDER BY SUM(G) DESC) AS pos_rank<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;FROM fielding<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;GROUP BY playerID, POS<br/>"
    ")<br/>"
    "SELECT playerID, POS AS primary_position<br/>"
    "FROM pos_counts<br/>"
    "WHERE pos_rank = 1;",
    style_code))

# ── Data Cleaning ────────────────────────────────────────────
story.append(Paragraph("Data Cleaning & Feature Engineering", style_h1))
story.append(Paragraph(
    "The raw Lahman tables required significant cleaning before modeling. "
    "Key decisions are outlined below.",
    style_body))

story.append(Paragraph("<b>Era Filtering</b>", style_h2))
story.append(Paragraph(
    "Data was filtered to 1990 and beyond to ensure consistency in tracked statistics. "
    "Many pre-1990 columns such as intentional walks, sacrifice flies, and caught stealing "
    "contained large numbers of missing values due to historical record keeping limitations.",
    style_body))

story.append(Paragraph("<b>Minimum At Bat Threshold</b>", style_h2))
story.append(Paragraph(
    "Players with fewer than 300 at bats in a season were excluded from the OPS prediction "
    "model. This filters out pitchers, bench players, and partial seasons which would "
    "introduce noise and outliers into the future ops distribution.",
    style_body))

story.append(Paragraph("<b>Feature Engineering</b>", style_h2))
story.append(Paragraph(
    "Several key features were engineered from the raw statistics. " \
    "These include On Base Percentage (OBP), Slugging (SLG), and On-base plus Slugging (OPS). " \
    "Player age was calculated from birth year "
    "and season year. Our target variable (next_OPS) was created using pandas shift and group by operators.",
    style_body))

story.append(Paragraph("<b>Hall of Fame Dataset</b>", style_h2))
story.append(Paragraph(
    "A separate dataset was constructed for HOF prediction by aggregating career level stats "
    "from batting, fielding, awards, All Star appearances, and World Series wins. "
    "Active players were excluded by filtering on final game date. Primary pitchers were "
    "removed since the model focuses on position players. Players with fewer than 1000 "
    "career at bats were excluded to remove inconsequential players.",
    style_body))


# ── EDA & Visualizations ─────────────────────────────────────
story.append(Paragraph("Exploratory Data Analysis", style_h1))
story.append(Paragraph(
    "Exploratory analysis was conducted on the cleaned dataset to understand distributions, "
    "relationships between features, and key baseball insights before modeling.",
    style_body))

# Helper function for adding images
def add_image(path, width=6*inch, caption=None):
    story.append(Spacer(1, 0.1*inch))
    story.append(Image(path, width=width, height=width*0.6))
    if caption:
        story.append(Paragraph(f"<i>{caption}</i>", 
            ParagraphStyle('caption', fontSize=8, alignment=TA_CENTER, spaceAfter=8)))
    story.append(Spacer(1, 0.1*inch))

add_image("outputs/figures/next_ops_dist.png",
    caption="Figure 1: Distribution of next season OPS. roughly normal, ideal for regression modeling.")

add_image("outputs/figures/next_ops_vs_ops.png",
    caption="Figure 2: Next season OPS vs current OPS. strong linear relationship confirms OPS as the primary predictor.")

add_image("outputs/figures/avg_ops_vs_age.png",
    caption="Figure 3: Average OPS by age. players peak offensively around age 28-31.")

add_image("outputs/figures/ops_vs_sal.png",
    caption="Figure 4: OPS Vs Salary. weak correlation suggesting teams don't always get what they pay for.")

add_image("outputs/figures/ops_vs_log_sal.png",
    caption="Figure 5: OPS vs Salary (log scale). slight positive trend becomes visible with log transformation.")

add_image("outputs/figures/corr_w_next_ops.png",
    caption="Figure 6: Feature correlations with next season OPS. OPS, SLG, and BB are the strongest predictors.")

# ── OPS Prediction Model ─────────────────────────────────────
story.append(Paragraph("OPS Prediction Model", style_h1))
story.append(Paragraph(
    "Five different models were built and their performance was analyzed with RMSE and R2 scores. " \
    "These models were using player’s current season statistics to predict their following seasons OPS, " \
    "a metric that is widely considered a top indicator of a player's offensive prowess. The models were trained on an " \
    "80/20 train/test split with cross validation and hyperparameter tuning.",
    style_body))

story.append(Paragraph("<b>Model Comparison</b>", style_h2))

# Model comparison table
table_data = [
    ['Model', 'RMSE', 'R² Score'],
    ['Ridge Regression', '0.0786', '0.432'],
    ['Linear Regression', '0.0786', '0.431'],
    ['Random Forest', '0.0793', '0.421'],
    ['XGBoost', '0.0796', '0.417'],
    ['Lasso Regression', '0.0819', '0.383'],
]

table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Ridge Regression performed best with an RMSE of 0.079, meaning predictions are within "
    "roughly 0.079 OPS points on average. The dominance of linear models suggests that "
    "next season OPS has a largely linear relationship with current season statistics, "
    "limiting the advantage of complex models.",
    style_body))

story.append(Paragraph("<b>SHAP Feature Importance</b>", style_h2))
story.append(Paragraph(
    "SHAP values were calculated for the Ridge model to identify which features most influenced "
    "predictions. Current OPS, SLG, and BB were the strongest predictors, confirming that "
    "plate discipline and power hitting are the most consistent and repeatable offensive skills.",
    style_body))

add_image("outputs/figures/shap_ops.png",
    caption="Figure 7: SHAP feature importance for OPS prediction. OPS, SLG, and BB dominate.")

story.append(PageBreak())

# ── Hall of Fame Prediction Model ────────────────────────────
story.append(Paragraph("Hall of Fame Prediction Model", style_h1))
story.append(Paragraph(
    "Two models were built and their performance was analyzed with AUC-ROC, Recall, and Precision." \
    " A player's probability of admittance to the Hall of Fame was calculated based on career statistics, " \
    "both offensively and defensively, as well as accolades. The models were trained on an 80/20 train/test split with " \
    "cross validation and hyperparameter tuning.",
    style_body))

story.append(Paragraph("<b>Class Imbalance</b>", style_h2))
story.append(Paragraph(
    "Only 5.1% of qualifying players in the dataset were inducted into the Hall of Fame. "
    "This severe class imbalance was handled using class_weight='balanced' in Logistic "
    "Regression and scale_pos_weight in XGBoost. AUC-ROC and recall were used as primary "
    "evaluation metrics rather than accuracy, which is misleading under class imbalance.",
    style_body))

story.append(Paragraph("<b>Model Comparison</b>", style_h2))

hof_table_data = [
    ['Model', 'AUC-ROC', 'Recall (Inducted)', 'Precision (Inducted)'],
    ['Logistic Regression', '0.896', '0.87', '0.35'],
    ['XGBoost Classifier', '0.859', '0.74', '0.59'],
]

hof_table = Table(hof_table_data, colWidths=[2.2*inch, 1.3*inch, 1.7*inch, 1.8*inch])
hof_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(hof_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Logistic Regression outperformed XGBoost with a higher AUC-ROC of 0.896 and recall of 0.87. "
    "For Hall of Fame scouting purposes recall is the more important metric, it is better to "
    "flag too many candidates than to miss a deserving player. XGBoost showed higher precision "
    "but at the cost of missing more true inductees.",
    style_body))

story.append(Paragraph("<b>SHAP Feature Importance</b>", style_h2))
story.append(Paragraph(
    "Career seasons played, hits, RBI, and OBP were the strongest predictors of HOF induction. "
    "Notably home runs did not rank as the top feature, suggesting that longevity and "
    "consistency matter more to HOF voters than peak power. This finding aligns with the "
    "historical HOF voting patterns where players like Barry Bonds have been kept out despite "
    "elite statistics due to non-statistical considerations.",
    style_body))

add_image("outputs/figures/shap_hof.png",
    caption="Figure 8: SHAP feature importance for HOF prediction. Longevity and contact dominate over power.")


# ── Player Projections ───────────────────────────────────────
story.append(Paragraph("Player Projections", style_h1))
story.append(Paragraph(
    "Two prediction functions were built to make the models interactive. "
    "Given a playerID, each function queries the dataset and returns a prediction.",
    style_body))

story.append(Paragraph("<b>OPS Prediction Function</b>", style_h2))
story.append(Paragraph(
    "get_next_ops_prediction(playerID): returns the predicted next season OPS "
    "for a given player based on their most recent season statistics.",
    style_body))
story.append(Paragraph(
    "get_next_ops_prediction('troutmi01') → Predicted OPS: 0.923<br/>"
    "get_next_ops_prediction('judgear01') → Predicted OPS: 0.910<br/>"
    "get_next_ops_prediction('bettsmo01') → Predicted OPS: 0.881",
    style_code))

story.append(Paragraph("<b>Hall of Fame Prediction Function</b>", style_h2))
story.append(Paragraph(
    "make_hof(playerID): returns the probability of a player being inducted "
    "into the Hall of Fame based on their career statistics.",
    style_body))
story.append(Paragraph(
    "make_hof('bondsba01') → HOF Chance: 99.9%<br/>"
    "make_hof('troutmi01') → HOF Chance: 95.0%<br/>"
    "make_hof('abreubo01') → HOF Chance: 24.8%<br/>"
    "make_hof('jeterde01') → HOF Chance: 99.9%",
    style_code))


# ── Conclusions & Key Insights ───────────────────────────────
story.append(Paragraph("Conclusions & Key Insights", style_h1))

story.append(Paragraph("<b>OPS Prediction</b>", style_h2))
story.append(Paragraph(
    "Current season OPS is one of the strongest predictors of next season OPS, confirming that "
    "offensive performance is highly consistent year over year for qualified hitters. "
    "Ridge Regression outperformed Random Forest and XGBoost, suggesting the relationship "
    "between features and next season OPS is largely linear. Walk rate (BB) ranked as the "
    "top SHAP feature, supporting the sabermetric finding that plate discipline is one of "
    "the most repeatable offensive skills.",
    style_body))

story.append(Paragraph("<b>Salary & Performance</b>", style_h2))
story.append(Paragraph(
    "Salary showed only a weak correlation with OPS, even on a log scale. This supports "
    "the Moneyball hypothesis that market inefficiencies exist in baseball and teams frequently "
    "overpay for declining veterans while undervaluing young players still under team control.",
    style_body))

story.append(Paragraph("<b>Hall of Fame Prediction</b>", style_h2))
story.append(Paragraph(
    "Aggregated statistics such as total RBI, hits, and number of seasons were indicated as the " \
    "most important predictors for Hall of Fame induction. This suggests HOF voters reward " \
    "consistency in careers over peak performance. The model predicted Barry Bonds as a near-certain " \
    "HOF candidate based purely on statistics, highlighting the gap between statistical merit and the " \
    "actual voting process which incorporates character considerations.",
    style_body))

story.append(Paragraph("<b>Linear vs Complex Models</b>", style_h2))
story.append(Paragraph(
    "Linear models outperformed more complex methods in both modeling tasks. This is consistent "
    "with the nature of aggregated baseball statistics as engineered features like OPS already "
    "capture most of the signal, leaving little non-linear structure for tree based models "
    "to exploit. This finding emphasizes that model selection should be driven by the data "
    "rather than defaulting to the most complex available method. Although skill and competence with both models" \
    "was shown",
    style_body))


# ── Technical Stack ──────────────────────────────────────────
story.append(Paragraph("Technical Stack", style_h1))

tech_table_data = [
    ['Tool', 'Purpose'],
    ['SQLite', 'Database storage and querying'],
    ['Python', 'Data cleaning, modeling, and reporting'],
    ['pandas / numpy', 'Data manipulation and feature engineering'],
    ['matplotlib / seaborn', 'Data visualization'],
    ['scikit-learn', 'Machine learning pipeline and evaluation'],
    ['XGBoost', 'Gradient boosting models'],
    ['SHAP', 'Model explainability'],
    ['reportlab', 'PDF report generation'],
    ['GitHub', 'Version control and portfolio hosting'],
]

tech_table = Table(tech_table_data, colWidths=[2.5*inch, 4.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(tech_table)

# Build PDF
doc.build(story)
print("✅ PDF created at outputs/baseball_report.pdf")

