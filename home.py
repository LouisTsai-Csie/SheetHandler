import streamlit as st
import json
from config import option
from config import countryList
from streamlit_lottie import st_lottie
from utils.helper import Helper

def home():
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Global Welfare Research Program</h1>",
        unsafe_allow_html=True
    )

    # with open('./src/lottie.json', 'r') as file:
        # st_lottie(json.load(file))

    st.header('Introduction')

    st.markdown(
        "<a src='https://www.facebook.com/profile.php?id=100083190949048'>FaceBook</a>",
        unsafe_allow_html=True
    )

    st.header('Tutorial')
    st.text('Please add the following email address:')
    st.text('sheetesting@sheetesting.iam.gserviceaccount.com')
    st.text('into the sharing list, and copy the url of the sheet into the text input.')


    st.subheader('Link')
    url = st.text_input('Google Sheet Link')

    function = st.radio("Choose Functionality", 
        [
            option.DATA_CORRECTION, 
            option.DATA_INPUT_COST, 
            option.DATA_OUTPUT_SUM, 
            option.DATA_CONVERSION, 
            option.DATA_GENERATION
        ]
    )

    area = st.radio("Choose Area",
        [
            "Global",
            "Taiwan"
        ]
    )

    country = st.selectbox('Choose a country',
            countryList.COUNTRY_LIST
    )

    op = st.selectbox('Choose Comma and Period Type',
        [
            'Normal',
            'Opposite'
        ]
    )

    data = {
        "area": area,
        "country": country,
        "option": op
    }


    click = st.button('Confirm')
    if click:
        if not url: st.info('Please Enter URL First')
        helper = Helper(url, function, data)

        with st.spinner('Please wait for a minute...'):
            result = helper.getResult()

        st.text(result)
        st.success('Data processing success!')
    return


if __name__ == '__main__':
    home()