import streamlit as st 
from Home import statusFunc
import streamlit.components.v1 as components
import imgkit 
import pdfkit

# with open("output/portfolio.html","r") as f:
#     report=f.read()

# components.html(report,height=8000)

# st.pyplot()
status=statusFunc()
if status == True:
    img_file=imgkit.from_file('output/portfolio.html','portfolio.jpg')
    st.image('portfolio.jpg',width=1540)
    with open("portfolio.jpg", "rb") as file:
        btn = st.download_button(
                label="Download Report",
                data=file,
                file_name="portfolio.jpg",
                mime="image/png"
            )


