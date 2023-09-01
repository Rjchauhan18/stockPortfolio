import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime as dt,date, timedelta
from plotly import graph_objs as go
import db 


st.set_page_config(page_title="Stock Portfolio" , page_icon=":bar_chart:",layout="wide")

#----------------------------------------------------------------DATABASE COMPLETE----------------------------------------------------------------


def app(un):
    st.header("**STOCK PORTFOLIO**")
    st.write("---")
    if st.sidebar.button('Log Out'):
        st.session_state.status = False
        st.experimental_rerun()
    st.sidebar.header(f"**{un} , Welcome to Stock Portfolio App**")
    # st.header(long_name)
    start_date = date.today() - timedelta(days=365)
    # st.write(start_date)
    end_date = date.today()

    # st.write(end_date)

    col1, col2 = st.columns(2)

    with col1:
        st.date_input("start date",start_date)
        

        

    with col2:
        st.date_input("End date",end_date)



    # stocks = q.utils.download_returns('^NSEI')
    # print(stocks)
    # company = list(Company_Name.keys())
    try:
        c=db.fetch_stocks()
        # st.write(c)
        companys=list(c.keys())
    except:
        st.error("Can't connect to database, Please try again later.")
        st.stop()

    # company = list(stocks.keys())


    select_company = st.multiselect("Select Stock",companys)
        # select_company = st.selectbox("Select Stock",company)

    if len(select_company) == 0:
        st.info("Please select")
    else:
        companies=[]
        for company in select_company:
            select = c.get(company)
            companies.append(select)
            


        # Get the list of Nifty 50 companies
        nifty_50 = yf.Ticker("^NSEI")

        # Get the stock data
        stock_close = pd.DataFrame()
        for i,company in enumerate(companies):
            stock_close[company] = yf.download(company, start=start_date, end=end_date)["Close"]
            stock_close.rename(columns={company:select_company[i]},inplace=True)

            # stock_open["open"] = yf.download(company, start="2023-01-01", end="2023-08-12")["Open"]
        stock_close["Portfolio"]= stock_close.sum(axis=1)



        # stock_close.reset_index(inplace=True)
        # #coverting time zone to date :
        # stock_close['Year'] = stock_close['Date'].apply(lambda x:str(x)[-4:])
        # stock_close['Month'] = stock_close['Date'].apply(lambda x:str(x)[-6:-4:])
        # stock_close['Day'] = stock_close['Date'].apply(lambda x:str(x)[-6:])
        # stock_close['date'] = pd.DataFrame(stock_close['Year'] +'-' +stock_close['Month'] +'-' + stock_close['Day'])

        if stock_close not in st.session_state  or st.session_state["stock close"] != stock_close:
            st.session_state["stock close"]= stock_close
        # Add the Nifty 50 index
        # nifty_50_data = yf.download("^NSEI", start=start_date, end=end_date)["Close"]
        # st.write(nifty_50_data)


        # # Combine all the companies into one line
        # combined_data = stock_data.sum(axis=1)
        # # st.write(combined_data)
        # stock_close["Nifty 50"] = nifty_50_data
        # stock_data["combined_data"] = combined_data

        st.line_chart(stock_close)
        with st.expander("Portfolio Table"):
            st.table(stock_close)


#Login and Authentication using firebase auth

    




def SignUp():
    with st.form(key="SignUp"):
        user=st.text_input("Enter Your Username")
        Fullname=st.text_input("Enter Your Full name")
        email=st.text_input("Enter Your Email ID")
        password=st.text_input("Enter Your Password",type="password")
        re_password=st.text_input("Re-Enter Your Password",type="password")

       
        if st.form_submit_button("Submit"):
            if password==re_password:
                e=db.check(email)
                if e=="Valid Email":
                    if db.get_user(user) != None:
                        st.warning("Username already in Exist !!!")
                    else:
                        if len(user) >3:
                            if len(password) >6:
                                # Hashed_password = stauth.Hasher([password]).generate()
                                db.insert_user(user,Fullname,email,password)
                                st.success("Account successfully Created !!!")
                                st.balloons()
                            else:
                                st.warning("Password should be at least 6 characters")
                        else:
                            st.warning("Username is too short")   
                else:
                    st.warning("Invalid Email ID")
            else:
                st.error("Password does not match")

          
status=None

                        
if 'status' not in st.session_state:
    st.session_state.status=status


if st.session_state.status==False or st.session_state.status==None:
    col1,col2,col3=st.columns(3)
    with col2:
        st.title('WELCOME TO STOCK PORTFOLIO APP')

        login,signup=st.tabs(["Login", "SignUp"])

        with login:
            with st.form(key="Login"):
                username= st.text_input( 'Username')
                password= st.text_input('Password',type='password')
    
                if st.form_submit_button('Login'):
                    try:
                        loggedIn_user=db.get_user(username)

                    except:
                        pass

                    if loggedIn_user !=None:
                        
                        if loggedIn_user["Password"] == password:
                            st.session_state.status=True
                            st.session_state.un=loggedIn_user["key"]

                            st.info("You have successfully logged In")
                            # st.stop()
                            st.experimental_rerun()
                        else:
                            st.error("Incorrect Password")
                        
                    else:
                        st.error("Invalid Username")

                        
            with signup:
                SignUp()


elif st.session_state.get('status')==True:
            # st.header(st.session_state.get('un'))
            app(st.session_state.get('un'))
