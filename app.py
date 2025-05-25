import streamlit as st
import joblib
import numpy as np

# Model ve bileşenleri yükle
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")

st.title("Gelir Tahmin Aracı")
st.write("Bu uygulama, bireyin bilgilerine göre yıllık gelirinin 50K'nın üzerinde olup olmadığını tahmin eder.")

# Kullanıcı girdileri
age = st.number_input("age - Yaş", min_value=18, max_value=90, value=30)
workclass = st.selectbox("workclass - Çalışma Sınıfı", encoders['workclass'].classes_)
fnlwgt = st.number_input("fnlwgt - Nüfus Katsayısı", min_value=0, max_value=1_000_000, value=100000)
education = st.selectbox("education - Eğitim Seviyesi", encoders['education'].classes_)
education_num = st.number_input("education-num - Eğitim Sayısal Değeri", min_value=1, max_value=20, value=10)
marital_status = st.selectbox("marital.status - Medeni Durum", encoders['marital.status'].classes_)
occupation = st.selectbox("occupation - Meslek", encoders['occupation'].classes_)
relationship = st.selectbox("relationship - Hane İlişkisi", encoders['relationship'].classes_)
race = st.selectbox("race - Irk", encoders['race'].classes_)
sex = st.selectbox("sex - Cinsiyet", encoders['sex'].classes_)
capital_gain = st.number_input("capital-gain - Sermaye Kazancı", min_value=0, max_value=100000, value=0)
capital_loss = st.number_input("capital-loss - Sermaye Kaybı", min_value=0, max_value=100000, value=0)
hours = st.slider("hours-per-week - Haftalık Çalışma Saati", min_value=1, max_value=99, value=40)
native_country = st.selectbox("native.country - Doğum Ülkesi", encoders['native.country'].classes_)

# Kategorik verileri sayısala çevir
workclass_enc = encoders['workclass'].transform([workclass])[0]
education_enc = encoders['education'].transform([education])[0]
marital_enc = encoders['marital.status'].transform([marital_status])[0]
occupation_enc = encoders['occupation'].transform([occupation])[0]
relationship_enc = encoders['relationship'].transform([relationship])[0]
race_enc = encoders['race'].transform([race])[0]
sex_enc = encoders['sex'].transform([sex])[0]
native_enc = encoders['native.country'].transform([native_country])[0]

# Özellikleri numpy dizisi olarak hazırla ve ölçekle
X = np.array([[age, workclass_enc, fnlwgt, education_enc, education_num, marital_enc,
               occupation_enc, relationship_enc, race_enc, sex_enc,
               capital_gain, capital_loss, hours, native_enc]])
X_scaled = scaler.transform(X)

# Tahmin yap
if st.button("Tahmin Et"):
    y_pred = model.predict(X_scaled)[0]
    label = encoders['income'].inverse_transform([y_pred])[0]
    st.success(f"Tahmini Gelir Sınıfı: {label}")
