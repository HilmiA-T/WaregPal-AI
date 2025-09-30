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
        font-size: 3rem;
        font-weight: 700;
        color: #4285F4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34A853;
        margin-bottom: 1rem;
    }
    
    /* Card Styles */
    .risk-card {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
        border: none;
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
    
    # Total skor
    total_score = food_risk_score * processing_multiplier + symptom_score
    
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
        base_contaminants.extend(["Parasit berbagai jenis", "Virus Hepatitis A"])
    elif processing_method == "Dibakar":
        if food in ["Ayam", "Daging sapi"]:
            base_contaminants.append("Hidrokarbon aromatik polisiklik (PAH)")
    
    return list(set(base_contaminants))  # Remove duplicates

def get_first_aid_advice(risk_level, symptoms, contaminants):
    """Memberikan saran pertolongan pertama berdasarkan WHO & Kemenkes 2025"""
    
    advice = []
    
    # Rehidrasi (selalu disarankan)
    advice.append("🏥 **REHIDRASI**:")
    advice.append("• Minum oralit atau cairan elektrolit secara bertahap")
    advice.append("• Larutan gula-garam (1 sendok teh garam + 8 sendok teh gula dalam 1 liter air)")
    advice.append("• Cairan bening seperti air kelapa, kuah kaldu, atau teh encer")
    
    # Saran berdasarkan tingkat risiko
    if risk_level == "Tinggi":
        advice.append("🚨 **TINDAKAN SEGERA**:")
        advice.append("• Segera ke fasilitas kesehatan terdekat")
        advice.append("• Jangan mencoba memuntahkan makanan secara paksa")
        advice.append("• Bawa sampel makanan yang diduga menyebabkan keracunan")
        
    elif risk_level == "Sedang":
        advice.append("⚠️ **PENANGANAN LANJUTAN**:")
        advice.append("• Pantau gejala setiap 2-3 jam")
        advice.append("• Jika gejala memburuk dalam 6 jam, segera ke dokter")
        advice.append("• Istirahat total dan hindari aktivitas berat")
    
    # Saran berdasarkan gejala spesifik
    if "Muntah" in symptoms or "Diare" in symptoms:
        advice.append("💧 **PENANGANAN MUNTAH/DIARE**:")
        advice.append("• Minum cairan sedikit demi sedikit tetapi sering")
        advice.append("• Hindari makanan padat selama 4-6 jam pertama")
        advice.append("• Setelah mereda, konsumsi makanan lunak (bubur, pisang, apel)")
    
    if "Demam" in symptoms:
        advice.append("🌡️ **PENANGANAN DEMAM**:")
        advice.append("• Kompres dengan air hangat di dahi dan ketiak")
        advice.append("• Gunakan pakaian tipis dan nyaman")
        advice.append("• Minum air cukup untuk mencegah dehidrasi")
    
    if "Kejang" in symptoms or "Keringat dingin" in symptoms:
        advice.append("🚑 **DARURAT MEDIS**:")
        advice.append("• SEGERA Bawa ke UGD rumah sakit")
        advice.append("• Jangan berikan apapun melalui mulut selama kejang")
        advice.append("• Longgarkan pakaian dan pastikan jalan napas terbuka")
    
    # Saran berdasarkan jenis kontaminan
    if "Clostridium botulinum" in contaminants:
        advice.append("🔬 **KHUSUS BOTULISME**:")
        advice.append("• Diperlukan antitoksin botulisme")
        advice.append("• Rawat inap dengan monitoring pernapasan")
        advice.append("• Hindari obat penenang atau relaksan otot")
    
    if "Salmonella" in contaminants or "E. coli" in contaminants:
        advice.append("🦠 **INFEKSI BAKTERI**:")
        advice.append("• Antibiotik mungkin diperlukan (hanya dengan resep dokter)")
        advice.append("• Hindari obat antidiare yang memperlambat usus")
        advice.append("• Probiotik dapat membantu pemulihan flora usus")
    
    # Saran umum dari WHO & Kemenkes 2025
    advice.append("📋 **PANDUAN UMUM WHO & KEMENKES 2025**:")
    advice.append("• Jangan menggunakan antibiotik tanpa resep dokter")
    advice.append("• Hindari obat anti-muntah kecuali diresepkan dokter")
    advice.append("• Cuci tangan dengan sabun sebelum makan dan setelah BAB")
    advice.append("• Pisahkan makanan mentah dan matang selama penyimpanan")
    advice.append("• Masak makanan sampai suhu internal minimal 70°C")
    
    return advice

def main():
    # Header utama
    st.markdown('<h1 class="main-header">🍽️ WaregPal: Pertolongan Pertama Keracunan Makanan</h1>', unsafe_allow_html=True)
    
    # Container utama
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Input section
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
                
                # Dapatkan saran pertolongan pertama
                first_aid_advice = get_first_aid_advice(risk_level, selected_symptoms, contaminants)
                
                # Tampilkan hasil dalam card-card yang menarik
                st.markdown("---")
                st.markdown('<div class="sub-header">📊 Hasil Analisis</div>', unsafe_allow_html=True)
                
                # Card untuk tingkat risiko
                risk_color = "#FF6B6B" if risk_level == "Tinggi" else "#F4D03F" if risk_level == "Sedang" else "#58D68D"
                st.markdown(f"""
                <div style="background: {risk_color}; padding: 1.5rem; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); color: white; margin-bottom: 1rem;">
                    <h3 style="margin:0; color: white;">🩺 Tingkat Risiko Keracunan</h3>
                    <h2 style="margin:0; font-size: 2.5rem; color: white;">{risk_level}</h2>
                    <p style="margin:0; opacity: 0.9;">Skor Risiko: {risk_score}/10</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Card untuk kemungkinan kontaminasi
                with st.expander("🔬 Kemungkinan Kontaminasi Bakteri/Jamur", expanded=True):
                    st.markdown('<div class="contamination-card">', unsafe_allow_html=True)
                    st.write("**Kemungkinan patogen:**")
                    for i, contaminant in enumerate(contaminants, 1):
                        st.write(f"{i}. {contaminant}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Card untuk pertolongan pertama
                with st.expander("🚑 Panduan Pertolongan Pertama (WHO & Kemenkes 2025)", expanded=True):
                    st.markdown('<div class="firstaid-card">', unsafe_allow_html=True)
                    for advice_line in first_aid_advice:
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
