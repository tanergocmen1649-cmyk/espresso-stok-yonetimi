import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os

# --- 1. KULLANICI BİLGİLERİ ---
# Bu yapı kütüphanenin beklediği standart "config" yapısıdır.
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Espresso Lab Patron',
                'password': stauth.Hasher(['kahve123']).generate()[0]
            }
        }
    },
    'cookie': {
        'name': 'stok_sistemi',
        'key': 'anahtar123',
        'expiry_days': 30
    }
}

# --- 2. AUTHENTICATE ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

st.set_page_config(page_title="Espresso Lab Yönetim", layout="wide")

# --- 3. GİRİŞ EKRANI ---
name, authentication_status, username = authenticator.login('Giriş Ekranı', 'main')

if authentication_status == False:
    st.error('Kullanıcı adı veya şifre hatalı!')
elif authentication_status == None:
    st.warning('Lütfen giriş yapın.')
elif authentication_status:
    authenticator.logout('Çıkış', 'sidebar')
    st.title("☕ Espresso Lab - Stok Yönetim Sistemi")
    
    dosya = "stok.xlsx"
    
    # Excel yoksa oluştur
    if not os.path.exists(dosya):
        df_ilk = pd.DataFrame(columns=["Kahve_Cesidi", "Miktar_Gram"])
        df_ilk.to_excel(dosya, index=False)
    
    df = pd.read_excel(dosya)

    # --- DÜŞÜK STOK UYARISI ---
    st.write("### ⚠️ Düşük Stok Uyarıları")
    kritik_seviye = 1000 
    uyari_df = df[df["Miktar_Gram"] < kritik_seviye]
    if not uyari_df.empty:
        for index, row in uyari_df.iterrows():
            st.error(f"DİKKAT: {row['Kahve_Cesidi']} stoğu azaldı! Kalan: {row['Miktar_Gram']}g.")
    else:
        st.success("Tüm stok seviyeleri iyi durumda.")

    # --- YÖNETİM PANELİ ---
    with st.expander("🛠️ Yönetim Paneli (Ürün Ekle/Sil)"):
        col_ekle, col_sil = st.columns(2)
        with col_ekle:
            yeni_urun = st.text_input("Yeni Ürün Adı")
            baslangic_stok = st.number_input("Başlangıç Miktarı", min_value=0.0)
            if st.button("Yeni Ürün Ekle"):
                if yeni_urun and yeni_urun not in df["Kahve_Cesidi"].values:
                    yeni_satir = pd.DataFrame({"Kahve_Cesidi": [yeni_urun], "Miktar_Gram": [baslangic_stok]})
                    df = pd.concat([df, yeni_satir], ignore_index=True)
                    df.to_excel(dosya, index=False)
                    st.rerun()
        with col_sil:
            silinecek_urun = st.selectbox("Silinecek Ürün", df["Kahve_Cesidi"].unique())
            if st.button("Ürünü Kalıcı Olarak Sil"):
                df = df[df["Kahve_Cesidi"] != silinecek_urun]
                df.to_excel(dosya, index=False)
                st.rerun()

    # --- STOK TABLOSU VE İŞLEMLER ---
    st.write("### Mevcut Stok Durumu")
    st.table(df)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        islem = st.radio("İşlem Tipi:", ["Stoktan Düş (Kullanım)", "Mevcut Stoğu Artır"])
    with col2:
        kahve = st.selectbox("İşlem Yapılacak Kahve", df["Kahve_Cesidi"].unique())
        miktar = st.number_input("Miktar (Gram)", min_value=0.0, step=1.0)

    if st.button("İşlemi Onayla"):
        if kahve in df["Kahve_Cesidi"].values:
            index = df[df["Kahve_Cesidi"] == kahve].index[0]
            if islem == "Stoktan Düş (Kullanım)":
                df.at[index, "Miktar_Gram"] -= miktar
            else:
                df.at[index, "Miktar_Gram"] += miktar
            df.to_excel(dosya, index=False)
            st.rerun()
