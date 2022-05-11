import streamlit as st 
import plotly.express as px 
from kedro.framework.project import configure_project, pipelines
from kedro.framework.session import KedroSession
from kedro.framework.session.session import _activate_session
from kedro.framework.startup import bootstrap_project
from pathlib import Path
import yaml 

st.set_page_config(layout="wide")

# get data from kedro 
default_project_path = Path.cwd()
metadata = bootstrap_project(default_project_path)
configure_project(metadata.package_name)
session = KedroSession.create(metadata.package_name, default_project_path)
context = session.load_context()
companies_data = context.catalog.load('companies')
reviews_data = context.catalog.load('reviews')
processed_companies_data = context.catalog.load('data_processing.preprocessed_companies')
processed_reviews_data = context.catalog.load('data_processing.preprocessed_reviews')
found_min_fleet = float(companies_data['total_fleet_count'].min())
found_max_fleet = float(companies_data['total_fleet_count'].max())
found_min_review_score = float(reviews_data['review_scores_rating'].min())
found_max_review_score = float(reviews_data['review_scores_rating'].max())
found_min_reviews = float(reviews_data['number_of_reviews'].min())
found_max_reviews = float(reviews_data['number_of_reviews'].max())

st.title('Parameter Editor')



col1, col2 = st.columns([1,1])


min_fleet = col1.slider(
    'min_fleet',
    min_value=found_min_fleet,
    max_value=found_max_fleet)

max_fleet = col1.slider(
    'max_fleet',
    min_value=found_min_fleet,
    max_value=found_max_fleet,
    value=found_max_fleet
    )

min_review_score = col1.slider(
    'min_review_score',
    min_value=found_min_review_score,
    max_value=found_max_review_score,
    )

max_review_score = col1.slider(
    'max_review_score',
    min_value=found_min_review_score,
    max_value=found_max_review_score,
    value=found_max_review_score
    )

min_reviews = col1.slider(
    'min_reviews',
    min_value=found_min_reviews,
    max_value=found_max_reviews)

max_reviews = col1.slider(
    'max_reviews',
    min_value=found_min_reviews,
    max_value=found_max_reviews,
    value=found_max_review_score
    )

with open('./conf/base/parameters/data_processing.yml','w') as f:
    yaml.dump({'data_processing':
    {    
            'min_fleet': min_fleet,
            'max_fleet': max_fleet,
            'min_review_score': min_review_score,
            'max_review_score': max_review_score,
            'min_reviews': min_reviews,
            'max_reviews': max_reviews,

    }},f)

st.button('Kedro Run', on_click=session.run)



col2.write(processed_companies_data)
col2.write(processed_reviews_data)




