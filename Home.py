import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime as dt,date, timedelta
from plotly import graph_objs as go
import db 
import quantstats as qs
import riskfolio as rp
import numpy as np
from report import download_report

st.set_page_config(page_title="Stock Portfolio" , page_icon=":bar_chart:",layout="wide")

# Login / SignUp setup with session state
status=None

def statusFunc():
    return st.session_state.status

# start_date and end_date
start_date = date.today() - timedelta(days=365)
# st.write(start_date)

end_date = date.today()



#----------------------------------------------------------------DATABASE COMPLETE----------------------------------------------------------------



def down(symbol,start,end):
    s=symbol.split('.')
    s[0] = qs.utils.download_returns(symbol)
    s[0]=s[0].loc[start:end]
    # print(s[0])
    s[0].index=s[0].index.tz_localize(None)
    # qs.plots.daily_returns(s[0],benchmark="IN")
    # qs.plots.returns(s[0])
    return s[0]

def portfolio_vs_symbol(df,symbol):
    fig = go.Figure()

    # df[symbol] = down(symbol, start=start_date, end=end_date)
    # # st.write(symbol_data)
    # # df[symbol]=symbol_data
    # st.write(df)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Portfolio'], name="Portfolio"))
    fig.add_trace(go.Scatter(x=df['Date'], y=df[symbol], name=symbol))


    fig.layout.update(title_text=f'Portfolio vs {symbol}', xaxis_rangeslider_visible=True)
    
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig , use_container_width=True)


def plot_portfolio_data(tickerDf):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tickerDf['Date'], y=tickerDf['Portfolio'], name="Portfolio"))
        fig.layout.update(
            title_text='Portfolio', xaxis_rangeslider_visible=True)
        
        fig.update_yaxes(automargin=True)
        st.plotly_chart(fig , use_container_width=True)

