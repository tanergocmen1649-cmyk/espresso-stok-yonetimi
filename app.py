import streamlit as st
import pandas as pd
import os

# --- AYARLAR ---
EXCEL_FILE = 'stok.xlsx'

# --- GİRİŞ KONTROLÜ ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("☕ Espresso Stok Paneli")
    user = st.text_input("Kullanıcı Adı")
    pw = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if user == "admin" and pw == "kahve123":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Hatalı giriş!")
    st.stop()

# --- ANA UYGULAMA ---
st.title("📊 Stok Yönetim Merkezi")
if st.sidebar.button("Çıkış Yap"):
    st.session_state['logged_in'] = False
    st.rerun()

# Dosyayı Yükle
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Ürün Adı', 'Stok Adedi', 'Birim Fiyat'])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)

# --- İŞLEMLER ---
tab1, tab2, tab3 = st.tabs(["Stok Listesi", "Yeni Ürün Ekle", "Ürün Düzenle/Sil"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    with st.form("ekle_formu"):
        yeni_ad = st.text_input("Ürün Adı")
        yeni_adet = st.number_input("Adet", min_value=0)
        yeni_fiyat = st.number_input("Fiyat", min_value=0.0)
        if st.form_submit_button("Ekle"):
            yeni_satir = pd.DataFrame({'Ürün Adı': [yeni_ad], 'Stok Adedi': [yeni_adet], 'Birim Fiyat': [yeni_fiyat]})
            df = pd.concat([df, yeni_satir], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success("Ürün eklendi!")
            st.rerun()

with tab3:
    secili_urun = st.selectbox("İşlem yapılacak ürünü seçin:", df['Ürün Adı'].unique())
    
    # Mevcut veriyi getir
    urun_data = df[df['Ürün Adı'] == secili_urun].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        yeni_adet = st.number_input("Yeni Adet", value=int(urun_data['Stok Adedi']))
        yeni_fiyat = st.number_input("Yeni Fiyat", value=float(urun_data['Birim Fiyat']))
    
    if st.button("Güncelle"):
        df.loc[df['Ürün Adı'] == secili_urun, 'Stok Adedi'] = yeni_adet
        df.loc[df['Ürün Adı'] == secili_urun, 'Birim Fiyat'] = yeni_fiyat
        df.to_excel(EXCEL_FILE, index=False)
        st.success("Güncellendi!")
        st.rerun()
        
    if st.button("❌ Ürünü Sil"):
        df = df[df['Ürün Adı'] != secili_urun]
        df.to_excel(EXCEL_FILE, index=False)
        st.warning("Ürün silindi!")
        st.rerun()
