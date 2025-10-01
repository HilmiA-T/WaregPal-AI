import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="WaregPal: Pertolongan Pertama Keracunan Makanan",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Custom untuk tampilan futuristik
st.markdown("""
<style>
    /* Global Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4285F4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 0 1rem;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            text-align: center;
            padding: 0 0.5rem;
        }
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34A853;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    @media (max-width: 768px) {
        .sub-header {
            font-size: 1.3rem;
            text-align: center;
        }
    }
    
    /* Card Styles */
    .risk-card {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 2rem;
        border: none;
        text-align: center;
    }
    
    .risk-card-medium {
        background: linear-gradient(135deg, #F4D03F, #F7DC6F);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 2rem;
        border: none;
        text-align: center;
    }
    
    .risk-card-low {
        background: linear-gradient(135deg, #58D68D, #82E5AA);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 2rem;
        border: none;
        text-align: center;
    }
    
    .risk-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: white;
    }
    
    .risk-level {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .risk-score {
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 0.5rem;
        color: white;
        opacity: 0.9;
    }
    
    .contamination-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 3px solid #4285F4;
        margin-bottom: 1rem;
    }
    
    .firstaid-card {
        background: linear-gradient(135deg, #34A853, #57C278);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
    }
    
    .advice-card {
        background: linear-gradient(135deg, #4285F4, #5B8DEF);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
    }
    
    .rehydration-card {
        background: linear-gradient(135deg, #F4B400, #F7C843);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #4285F4, #34A853);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #34A853, #4285F4);
    }
    
    /* Select Box Styles */
    .stSelectbox, .stMultiselect {
        border-radius: 15px;
    }
    
    /* Custom container */
    .main-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    @media (max-width: 768px) {
        .main-container {
            padding: 1rem;
            margin: 0.5rem;
        }
    }
    
    /* Mobile responsive columns */
    @media (max-width: 768px) {
        .mobile-stack {
            flex-direction: column;
        }
    }
    
    /* Center align for mobile */
    @media (max-width: 768px) {
        .center-mobile {
            text-align: center;
            justify-content: center;
        }
        
        .risk-level {
            font-size: 2.5rem;
        }
        
        .risk-card, .risk-card-medium, .risk-card-low {
            padding: 1.5rem;
            margin: 1rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Data pengetahuan tentang keracunan makanan
FOOD_SAFETY_KNOWLEDGE = {
    # Risiko berdasarkan bahan makanan
    "food_risk": {
        "Ayam": {"risk": "tinggi", "bacteria": ["Salmonella", "Campylobacter"]},
        "Daging sapi": {"risk": "sedang", "bacteria": ["E. coli", "Salmonella"]},
        "Ikan": {"risk": "sedang", "bacteria": ["Vibrio", "Listeria"]},
        "Telur": {"risk": "tinggi", "bacteria": ["Salmonella"]},
        "Sayuran hijau": {"risk": "sedang", "bacteria": ["E. coli", "Listeria"]},
        "Nasi": {"risk": "sedang", "bacteria": ["Bacillus cereus"]},
        "Mie": {"risk": "rendah", "bacteria": ["Bacillus cereus"]},
        "Susu/Olahan susu": {"risk": "sedang", "bacteria": ["Listeria", "Staphylococcus aureus"]},
        "Seafood": {"risk": "tinggi", "bacteria": ["Vibrio", "Norovirus"]},
        "Makanan kaleng": {"risk": "tinggi", "bacteria": ["Clostridium botulinum"]}
    },
    
    # Risiko berdasarkan cara pengolahan
    "processing_risk": {
        "Mentah": {"risk": "tinggi", "multiplier": 3.0},
        "Digoreng": {"risk": "rendah", "multiplier": 0.5},
        "Direbus": {"risk": "rendah", "multiplier": 0.3},
        "Dipanggang": {"risk": "sedang", "multiplier": 1.0},
        "Dibakar": {"risk": "sedang", "multiplier": 1.2},
        "Dikukus": {"risk": "rendah", "multiplier": 0.4}
    },
    
    # Gejala dan tingkat keparahan
    "symptoms_severity": {
        "Mual": {"severity": "ringan", "weight": 1},
        "Muntah": {"severity": "sedang", "weight": 2},
        "Diare": {"severity": "sedang", "weight": 2},
        "Sakit perut": {"severity": "ringan", "weight": 1},
        "Pusing": {"severity": "ringan", "weight": 1},
        "Demam": {"severity": "sedang", "weight": 2},
        "Lemas": {"severity": "sedang", "weight": 2},
        "Keringat dingin": {"severity": "berat", "weight": 3},
        "Kejang": {"severity": "berat", "weight": 4}
    }
}

def calculate_risk_level(food, processing_method, symptoms):
    """Menghitung tingkat risiko berdasarkan input pengguna"""
    
    # Risiko dasar dari makanan
    food_risk_score = {"rendah": 1, "sedang": 2, "tinggi": 3}[FOOD_SAFETY_KNOWLEDGE["food_risk"][food]["risk"]]
    
    # Multiplier dari cara pengolahan
    processing_multiplier = FOOD_SAFETY_KNOWLEDGE["processing_risk"][processing_method]["multiplier"]
    
    # Skor gejala
    symptom_score = sum(FOOD_SAFETY_KNOWLEDGE["symptoms_severity"][symptom]["weight"] for symptom in symptoms)
    
    # Total skor dengan batas maksimal 10
    total_score = min(food_risk_score * processing_multiplier + symptom_score, 10)
    
    # Menentukan tingkat risiko
    if total_score >= 8:
        return "Tinggi", total_score
    elif total_score >= 4:
        return "Sedang", total_score
    else:
        return "Rendah", total_score

def get_possible_contaminants(food, processing_method):
    """Mendapatkan kemungkinan kontaminan berdasarkan makanan dan cara pengolahan"""
    base_contaminants = FOOD_SAFETY_KNOWLEDGE["food_risk"][food]["bacteria"]
    
    # Tambahan kontaminan berdasarkan cara pengolahan
    if processing_method == "Mentah":
        base_contaminants.extend(["Parasit berbagai jenis"])
    elif processing_method == "Dibakar":
        if food in ["Ayam", "Daging sapi"]:
            base_contaminants.append("Hidrokarbon aromatik polisiklik (PAH)")
    
    # Filter: Hapus Hepatitis A dari daftar
    filtered_contaminants = [cont for cont in base_contaminants if "Hepatitis" not in cont]
    
    return list(set(filtered_contaminants))  # Remove duplicates

def get_main_advice(symptoms, risk_level):
    """Memberikan saran utama berdasarkan gejala spesifik"""
    advice = []
    
    # Saran berdasarkan gejala spesifik
    if "Muntah" in symptoms or "Diare" in symptoms:
        advice.append("**Penanganan Muntah/Diare:**")
        advice.append("• Minum cairan sedikit demi sedikit tetapi sering")
        advice.append("• Hindari makanan padat selama 4-6 jam pertama")
        advice.append("• Setelah mereda, konsumsi makanan lunak (bubur, pisang, apel)")
        advice.append("• Hindari makanan berlemak, pedas, dan susu sementara waktu")
    
    if "Demam" in symptoms:
        advice.append("**Penanganan Demam:**")
        advice.append("• Kompres dengan air hangat di dahi dan ketiak")
        advice.append("• Gunakan pakaian tipis dan nyaman")
        advice.append("• Minum air cukup untuk mencegah dehidrasi")
        advice.append("• Pantau suhu tubuh setiap 4 jam")
    
    if "Kejang" in symptoms:
        advice.append("**DARURAT MEDIS - Kejang:**")
        advice.append("• SEGERA Bawa ke UGD rumah sakit")
        advice.append("• Jangan berikan apapun melalui mulut selama kejang")
        advice.append("• Longgarkan pakaian dan pastikan jalan napas terbuka")
        advice.append("• Jangan menahan gerakan kejang")
    
    if "Keringat dingin" in symptoms:
        advice.append("**DARURAT MEDIS - Keringat Dingin:**")
        advice.append("• Segera cari pertolongan medis")
        advice.append("• Berbaring dengan posisi kaki lebih tinggi dari kepala")
        advice.append("• Jangan berikan makanan atau minuman")
        advice.append("• Pantau kesadaran terus menerus")
    
    # Saran berdasarkan tingkat risiko
    if risk_level == "Tinggi":
        advice.append("**Tindakan Segera (Risiko Tinggi):**")
        advice.append("• Segera ke fasilitas kesehatan terdekat")
        advice.append("• Jangan mencoba memuntahkan makanan secara paksa")
        advice.append("• Bawa sampel makanan yang diduga menyebabkan keracunan")
        advice.append("• Hindari mengemudi sendiri ke rumah sakit")
    
    elif risk_level == "Sedang":
        advice.append("**Pemantauan Ketat (Risiko Sedang):**")
        advice.append("• Pantau gejala setiap 2-3 jam")
        advice.append("• Jika gejala memburuk dalam 6 jam, segera ke dokter")
        advice.append("• Istirahat total dan hindari aktivitas berat")
        advice.append("• Catat perkembangan gejala")
    
    return advice

def get_rehydration_advice():
    """Memberikan saran rehidrasi standar"""
    advice = []
    advice.append("**Langkah Rehidrasi Wajib:**")
    advice.append("• Minum oralit atau cairan elektrolit secara bertahap")
    advice.append("• Larutan gula-garam (1 sendok teh garam + 8 sendok teh gula dalam 1 liter air)")
    advice.append("• Cairan bening seperti air kelapa, kuah kaldu, atau teh encer")
    advice.append("• Minum 200-300 ml setiap kali muntah atau diare")
    advice.append("• Hindari minuman berkafein, soda, dan alkohol")
    
    return advice

def get_additional_advice(contaminants):
    """Memberikan saran tambahan berdasarkan pedoman WHO/Kemenkes"""
    advice = []
    
    advice.append("**Pedoman Umum WHO & Kemenkes 2025:**")
    advice.append("• Jangan menggunakan antibiotik tanpa resep dokter")
    advice.append("• Hindari obat anti-muntah kecuali diresepkan dokter")
    advice.append("• Cuci tangan dengan sabun sebelum makan dan setelah BAB")
    advice.append("• Pisahkan makanan mentah dan matang selama penyimpanan")
    advice.append("• Masak makanan sampai suhu internal minimal 70°C")
    advice.append("• Simpan makanan pada suhu yang tepat (<5°C atau >60°C)")
    
    # Saran berdasarkan jenis kontaminan spesifik
    if "Clostridium botulinum" in contaminants:
        advice.append("**Khusus Botulisme:**")
        advice.append("• Diperlukan antitoksin botulisme di rumah sakit")
        advice.append("• Rawat inap dengan monitoring pernapasan ketat")
    
    if "Salmonella" in contaminants or "E. coli" in contaminants:
        advice.append("**Khusus Infeksi Bakteri:**")
        advice.append("• Antibiotik mungkin diperlukan (hanya dengan resep dokter)")
        advice.append("• Probiotik dapat membantu pemulihan flora usus")
    
    return advice

def main():
    # Header utama dengan div wrapper untuk mobile
    st.markdown("""
    <div class="center-mobile">
        <h1 class="main-header">🍽️ WaregPal: Pertolongan Pertama Keracunan Makanan</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Container utama
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Input section dengan responsive columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">🔍 Identifikasi Kasus</div>', unsafe_allow_html=True)
            
            # Pilihan bahan makanan
            food_options = ["Ayam", "Daging sapi", "Ikan", "Telur", "Sayuran hijau", 
                          "Nasi", "Mie", "Susu/Olahan susu", "Seafood", "Makanan kaleng"]
            selected_food = st.selectbox("🍖 Bahan Makanan Utama", food_options)
            
            # Pilihan cara pengolahan
            processing_options = ["Mentah", "Digoreng", "Direbus", "Dipanggang", "Dibakar", "Dikukus"]
            selected_processing = st.selectbox("🍳 Cara Pengolahan Makanan", processing_options)
        
        with col2:
            st.markdown('<div class="sub-header">🤒 Gejala yang Dialami</div>', unsafe_allow_html=True)
            
            # Pilihan gejala (multiple select)
            symptom_options = ["Mual", "Muntah", "Diare", "Sakit perut", "Pusing", 
                             "Demam", "Lemas", "Keringat dingin", "Kejang"]
            selected_symptoms = st.multiselect("Pilih gejala yang dialami:", symptom_options)
            
            # Tombol analisis
            analyze_button = st.button("🔬 Analisis Kasus", use_container_width=True)
        
        # Analisis dan hasil
        if analyze_button:
            if not selected_symptoms:
                st.warning("⚠️ Silakan pilih minimal satu gejala untuk analisis.")
            else:
                # Hitung tingkat risiko
                risk_level, risk_score = calculate_risk_level(selected_food, selected_processing, selected_symptoms)
                
                # Dapatkan kemungkinan kontaminan
                contaminants = get_possible_contaminants(selected_food, selected_processing)
                
                # Dapatkan saran-saran terpisah
                main_advice = get_main_advice(selected_symptoms, risk_level)
                rehydration_advice = get_rehydration_advice()
                additional_advice = get_additional_advice(contaminants)
                
                # Tampilkan hasil dalam card-card yang menarik
                st.markdown("---")
                st.markdown('<div class="sub-header center-mobile">📊 Hasil Analisis</div>', unsafe_allow_html=True)
                
                # Card untuk tingkat risiko dengan styling yang lebih baik
                if risk_level == "Tinggi":
                    risk_class = "risk-card"
                elif risk_level == "Sedang":
                    risk_class = "risk-card-medium"
                else:
                    risk_class = "risk-card-low"
                
                st.markdown(f"""
                <div class="{risk_class}">
                    <div class="risk-title">🩺 Tingkat Risiko Keracunan</div>
                    <div class="risk-level">{risk_level}</div>
                    <div class="risk-score">Skor Risiko: {risk_score}/10</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Card untuk kemungkinan kontaminasi
                with st.expander("🔬 Kemungkinan Kontaminasi Bakteri/Jamur", expanded=True):
                    st.markdown('<div class="contamination-card">', unsafe_allow_html=True)
                    st.write("**Kemungkinan patogen:**")
                    for i, contaminant in enumerate(contaminants, 1):
                        st.write(f"{i}. {contaminant}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Card untuk SARAN UTAMA
                with st.expander("💡 Saran Utama (Berdasarkan Gejala)", expanded=True):
                    st.markdown('<div class="advice-card">', unsafe_allow_html=True)
                    if main_advice:
                        for advice_line in main_advice:
                            if advice_line.startswith("**"):
                                st.markdown(f"**{advice_line}**")
                            else:
                                st.write(advice_line)
                    else:
                        st.write("• Istirahat yang cukup")
                        st.write("• Pantau perkembangan gejala")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Card untuk REHIDRASI
                with st.expander("💧 Rehidrasi", expanded=True):
                    st.markdown('<div class="rehydration-card">', unsafe_allow_html=True)
                    for advice_line in rehydration_advice:
                        if advice_line.startswith("**"):
                            st.markdown(f"**{advice_line}**")
                        else:
                            st.write(advice_line)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Card untuk SARAN TAMBAHAN
                with st.expander("📋 Saran Tambahan (Pedoman WHO/Kemenkes)", expanded=True):
                    st.markdown('<div class="firstaid-card">', unsafe_allow_html=True)
                    for advice_line in additional_advice:
                        if advice_line.startswith("**"):
                            st.markdown(f"**{advice_line}**")
                        else:
                            st.write(advice_line)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Informasi tambahan
                st.info("""
                **📝 Catatan Penting:** 
                - Informasi ini merupakan panduan umum dan tidak menggantikan konsultasi medis
                - Segera hubungi dokter atau fasilitas kesehatan terdekat untuk penanganan profesional
                - Simpan sampel makanan yang diduga menyebabkan keracunan untuk pemeriksaan lebih lanjut
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🩺 <strong>WaregPal</strong> - Sistem Pakar Pertolongan Pertama Keracunan Makanan</p>
        <p>Berdasarkan Panduan WHO & Kementerian Kesehatan RI 2025</p>
        <p>© 2025 - Untuk konsultasi medis profesional, hubungi dokter atau fasilitas kesehatan terdekat</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
