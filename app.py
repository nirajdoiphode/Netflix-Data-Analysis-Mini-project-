from flask import Flask, jsonify
import pandas as pd
import plotly.express as px
from textblob import TextBlob

app = Flask(__name__)

# Load dataset (ensure correct path)
# dff = pd.read_csv('C:\\Users\\niraj\\OneDrive\\Desktop\\netflix_titles_cleaned.csv')3
dff = pd.read_csv('C:\\Users\\niraj\\PycharmProjects\\NetfilxDataAnalysis\\\DataSets\\netflix_titles_cleaned.csv')


def showdist():
    """Function to generate and display the pie chart"""
    z = dff.groupby(['rating']).size().reset_index(name='counts')
    pieChart = px.pie(z, values='counts', names='rating',
                      title='Distribution of Content Ratings on Netflix',
                      color_discrete_sequence=px.colors.qualitative.Set3)
    pieChart.show()


def showtopDirectors():
    dff['director'] = dff['director'].fillna('No Director Specified')
    filtered_directors = pd.DataFrame()
    filtered_directors = dff['director'].str.split(',', expand=True).stack()
    filtered_directors = filtered_directors.to_frame()
    filtered_directors.columns = ['Director']
    directors = filtered_directors.groupby(['Director']).size().reset_index(name='Total Content')
    directors = directors[directors.Director != 'No Director Specified']
    directors = directors.sort_values(by=['Total Content'], ascending=False)
    directorsTop5 = directors.head()
    directorsTop5 = directorsTop5.sort_values(by=['Total Content'])
    fig1 = px.bar(directorsTop5, x='Total Content', y='Director', title='Top 5 Directors on Netflix')
    fig1.show()

def showtopActors():
    dff['cast'] = dff['cast'].fillna('No Cast Specified')
    filtered_cast = pd.DataFrame()
    filtered_cast = dff['cast'].str.split(',', expand=True).stack()
    filtered_cast = filtered_cast.to_frame()
    filtered_cast.columns = ['Actor']
    actors = filtered_cast.groupby(['Actor']).size().reset_index(name='Total Content')
    actors = actors[actors.Actor != 'No Cast Specified']
    actors = actors.sort_values(by=['Total Content'], ascending=False)
    actorsTop5 = actors.head()
    actorsTop5 = actorsTop5.sort_values(by=['Total Content'])
    fig2 = px.bar(actorsTop5, x='Total Content', y='Actor', title='Top 5 Actors on Netflix')
    fig2.show()

def showtrendingcontent():
    df1 = dff[['type', 'release_year']]
    df1 = df1.rename(columns={"release_year": "Release Year"})
    df2 = df1.groupby(['Release Year', 'type']).size().reset_index(name='Total Content')
    df2 = df2[df2['Release Year'] >= 2010]
    fig3 = px.line(df2, x="Release Year", y="Total Content", color='type',
                   title='Trend of content produced over the years on Netflix')
    fig3.show()


def showsentimentcontent():
    dfx = dff[['release_year', 'description']]
    dfx = dfx.rename(columns={'release_year': 'Release Year'})
    for index, row in dfx.iterrows():
        z = row['description']
        testimonial = TextBlob(z)
        p = testimonial.sentiment.polarity
        if p == 0:
            sent = 'Neutral'
        elif p > 0:
            sent = 'Positive'
        else:
            sent = 'Negative'
        dfx.loc[[index, 2], 'Sentiment'] = sent

    dfx = dfx.groupby(['Release Year', 'Sentiment']).size().reset_index(name='Total Content')

    dfx = dfx[dfx['Release Year'] >= 2010]
    fig4 = px.bar(dfx, x="Release Year", y="Total Content", color="Sentiment", title="Sentiment of content on Netflix")
    fig4.show()



@app.route('/')
def index():
    """Serve the HTML page"""
    return open("templates/index.html").read()


@app.route('/show_chart', methods=['GET'])
def show_chart():
    """Call the function to generate the chart when the button is clicked"""
    showdist()
    return jsonify({"message": "Chart displayed successfully!"})


@app.route('/show_directors', methods=['GET'])
def show_directors():
    showtopDirectors()
    return jsonify({"message": "Chart displayed successfully!"})

@app.route('/show_actors', methods=['GET'])
def show_actors():
    showtopActors()
    return jsonify({"message": "Chart displayed successfully!"})

@app.route('/show_trendcontent', methods=['GET'])
def show_tendcontent():
    showtrendingcontent()
    return jsonify({"message": "Chart displayed successfully!"})

@app.route('/show_scontent', methods=['GET'])
def show_scontent():
    showsentimentcontent()
    return jsonify({"message": "Chart displayed successfully!"})




if __name__ == '__main__':
    app.run(debug=True)
