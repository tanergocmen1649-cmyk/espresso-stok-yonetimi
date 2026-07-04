import streamlit as st
import pandas as pd
import os

EXCEL_FILE = 'stok.xlsx'

# Giriş Kontrolü
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Giriş Paneli")
    user = st.text_input("Kullanıcı Adı")
    pw = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if user == "admin" and pw == "kahve123":
            st.session_state['logged_in'] = True
            st.rerun()
    st.stop()

# Dosya İşlemleri
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    st.error("stok.xlsx dosyası bulunamadı!")
    st.stop()

st.title("📊 Stok Yönetim")
tab1, tab2, tab3 = st.tabs(["Listele", "Ekle", "Düzenle/Sil"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    with st.form("ekle"):
        # Excel'indeki sütun isimlerini buraya birebir yazdım
        cesit = st.text_input("Kahve Çeşidi")
        adet = st.number_input("Stok Adedi", min_value=0)
        if st.form_submit_button("Ekle"):
            yeni = pd.DataFrame({'kahve_cesidi': [cesit], 'stok_adedi': [adet]})
            df = pd.concat([df, yeni], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success("Eklendi!")
            st.rerun()

with tab3:
    if not df.empty:
        # Excel'deki sütun isimlerine göre seçim yaptırıyoruz
        secilen = st.selectbox("Düzenlenecek Kahveyi Seç:", df['kahve_cesidi'].unique())
        
        # Seçili ürünün mevcut adedini çek
        mevcut_adet = int(df[df['kahve_cesidi'] == secilen]['stok_adedi'].iloc[0])
        yeni_adet = st.number_input("Yeni Adet", value=mevcut_adet)
        
        if st.button("Güncelle"):
            df.loc[df['kahve_cesidi'] == secilen, 'stok_adedi'] = yeni_adet
            df.to_excel(EXCEL_FILE, index=False)
            st.rerun()
            
        if st.button("❌ Sil"):
            df = df[df['kahve_cesidi'] != secilen]
            df.to_excel(EXCEL_FILE, index=False)
            st.rerun()
