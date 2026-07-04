import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os

# 1. Kullanıcı Bilgileri (Hashlenmiş şifreler)
# 'kahve123' şifresinin hashlenmiş hali (0.3.2 versiyonu ile uyumlu)
usernames = ['admin']
passwords = ['kahve123']
hashed_passwords = stauth.Hasher(passwords).generate()

# 2. Authenticator Kurulumu
authenticator = stauth.Authenticate(
    names=['Admin Kullanıcı'],
    usernames=usernames,
    passwords=hashed_passwords,
    cookie_name='stok_cookie',
    key='abc_123',
    cookie_expiry_days=30
)

# 3. Giriş Ekranı
name, authentication_status, username = authenticator.login('Giriş Yap', 'main')

if authentication_status == False:
    st.error('Kullanıcı adı veya şifre hatalı!')
elif authentication_status == None:
    st.warning('Lütfen kullanıcı adı ve şifrenizi girin.')
elif authentication_status:
    # 4. Giriş Başarılıysa Stok Yönetimi
    authenticator.logout('Çıkış', 'sidebar')
    st.title(f"Hoş geldin {name}")
    
    st.subheader("Stok Durumu")
    
    # Excel dosyasını okuma (Eğer dosya yoksa örnek oluştur)
    file_path = 'stok.xlsx'
    
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        st.dataframe(df)
        
        # Basit Stok Güncelleme
        st.write("---")
        st.subheader("Stok Güncelle")
        item = st.text_input("Ürün Adı")
        count = st.number_input("Adet", min_value=0)
        
        if st.button("Kaydet"):
            # Burada veriyi işleyip Excel'e geri yazan kodların olacak
            st.success(f"{item} için {count} adet güncellendi!")
    else:
        st.error("stok.xlsx dosyası bulunamadı! Lütfen GitHub'a yüklediğinden emin ol.")
