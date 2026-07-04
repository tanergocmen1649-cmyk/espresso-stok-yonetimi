import streamlit as st
import pandas as pd
import os

# --- AYARLAR ---
EXCEL_FILE = 'stok.xlsx'

# --- GİRİŞ KONTROLÜ ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Giriş Paneli")
    user = st.text_input("Kullanıcı Adı")
    pw = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if user == "admin" and pw == "kahve123":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Hatalı bilgiler!")
    st.stop()

# --- ANA UYGULAMA ---
st.title("☕ Espresso Stok Yönetimi")
if st.sidebar.button("Çıkış Yap"):
    st.session_state['logged_in'] = False
    st.rerun()

# 1. Dosyayı Yükle veya Oluştur
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Ürün Adı', 'Stok Adedi', 'Birim Fiyat'])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)

# 2. Stok Görüntüleme
st.subheader("Mevcut Stoklar")
st.dataframe(df, use_container_width=True)

# 3. Yeni Ürün Ekleme / Güncelleme
st.subheader("Stok İşlemleri")
col1, col2, col3 = st.columns(3)
with col1:
    yeni_urun = st.text_input("Ürün Adı")
with col2:
    yeni_adet = st.number_input("Adet", min_value=0)
with col3:
    yeni_fiyat = st.number_input("Fiyat", min_value=0.0)

if st.button("Kaydet / Güncelle"):
    if yeni_urun in df['Ürün Adı'].values:
        df.loc[df['Ürün Adı'] == yeni_urun, 'Stok Adedi'] = yeni_adet
        df.loc[df['Ürün Adı'] == yeni_urun, 'Birim Fiyat'] = yeni_fiyat
    else:
        yeni_satir = pd.DataFrame({'Ürün Adı': [yeni_urun], 'Stok Adedi': [yeni_adet], 'Birim Fiyat': [yeni_fiyat]})
        df = pd.concat([df, yeni_satir], ignore_index=True)
    
    df.to_excel(EXCEL_FILE, index=False)
    st.success("Stok başarıyla güncellendi!")
    st.rerun()

# 4. Ürün Silme
silinecek_urun = st.selectbox("Silinecek Ürünü Seçin", df['Ürün Adı'].unique())
if st.button("Ürünü Sil"):
    df = df[df['Ürün Adı'] != silinecek_urun]
    df.to_excel(EXCEL_FILE, index=False)
    st.warning(f"{silinecek_urun} silindi.")
    st.rerun()
