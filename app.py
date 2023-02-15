import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from startupsinfo import StartupInfo
plt.style.use('ggplot')

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startups.csv', parse_dates=['date'], dayfirst=True)
dataset = pd.read_csv('newdf.csv',parse_dates=['date'], dayfirst=True)
df['location']=df['location'].replace('Delhi','New Delhi')  # came to know at last moment that this thing left out while cleaning
df['startup']=df['startup'].replace('Flipkart.com','Flipkart') #last moment changes
startup_info = StartupInfo(df)

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['Dates'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3 = px.bar(temp_df, y=temp_df['amount'], x=temp_df['Dates'], text=temp_df['amount'])
    fig3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig3.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    #fig3.show()
    st.plotly_chart(fig3,theme=None, use_container_width=True)

    col5,col6 = st.columns(2)
    with col5:
        top_sectors = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Top_Sectors')
        fig6, ax6 = plt.subplots()
        ax6.bar(top_sectors.index, top_sectors.values)
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig6)
    with col6:
        count_sectors=df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
        st.subheader('Counts')
        fig7, ax7 = plt.subplots()
        ax7.bar(count_sectors.index, count_sectors.values)
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig7)

    top_5_values = df['investment_type'].value_counts().nlargest(5).index.tolist()
    result1 = df[df['investment_type'].isin(top_5_values)].groupby('investment_type').agg({'amount': 'sum', 'investment_type': 'size'})
    result1.columns = ['sum', 'count']
    result1 = result1.sort_values(by='count', ascending=False)
    result1.reset_index(inplace=True)
    st.subheader('Usual Fundings')
    fig8 = px.pie(result1, values='count', names='investment_type', hover_data=['sum'], labels={'sum': 'amount'},
                  hole=0.4, color_discrete_sequence=px.colors.qualitative.Dark2)
    fig8.update_traces(textposition='inside', textinfo='percent+label')
    # fig8.show()
    st.plotly_chart(fig8)

    top_10_values = df['location'].value_counts().nlargest(10).index.tolist()
    result2 = df[df['location'].isin(top_10_values)].groupby('location').agg({'amount': 'sum', 'location': 'size'})
    result2.columns = ['sum', 'count']
    result2 = result2.sort_values(by='count', ascending=False)
    result2.reset_index(inplace=True)
    st.subheader('City Wise')
    fig9 = px.bar(result2, x='location', y='count',
                  hover_data=['sum'], color='sum',
                  labels={'sum': 'amount'}, height=400)
    #fig9.show()
    st.plotly_chart(fig9)

    overall_startups = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
    top_startup_per_year = (df.groupby(['year'])
                            .apply(lambda x: x.nlargest(2, 'amount'))
                            .reset_index(drop=True))

    st.subheader('YOY Top Funded Startups')
    fig10 = px.bar(top_startup_per_year, x='year', y='amount',
                   hover_data=['startup','investor','location'], color='startup', height=400)
    #fig10.show()
    st.plotly_chart(fig10)

    col7, col8 = st.columns(2)

    with col7:
        st.subheader('Overall Top Funded Startups')
        fig11, ax11 = plt.subplots()
        ax11.bar(overall_startups.index, overall_startups.values)
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig11)

    with col8:
        df1 = dataset.groupby('investor').agg({'amount': 'sum'}).nlargest(10, 'amount')
        df1.reset_index(inplace=True)
        st.subheader('Top Investors Over the years')
        fig12, ax12 = plt.subplots()
        ax12.bar(df1['investor'], df1['amount'])
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig12)


def load_startup_details(startups):
    st.title(startups)
    st.write('*(Note: O means Not Mentioned/Undisclosed)*')

    st.subheader('Founder (URL)')
    founder = startup_info.get_founder(startups)
    st.write(founder)

    st.subheader('Vertical/Industry')
    vertical = startup_info.get_vertical(startups)
    st.write(vertical)

    st.subheader('SubVertical/SubIndustry')
    subvertical = startup_info.get_subvertical(startups)
    st.write(subvertical)

    st.subheader('Location/HQ')
    location = startup_info.get_location(startups)
    st.write(location)

    st.subheader(f'Funding details for {startups}')
    fig13 = startup_info.plot_startup_funding(startups)
    st.plotly_chart(fig13)

    st.subheader('Similar Startups')
    similar_startups = startup_info.find_similar_startups(startups, num_similar=6)
    st.write(similar_startups)



def load_investor_details(investors):
    st.title(investors)
    col1, col2 = st.columns(2)
    with col1:
        # load the recent 5 investments of the investor
        last5_df = df[df['investor'].str.contains(investors)].tail()[['date', 'startup', 'vertical', 'location', 'investment_type', 'amount']]
        st.subheader('Most Recent Investments')
        st.dataframe(last5_df)

    with col2:
        st.subheader('Similar Investors')
        from bagofwords import similar_investor
        similar_investors = similar_investor(investors)
        for investorss in similar_investors:
            st.write(investorss)

    col3, col4 = st.columns(2)
    with col3:
        # biggest investments
        big_series = df[df['investor'].str.contains(investors)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col4:
        df['year'] = df['date'].dt.year
        year_series = df[df['investor'].str.contains(investors)].groupby('year')['amount'].sum()

        st.subheader('YoY Investment')
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index, year_series.values)

        st.pyplot(fig2)


    vertical_series = df[df['investor'].str.contains(investors)].groupby('vertical')['amount'].sum()
    st.subheader('Sectors invested in')
    fig1, ax1 = plt.subplots()
    ax1.bar(vertical_series.index, vertical_series.values)
    plt.xticks(rotation='vertical')
    plt.show()
    st.pyplot(fig1)

    col5, col6 = st.columns(2)
    with col5:
        stage_series = df[df['investor'].str.contains(investors)].groupby('investment_type')['amount'].sum()
        st.subheader('Investment Stages')
        fig4 = px.pie(stage_series, values=stage_series.values, names=stage_series.index)
        #fig4.show()
        st.plotly_chart(fig4)
    with col6:
        location_series = df[df['investor'].str.contains(investors)].groupby('location')['amount'].sum()
        st.subheader('Location Preffered')
        fig5 = px.pie(location_series, values=location_series.values, names=location_series.index)
        #fig5.show()
        st.plotly_chart(fig5)

    st.subheader('Investor Portfolio')
    st.write(str(df[df['investor'].str.contains(investors)]['startup'].unique()))





st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)