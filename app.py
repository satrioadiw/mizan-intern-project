import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Professional Donor Intelligence Report | Mizan Amanah",
    page_icon="☖",
    layout="wide"
)

# --- KONFIGURASI DATA RAMADHAN ---
ramadhan_periods = [
    {"start": "2020-04-24", "end": "2020-05-23", "label": "1441 H"},
    {"start": "2021-04-13", "end": "2021-05-12", "label": "1442 H"},
    {"start": "2022-04-02", "end": "2022-05-01", "label": "1443 H"},
    {"start": "2023-03-23", "end": "2023-04-20", "label": "1444 H"},
    {"start": "2024-03-11", "end": "2024-04-09", "label": "1445 H"}
]

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef0f2; }
    .section-divider { border-top: 3px solid #1a237e; margin-top: 40px; margin-bottom: 40px; opacity: 0.2; }
    .insight-box { background-color: #f8f9fa; padding: 25px; border-left: 8px solid #1a237e; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .report-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #dee2e6; margin-bottom: 20px; }
    h1, h2, h3 { color: #1a237e; font-weight: 800; }
    .label-bold { font-weight: bold; color: #0d47a1; }
    .sub-heading { color: #1565c0; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI LOAD DATA ---
@st.cache_data
def get_data():
    df = pd.read_csv('final_mizan_donasi_intelligence_360.csv')
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    if 'affinity_score' not in df.columns:
        try:
            df_prof = pd.read_csv('donor_intelligence_profile_360.csv')
            df = df.merge(df_prof[['donor_id', 'affinity_score']], on='donor_id', how='left')
        except:
            df['affinity_score'] = 0
    return df

try:
    df = get_data()
except:
    st.error("File dataset tidak ditemukan!")
    st.stop()

# --- SIDEBAR ---
try:
    sidebar_logo = Image.open('logo.png')
    st.sidebar.image(sidebar_logo, use_container_width=True)
except FileNotFoundError:
    pass

st.sidebar.header("⚙ Global Control Center")
selected_segments = st.sidebar.multiselect("Filter Segmen Donatur:", df['donor_segment'].unique(), default=df['donor_segment'].unique())
filtered_df = df[df['donor_segment'].isin(selected_segments)]

# --- HEADER ---
h_col1, h_col2 = st.columns([4, 1])
with h_col1:
    st.title("🏛️ Professional Report: Preference Intelligence")
    st.markdown("### Internship Data Scientist with Mizan Amanah and Digital Skola")
with h_col2:
    try:
        main_logo = Image.open('logo.png')
        st.image(main_logo, width=300)
    except FileNotFoundError:
        pass

# Metric Utama
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Total Economic Value", f"Rp {df['nominal'].sum():,.0f}")
with m2: st.metric("Processed Transactions", f"{len(df):,}")
with m3: st.metric("Unique Donor Base", f"{df['donor_id'].nunique():,}")
with m4: st.metric("Avg. Affinity Score", "91.66%")

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 0: LAPORAN AKHIR PROYEK GROUP 4
# =============================================================================
st.header("✅ Laporan Akhir Proyek Group 4: Preference Intelligence Mizan Amanah")
try:
    image = Image.open('Picture4.png')
    col_img_left, col_img_mid, col_img_right = st.columns([1, 2, 1])
    with col_img_mid:
        st.image(image, caption="Visualisasi Alur & Output Proyek Group 4", use_container_width=True)
except FileNotFoundError:
    st.warning("Gambar Picture4.png tidak ditemukan di direktori.")

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 1: 2D RFM CLUSTERING
# =============================================================================
st.header("✨ Donor Behavioral Clustering (2D RFM)")
df_2d = filtered_df.drop_duplicates('donor_id')
fig_2d = px.scatter(df_2d, x='Recency', y='Frequency', size='Monetary',
                 color='donor_segment', hover_data=['donor_id'],
                 title="Recency vs Frequency (Bubble Size = Monetary)",
                 template='plotly_white', height=600)
st.plotly_chart(fig_2d, use_container_width=True)

st.markdown("""
<div class='insight-box'>
    <p class='sub-heading'>① Cara Membaca Grafik:</p>
    <ul>
        <li><b>Sumbu X (Recency):</b> Jarak hari sejak donasi terakhir. Semakin ke kanan, donatur semakin lama tidak aktif.</li>
        <li><b>Sumbu Y (Frequency):</b> Berapa kali donatur berdonasi. Semakin ke atas, donatur semakin sering berkontribusi.</li>
        <li><b>Ukuran Gelembung (Monetary):</b> Semakin besar gelembung, semakin besar total uang yang disumbangkan.</li>
    </ul>
    <p class='sub-heading'>② Analisis Data:</p>
    <ul>
        <li>Grafik menunjukkan penumpukan di sudut kiri bawah (Recency rendah, Frequency rendah).</li>
        <li>Ini mengindikasikan banyak 'New Donors' yang perlu dipicu agar naik ke sumbu Y (menjadi Loyal).</li>
        <li>Gelembung besar yang berada di area kanan (Recency tinggi) adalah 'Major Donors' yang sedang 'tidur' dan harus segera dibangunkan.</li>
    </ul>
    <p class='sub-heading'>③ Business Insight:</p>
    <ul>
        <li><b>Internal:</b> Tim operasional harus fokus pada strategi <i>retention</i> untuk memindahkan donatur dari kiri-bawah ke kiri-atas.</li>
        <li><b>Eksternal:</b> Mizan Amanah memiliki basis donatur 'VIP' (gelembung besar) yang berisiko hilang. Diperlukan pendekatan personal khusus untuk donatur bernilai tinggi ini.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 2: PRODUCT PORTFOLIO
# =============================================================================
st.header("☖ Product Portfolio & Market Fit")
c1, c2 = st.columns(2)
with c1:
    st.subheader("✰ Revenue Driver by Category")
    prog_rev = filtered_df.groupby('program_category')['nominal'].sum().sort_values(ascending=False).reset_index()
    fig1 = px.bar(prog_rev, x='nominal', y='program_category', orientation='h', color='nominal', color_continuous_scale='teal')
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.subheader("⚖ Market Penetration (Transaction Mix)")
    prog_cnt = filtered_df['program_category'].value_counts().reset_index()
    fig2 = px.pie(prog_cnt, values='count', names='program_category', hole=0.5, color_discrete_sequence=px.colors.sequential.GnBu_r)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class='insight-box'>
    <p class='sub-heading'>① Cara Membaca Grafik:</p>
    <ul>
        <li><b>Bar Chart (Kiri):</b> Menampilkan kategori program mana yang menghasilkan uang paling banyak (Nilai Nominal).</li>
        <li><b>Donut Chart (Kanan):</b> Menampilkan kategori program mana yang paling populer secara jumlah transaksi (Volume).</li>
    </ul>
    <p class='sub-heading'>② Analisis Data:</p>
     <ul>
        <li>Terjadi dikotomi: <b>Zakat</b> adalah penyumbang dana terbesar (Revenue Driver), namun <b>Sedekah/Infaq</b> adalah pemenang dalam hal penetrasi pasar atau jumlah transaksi.</li>
        <li>Ini berarti donatur Zakat menyumbang dalam jumlah besar namun jarang, sementara donatur Sedekah menyumbang kecil namun sering.</li>
    </ul>
    <p class='sub-heading'>③ Business Insight:</p>
    <ul>
        <li><b>Internal:</b> Mizan harus menjaga akuntabilitas program Zakat karena ini tulang punggung finansial.</li>
        <li><b>Eksternal:</b> Program Sedekah/Infaq sangat efektif untuk menjaring donatur baru secara massal (akuisisi).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 3: SEASONALITY
# =============================================================================
st.header("⌒ Temporal Dynamics & Seasonality")
df_trend = filtered_df.copy()
df_trend['Month'] = df_trend['tanggal'].dt.to_period('M').dt.to_timestamp()
trend_data = df_trend.groupby('Month').size().reset_index(name='Transactions')
fig_trend = px.area(trend_data, x='Month', y='Transactions', title='Interactive Seasonality Map', template='plotly_white')
for p in ramadhan_periods:
    fig_trend.add_vrect(x0=p['start'], x1=p['end'], fillcolor="orange", opacity=0.15, layer="below", annotation_text=f"Ramadhan {p['label']}")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
<div class='insight-box'>
    <p class='sub-heading'>① Cara Membaca Grafik:</p>
    <ul>
        <li>Garis area menunjukkan fluktuasi jumlah transaksi dari waktu ke waktu. Kotak oranye menandakan periode Ramadhan setiap tahunnya.</li>
    </ul>
    <p class='sub-heading'>② Analisis Data:</p>
    <ul>
        <li>Puncak tertinggi (Peak) selalu terjadi tepat di dalam kotak Ramadhan.</li>
        <li>Pasca Ramadhan, terjadi penurunan tajam (Slumping). Pola ini berulang secara konsisten dari 2020 hingga 2024.</li>
        <li>Hal ini membuktikan ketergantungan musiman yang sangat kuat.</li>
    </ul>
    <p class='sub-heading'>③ Business Insight:</p>
    <ul>
        <li><b>Internal:</b> Beban kerja operasional akan meningkat 5-10x lipat saat Ramadhan. Perlu manajemen relawan yang baik.</li>
        <li><b>Eksternal:</b> Mizan perlu menciptakan kampanye 'Ramadhan Sepanjang Tahun' untuk menstabilkan arus donasi di bulan-bulan sepi.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 4: STRATEGIC MATRIX
# =============================================================================
st.header("⚙ Strategic Behavioral Matrix")
cola, colb = st.columns(2)
with cola:
    st.subheader("✨ Loyalty vs Preference Heatmap")
    pref_matrix = pd.crosstab(filtered_df['donor_segment'], filtered_df['program_category'], normalize='index') * 100
    fig_heat = px.imshow(pref_matrix, text_auto='.1f', aspect="auto", color_continuous_scale='YlGnBu')
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
        <p class='sub-heading'>① Cara Membaca Grafik Heatmap:</p>
        <ul>
            <li>Warna lebih gelap/biru tua menunjukkan konsentrasi donatur yang lebih tinggi pada pertemuan antara segmen loyalitas (baris) dan kategori program (kolom).</li>
        </ul>
        <p class='sub-heading'>② Analisis Data:</p>
        <p>Terlihat dominasi program Sedekah/Infaq di hampir semua segmen, namun ada 'pergeseran warna' yang menarik pada segmen Lost Donor ke arah Yatim & Pendidikan.</p>
    </div>
    """, unsafe_allow_html=True)

with colb:
    st.subheader("⚖ Affinity Score Spread")
    fig_box = px.box(filtered_df.drop_duplicates('donor_id'), x='donor_segment', y='affinity_score', color='donor_segment')
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
        <p class='sub-heading'>① Cara Membaca Grafik Boxplot:</p>
        <ul>
            <li><b>Titik Tengah (Median):</b> Menunjukkan nilai afinitas tengah.</li>
            <li><b>Rentang Kotak:</b> Menunjukkan sebaran 50% donatur. Jika kotak sangat pendek di angka 100, berarti donatur sangat fanatik hanya pada satu program.</li>
        </ul>
        <p class='sub-heading'>② Analisis Data:</p>
        <p>Skor afinitas mayoritas menumpuk di angka 100% (Single-Program Loyalist). Hal ini menunjukkan donatur Mizan memiliki 'pilihan tetap' yang jarang berubah meskipun mereka berpindah segmen dari Active ke Dormant.</p>
        <p class='sub-heading'>③ Business Insight:</p>
        <ul>
            <li><b>Strategi Penawaran:</b> Karena afinitas sangat tinggi, kampanye <i>Cross-selling</i> (menawarkan program baru) harus dilakukan dengan narasi 'pendamping', bukan pengganti program utama mereka.</li>
            <li><b>Segmentasi Konten:</b> Konten edukasi harus disesuaikan 100% dengan minat program dominan mereka agar <i>conversion rate</i> tetap tinggi.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 5: SMART LEADS GENERATOR
# =============================================================================
st.header("✰ Smart CRM Leads Generator")
st.info("Filter dan ekspor data target kampanye.")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1: target_seg = st.multiselect("Target Segmen CRM:", filtered_df['donor_segment'].unique(), default=['Active Donor (Mulai Aktif)'])
with col_f2: target_prog = st.multiselect("Minat Program:", filtered_df['dominant_program'].unique())
with col_f3: min_monetary = st.number_input("Min. Kontribusi Akumulatif (Rp):", value=0, step=500000)

leads = filtered_df[filtered_df['donor_segment'].isin(target_seg)]
if target_prog: leads = leads[leads['dominant_program'].isin(target_prog)]
leads = leads[leads['Monetary'] >= min_monetary]
leads_clean = leads[['donor_id', 'donor_segment', 'dominant_program', 'Monetary', 'Frequency', 'Recency']].drop_duplicates('donor_id')

def suggest_action(prog):
    if prog == 'Zakat': return 'Cross-Sell: Sedekah Harian'
    elif prog == 'Sedekah/Infaq': return 'Upsell: Yatim & Pendidikan'
    else: return 'Engagement: Newsletter'

leads_clean['Strategic_Action'] = leads_clean['dominant_program'].apply(suggest_action)
st.dataframe(leads_clean, use_container_width=True)

st.markdown("""
<div class='insight-box'>
    <p class='sub-heading'>① Detail Strategic Action & Panduan Eksternal:</p>
    <ul>
        <li><b>Cross-Sell: Sedekah Harian (Target: Donatur Zakat)</b>
            <br>- <b>CRM:</b> Kirimkan pesan apresiasi atas zakatnya, lalu tawarkan program Sedekah Subuh Rp2.000/hari sebagai 'tabungan akhirat harian'.
            <br>- <b>Sales & Marketing:</b> Buat konten visual tentang kemudahan berdonasi harian lewat QRIS.
        </li>
        <li><b>Upsell: Yatim & Pendidikan (Target: Donatur Sedekah)</b>
            <br>- <b>CRM:</b> Bagikan profil anak yatim binaan yang sukses sekolah. Ajak donatur naik kelas menjadi 'Orang Tua Asuh'.
            <br>- <b>Sales & Marketing:</b> Fokus pada <i>storytelling</i> emosional dan laporan transparansi biaya pendidikan.
        </li>
        <li><b>Engagement: Newsletter (Target: Segmen Lainnya)</b>
            <br>- <b>CRM:</b> Kirim kabar terbaru mengenai kegiatan asrama tanpa ajakan donasi uang keras (Hard-selling).
            <br>- <b>Sales & Marketing:</b> Tingkatkan <i>brand awareness</i> melalui video dokumenter pendek kegiatan yayasan.
        </li>
    </ul>
    <p class='sub-heading'>② Business Insight:</p>
    <ul>
        <li><b>Internal:</b> Memastikan efisiensi kerja tim dengan data yang sudah tersegmentasi (tidak <i>random broadcast</i>).</li>
        <li><b>Eksternal:</b> Membangun hubungan jangka panjang yang lebih personal dan relevan bagi donatur.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<center><p style='color:grey;'>&copy; 2026 Mizan Amanah Preference Intelligence System</p></center>", unsafe_allow_html=True)
