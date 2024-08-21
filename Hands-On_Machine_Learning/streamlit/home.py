import pandas as pd
import numpy as np
import sklearn.linear_model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import altair as alt
import streamlit as st
import config as cfg


st.markdown(
    """<style>.block-container{max-width: 86rem !important;}</style>""",
    unsafe_allow_html=True,
)

def run_interface():

    # Título do painel
    st.markdown("## Hands-On Machine Learning")
    st.write("---")
    st.markdown('### Example 1-1')
    st.markdown('Training and running a linear model using Scikit-Learn')

    filepath_oecd = 'data/oecd_bli.csv'
    filepath_gdp = 'data/gdp_per_capita.csv'

    df_oecd_bli = pd.read_csv(filepath_oecd, thousands=',')
    df_gdp = pd.read_csv(filepath_gdp)

    df_oecd_bli.rename(columns={'LOCATION': 'Code'}, inplace=True)
    df_gdp.rename(columns={'GDP per capita, PPP (constant 2017 international $)': 'gdp'}, inplace=True)

    columns_indicators = st.columns([6,2,2,2,2,2])

    selected_indicator = columns_indicators[0].selectbox('Indicator', df_oecd_bli['Indicator'].unique())
    df_gdp.sort_values(by=['Year'],inplace=True, ascending=False)
    selected_year = columns_indicators[1].selectbox('Year', df_gdp['Year'].unique())

    df_oecd = df_oecd_bli[['Code', 'Indicator', 'Unit', 'Inequality', 'Value']].query(f'Indicator == "{selected_indicator}"')
    df_oecd.reset_index(drop=True, inplace=True)

    ind_unit = df_oecd['Unit'].unique()[0]

    # ---- inequality indicator ----------------------
    ind_inequality = list(df_oecd['Inequality'].unique())

    if 'Men' in ind_inequality:
        ind_inequality.pop(ind_inequality.index('Men'))
        ind_inequality.pop(ind_inequality.index('Women'))
        ind_inequality.append('Gender')

    if 'Low' in ind_inequality:
        ind_inequality.pop(ind_inequality.index('Low'))
        ind_inequality.pop(ind_inequality.index('High'))
        ind_inequality.append('Income')

    selected_inequality = columns_indicators[2].selectbox('Type', ind_inequality)


    if selected_inequality == 'Gender':
        df_oecd = df_oecd.query('Inequality == "Men" or Inequality == "Women"')
    elif selected_inequality == 'Income':
        df_oecd = df_oecd.query('Inequality == "High" or Inequality == "Low"')
    else:
        df_oecd = df_oecd.query(f'Inequality == "{selected_inequality}"')

    df_gdp = df_gdp.query(f'Year == {selected_year}')

    list_df_gdp = []
    for i in df_oecd['Inequality'].unique():

        df_gdp_temp = df_gdp.copy()
        df_gdp_temp['Type'] = i

        indicator_dict = df_oecd.query(f'Inequality=="{i}"').set_index('Code')['Value'].to_dict()

        df_gdp_temp['Value'] = df_gdp_temp['Code'].map(indicator_dict)
        list_df_gdp.append(df_gdp_temp)

    df_gdp = pd.concat(list_df_gdp)

    df_gdp['gdp'] = df_gdp['gdp'] / 1000

    # select_gdp_lower_cut = float(columns_indicators[4].text_input('GDP Threshold', '10'))
    # select_gdp_upper_cut = float(columns_indicators[5].text_input('', '30'))

    # df_gdp = df_gdp.query(f'gdp <= {select_gdp_upper_cut} and gdp >= {select_gdp_lower_cut}')

    df_none = df_gdp[df_gdp['Value'].isnull()]
    df_none.sort_values(by='Entity', inplace=True)
    df_gdp = df_gdp[df_gdp['Value'].notnull()]
    df_gdp.sort_values(by=['Entity'],inplace=True)
    df_gdp.reset_index(drop=True, inplace=True)
    # df_gdp = df_gdp.sample(frac=1, replace=False)

    container_chart = st.container(border=True)
    columns_container = container_chart.columns([5,1,2,2,2])

    predict_entity = selected_none = columns_container[3].selectbox('Predict', df_none['Entity'].unique())

    df_topredict = df_none.query(f'Entity == "{predict_entity}"')

    list_df_gdp = []
    list_predict = []
    list_b_0 = []
    list_b_1 = []

    for i in df_gdp['Type'].unique():

        df_gdp_temp = df_gdp.copy()
        df_topredict_temp = df_topredict.copy()

        df_gdp_temp = df_gdp_temp.query(f'Type == "{i}"')
        df_topredict_temp = df_topredict_temp.query(f'Type == "{i}"')

        X = np.c_[df_gdp_temp['gdp']]
        y = np.c_[df_gdp_temp['Value']]

        model = sklearn.linear_model.LinearRegression()
        model.fit(X,y)

        columns_container[2].metric(label=f'Coefficient 1 ({i})', value=round(float(model.coef_[0]), 2))

        fitted_values = model.predict(X)

        model_r2_score = r2_score(y, fitted_values)

        columns_container[2].metric(label='$R^2$', value=round(float(model_r2_score), 2))
        columns_container[2].metric(label='Correlation', value=round(float(np.sqrt(model_r2_score)), 2))

        df_gdp_temp['Fitted'] = fitted_values
        df_topredict_temp['Fitted'] = model.predict(np.c_[df_topredict_temp['gdp']])

        list_df_gdp.append(df_gdp_temp)
        list_predict.append(df_topredict_temp)

    df_gdp = pd.concat(list_df_gdp)
    df_topredict = pd.concat(list_predict)
        
    chart_gdp = alt.Chart(df_gdp).mark_circle(size=70, color='red').encode(
            alt.X(
                'gdp:Q',
                axis=alt.Axis(title='GDP (in US$ 1,000)'),
                ),
            alt.Y(
                'Value:Q',
                axis=alt.Axis(title=selected_indicator + ' ( ' +ind_unit + ' )'),
                scale=alt.Scale(
                    domain=[
                        min(df_gdp['Value'].min(),df_gdp['Fitted'].min()) * 0.9,
                        max(df_gdp['Value'].max(), df_gdp['Fitted'].max()) * 1.1
                        ]
                    )
                ),
            color=alt.Color('Type').scale(scheme='set1')
            ).properties(height=400, width=600)

    chart_gdp_line = alt.Chart(df_gdp).mark_line(opacity=0.5).encode(
            alt.X('gdp:Q'),
            alt.Y(
                'Fitted:Q',
                ),
            color=alt.Color('Type')
            )


    chart_predicted = alt.Chart(df_topredict).mark_point(size=150).encode(
            alt.X('gdp:Q'),
            alt.Y(
                'Fitted:Q'
                ),
            color=alt.Color('Type').scale(scheme='set3')
            )

    columns_container[0].altair_chart(chart_gdp + chart_gdp_line + chart_predicted, use_container_width=False)



    st.write("---")
def main():
    run_interface()

if __name__ == "__main__":
    main()