def app(un):



    st.header("**STOCK PORTFOLIO**",anchor=False)
    st.write("---")

    # Log out button
    with st.container():
        with st.container():
            st.sidebar.header(f"**{un} , Welcome to Stock Portfolio App**")

        with st.container():
            if st.sidebar.button('Log Out'):
                st.session_state.status = False
                st.session_state.un = None  # Reset the username
                st.experimental_set_query_params()  # Trigger rerun by updating query params
                st.session_state.i = 0  # Reset any other session state variables if necessary
                st.stop()  # Stop the execution to refresh the app

    # created i variable for getting the stocks and symbol dictionary only once
    i=0
    if i not in st.session_state:
        st.session_state["i"]=i
     

    if st.session_state.i==0:
        # st.write(Udata)
        st.session_state.i+=1
        try:
            c=db.fetch_stocks()
            # st.write(c)
            companys=list(c.keys())
        except:
            st.error("Can't connect to database, Please try again later.")
            st.stop()
        Udata=db.get_user(un)


    select_company = st.multiselect("Select Stock",companys)
    
    if 'db_list' in Udata:
        # st.write(Udata['db_list'])
        # creating list l of information about selected company . information like qty,start_date,end_date and it can be chage from given table
        db_l=[]

        if len(select_company)!=0 :
            for selected in select_company:
                new_company={c.get(selected):{"Qty":1,"Start_date":str(start_date),"End_date":str(end_date)}}
                Udata['db_list'].update(new_company)
        if Udata['db_list']!=None:
            db_company=[ x for x in Udata['db_list']]
            # st.write(ne)

            
            # st.write(qty)
            # st.write(startDate)
            # st.write(endDate)
            companies=[]
            for i,company in enumerate(db_company):
                # select = c.get(company)
                # st.write(select)
                qty=int(Udata['db_list'].get(db_company[i])["Qty"])
                startDate=Udata['db_list'].get(db_company[i])["Start_date"]
                dt_obj = dt.strptime(startDate, '%Y-%m-%d')
                dt_no_time = dt_obj.date()  

                endDate=Udata['db_list'].get(db_company[i])["End_date"]
                dt_obj2 = dt.strptime(endDate, '%Y-%m-%d')
                dt_no_time2 = dt_obj2.date()

                companies.append(company)
                l1={"Company": company, "Qty": qty, "Start_date":dt_no_time, "End_date":dt_no_time2 }

                db_l.append(l1)

            # print(companies)
            # st.write(companies)

            df = pd.DataFrame(db_l)
            with st.expander("Data Info"):
                c1,c2=st.columns([0.95,2])
                with c2:
                    edited_df = st.data_editor(df,
                        column_config={
                            "Company":st.column_config.TextColumn(help="Company"),
                            "Qty":st.column_config.NumberColumn(help="How many Stock You have ?"),
                            "Start_date" : st.column_config.DateColumn("Start Date",help="Enter the date when you bought the stock"),
                            "End_date" : st.column_config.DateColumn("End Date",help="Enter the date when you sold the stock or current date will be counted")

                        }
                                            
                    )
            # data_metrics()
            
            if st.button('SAVE'):

                    # nifty_50 = yf.Ticker("^NSEI")

                    # Get the stock data
                    stock_close = pd.DataFrame()
                    db_dic={}

                    # db_list=[]
                    for i,company in enumerate(companies):
                        try :

                            db_l1={ company:{"Qty": str(edited_df["Qty"][i]), "Start_date": str(edited_df["Start_date"][i]), "End_date": str(edited_df["End_date"][i])}}
                            db_dic.update(db_l1)
                            # stock_close[company] = yf.download(company, start=edited_df["Start_date"][i], end=edited_df["End_date"][i])["Close"]
                            stock_close[company] = down(company,edited_df["Start_date"][i],edited_df["End_date"][i])#yf.download(company, start=edited_df["Start_date"][i], end=edited_df["End_date"][i])["Close"]
                            stock_close[company] = stock_close[company] * edited_df["Qty"][i]
                            # stock_close.rename(columns={company:select_company[i]},inplace=True)
                        except :
                            st.warning(f"can't able to fetch the data of  {company} , Please select other.")
                            # st.write(e)
                    
                    #Adding Data of list companies and qty,startdate,enddate into database
                    db.Update_db_list(un,db_dic)
                    # qs.reports.html(stock_close,title="portfolio",output="output/portfolio.html")
                    if stock_close.shape[1] > 1:  # Ensure there is more than 1 column (stocks) to plot
                        # qs.reports.html(stock_close, title="portfolio", output="output/portfolio.html")
                        st.write(companies)
                        rpt=download_report(companies,start_date,end_date)
                        st.pyplot(rpt,clear_figure=True)
                    else:
                        st.warning("Not enough data to generate the report")

                        # stock_open["open"] = yf.download(company, start="2023-01-01", end="2023-08-12")["Open"]
                    stock_close["Portfolio"]= stock_close.sum(axis=1)



                    stock_close.reset_index(inplace=True)
                    #coverting time zone to date :
                    # stock_close['Year'] = stock_close['Date'].apply(lambda x:str(x)[-4:])
                    # stock_close['Month'] = stock_close['Date'].apply(lambda x:str(x)[-6:-4:])
                    # stock_close['Day'] = stock_close['Date'].apply(lambda x:str(x)[-6:])
                    # stock_close['date'] = pd.DataFrame(stock_close['Year'] +'-' +stock_close['Month'] +'-' + stock_close['Day'])

                    # if stock_close not in st.session_state  or st.session_state["stock close"] != stock_close:
                    st.session_state["stock close"]= stock_close
                    # Add the Nifty 50 index
                    # nifty_50_data = yf.download("^NSEI", start=start_date, end=end_date)["Close"]
                    # st.write(nifty_50_data)


                    # # Combine all the companies into one line
                    # combined_data = stock_data.sum(axis=1)
                    # # st.write(combined_data)
                    # stock_close["Nifty 50"] = nifty_50_data
                    # stock_data["combined_data"] = combined_data
                    # st.write(stock_close)
                    # st.line_chart(stock_close,y=['Portfolio'])
                    # col1,col2=st.columns(2)
                    # with col1:

                    # st.write(stock_close)
                    # m1,m2,m3=st.columns(3)
                    # st.write()
                    # avg_return=qs.stats.avg_return(stock_close["Portfolio"])
                    
                    # m1.metric("Daily Return",avg_return,avg_return*100)
                    # m2.metric("Portfolio Return","20%","Rs. 2000")
                    # m3.metric("Total Return",str(stock_close["Portfolio"][len(stock_close["Portfolio"]) -1]),"Rs. 2000")
                    # st.write(stock_close)
                    tab1 , tab2 = st.tabs(["Total Return","Total Return vs. Nifty 50"])
                    with tab1:
                        plot_portfolio_data(stock_close)
                    with tab2:
                        stock_close['Date']= pd.to_datetime(stock_close['Date'])
                        # oldest date user has choosen in to start date column and newest date user has choosen into end date column
                        st_dates=stock_close['Date'].min()
                        # st.write(st_dates)
                        end_dates= stock_close['Date'].max()
                        # st.write(st_dates,end_dates)
                        try:
                            sym=down('^NSEI',st_dates,end_dates)
                            if len(sym)!=len(stock_close):
                                sym=sym[:-1]
                    
                            stock_close['Nifty50']=sym.values
                            # stock_close=pd.concat([stock_close,sym])
                            # st.write(stock_close.columns)

                            stock_close.rename(columns = { 0 :'Nifty50'}, inplace = True)
                            # st.write(stock_close.columns)

                            # st.write(stock_close)
                            # Add the Nifty 50 index
                            # symbol=down('^NSEI')#,edited_df["Start_date"].max(),edited_df["End_date"].max())
                            portfolio_vs_symbol(stock_close,'Nifty50')
                        except:
                            pass

                   

                      
                        
                    # with col2:

        
            
    else:
        if len(select_company) == 0:
            st.info("Please select")
        else:

            # creating list l of information about selected company . information like qty,start_date,end_date and it can be chage from given table
            l=[]

            # l=  [{"Qty": company, "Start": st.date_input("start date",start_date), "End": st.date_input("End date",end_date)}]
            companies=[]
            
            for company in select_company:
                select = c.get(company)
                companies.append(select)
                l1={"Company": company, "Qty": 1, "Start_date": start_date, "End_date": end_date}

                l.append(l1)
                        
            df = pd.DataFrame(l)
            with st.expander(":Green[Data Info]"):
                c1,c2=st.columns([1/2,2])
                with c2:
                    edited_df = st.data_editor(df,
                        column_config={
                            "Company":st.column_config.TextColumn(help="Company"),
                            "Qty":st.column_config.NumberColumn(help="How many Stock You have ?"),
                            "Start_date" : st.column_config.DateColumn("Start Date",help="Enter the date when you bought the stock"),
                            "End_date" : st.column_config.DateColumn("End Date",help="Enter the date when you sold the stock or current date will be counted")

                        }
                                            
                    )
            
            # all the symbols data  run according to information and we get data when 'SAVE' button is clicked
            if st.button('SAVE'):

                # nifty_50 = yf.Ticker("^NSEI")

                # Get the stock data
                stock_close = pd.DataFrame()
                db_dic={}

                # db_list=[]
                for i,company in enumerate(companies):
                    try :

                        db_l1={ company:{"Qty": str(edited_df["Qty"][i]), "Start_date": str(edited_df["Start_date"][i]), "End_date": str(edited_df["End_date"][i])}}
                        db_dic.update(db_l1)
                        # db_list.append(db_l1)
                        stock_close[company] = down(company, start=edited_df["Start_date"][i], end=edited_df["End_date"][i])["Close"]
                        stock_close[company] = stock_close[company] * edited_df["Qty"][i]
                        stock_close.rename(columns={company:select_company[i]},inplace=True)
                    except:
                        st.warning(f"can't able to fetch the data of  {company} , Please select other.")
                
                #Adding Data of list companies and qty,startdate,enddate into database
                # if Udata
                db.Update_db_list(un,db_dic)

                    # stock_open["open"] = yf.download(company, start="2023-01-01", end="2023-08-12")["Open"]
                stock_close["Portfolio"]= stock_close.sum(axis=1)



                stock_close.reset_index(inplace=True)
                #coverting time zone to date :
                # stock_close['Year'] = stock_close['Date'].apply(lambda x:str(x)[-4:])
                # stock_close['Month'] = stock_close['Date'].apply(lambda x:str(x)[-6:-4:])
                # stock_close['Day'] = stock_close['Date'].apply(lambda x:str(x)[-6:])
                # stock_close['date'] = pd.DataFrame(stock_close['Year'] +'-' +stock_close['Month'] +'-' + stock_close['Day'])

                # if stock_close not in st.session_state  or st.session_state["stock close"] != stock_close:
                st.session_state["stock close"]= stock_close


                # # Combine all the companies into one line
                # combined_data = stock_data.sum(axis=1)
                # # st.write(combined_data)
                # stock_close["Nifty 50"] = nifty_50_data
                # stock_data["combined_data"] = combined_data
                # st.write(stock_close)
                plot_portfolio_data(stock_close)

            


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
                                db.insert_user(user,Fullname,email,password,db_list={})
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

def Login():

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
                    st.experimental_user()  # Trigger rerun by updating query params
                else:
                    st.error("Incorrect Password")
                
            else:
                st.error("Invalid Username")



if 'status' not in st.session_state:
    st.session_state.status=status


if st.session_state.status==False or st.session_state.status==None:
    col1,col2,col3=st.columns([1.3,2,3/2])
    with col2:
        st.title('WELCOME TO STOCK PORTFOLIO APP')

        login,signup=st.tabs(["Login", "SignUp"])

        with login:
            Login()
                        
        with signup:
            SignUp()


elif st.session_state.get('status')==True:
            # st.header(st.session_state.get('un'))
            app(st.session_state.get('un'))
