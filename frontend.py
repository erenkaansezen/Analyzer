import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Google Play Yorum Analizi", layout="wide")
st.title("🚀 Google Play Yorum Analizi")

app_id = st.text_input("Uygulama ID'si", "com.flatgames.patrolofficer")

if st.button("Analiz Et"):
    with st.spinner("Yorumlar analiz ediliyor..."):
        response = requests.get(f"http://localhost:8000/analyze/{app_id}")

        if response.status_code == 200:
            result = response.json()

            # Duygu sayıları
            counts = result["sentiment_counts"]
            pos = counts.get("POSITIVE", 0)
            neu = counts.get("NEUTRAL", 0)
            neg = counts.get("NEGATIVE", 0)
            total = pos + neu + neg

            # Oranlar
            pos_perc = (pos / total) * 100 if total else 0
            neu_perc = (neu / total) * 100 if total else 0
            neg_perc = (neg / total) * 100 if total else 0

            # Yorum Sayısı
            st.markdown(
                f"""
                <div style='
                    background-color: #0e1117;
                    color: white;
                    padding: 1rem;
                    border-radius: 8px;
                    font-size: 1.5rem;
                    font-weight: bold;
                    text-align: left;
                    margin-bottom: 1rem;
                '>
                    Yorum Sayısı: {total:,}
                </div>
                """, unsafe_allow_html=True
            )

            # Bar grafikleri (alt alta)
            st.markdown(
                f"""
                <style>
                    .bar-container {{
                        width: 100%;
                        background-color: #0e1117;
                        border-radius: 6px;
                        overflow: hidden;
                        margin-bottom: 10px;
                        border: 1px solid #333;
                    }}
                    .bar-fill {{
                        color: white;
                        padding: 10px;
                        font-weight: bold;
                    }}
                    .positive {{ background-color: #28a745; }}
                    .neutral  {{ background-color: #6c757d; }}
                    .negative {{ background-color: #dc3545; }}
                    .constructive {{ background-color: #ffc107; color: black; }}
                    .fake {{ background-color: #17a2b8; color: white; }}
                </style>

                <div class="bar-container">
                    <div class="bar-fill positive" style="width: {pos_perc:.1f}%">
                        Pozitif: {pos:,}
                    </div>
                </div>

                <div class="bar-container">
                    <div class="bar-fill neutral" style="width: {neu_perc:.1f}%">
                        Nötr: {neu:,}
                    </div>
                </div>

                <div class="bar-container">
                    <div class="bar-fill negative" style="width: {neg_perc:.1f}%">
                        Negatif: {neg:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("---")

            # Yapıcı Yorumlar
            st.subheader("🔧 Gelen Feedback Yorum Sayısı")
            constructive = result["constructive_comments_count"]
            feedback_perc = (constructive / total) * 100 if total else 0
            st.markdown(
                f"""
                <div class="bar-container">
                    <div class="bar-fill constructive" style="width: {feedback_perc:.1f}%">
                        Feedback: {constructive:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )



            st.markdown("---")

            # En Çok Yıldız Alan 100 Feedback Yorumu
            st.subheader("🆙 En Çok Yıldız Alan 100 Feedback Yorumu")
            df_feedback = pd.DataFrame(result["top_constructive_comments"])
            st.dataframe(df_feedback)

            
            # En Çok Yıldız Alan 100 Sahte Yorum
            st.subheader("🚫 Tespit Edilen Sahte Yorumlardan Bağzıları")
            df_fake = pd.DataFrame(result["top_fake_comments"])
            st.dataframe(df_fake)

        else:
            st.error("❌ API hatası!")
