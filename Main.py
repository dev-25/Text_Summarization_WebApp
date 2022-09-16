
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest

import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
# punctuation = punctuation + '\n


def data(value):
    text = value
    doc = nlp(text)
    tokens = [token.text for token in doc]

    punctuation = punctuation + '\n'
    
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    sentence_tokens = [sent for sent in doc.sents]
    
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency



    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens)*0.3)

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

    final_summary = [word.text for word in summary]

    summary = ' '.join(final_summary)

    return summary



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY]) # SLATE  DARKLY
# app = dash.Dash(__name__)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Long Paragraph to Short Summarization !!",
                         style={'fontSize':40, 
                                'textAlign':'center',"margin-top": "15px","color": "white"
                                # 'text': '#7FDBFF'
                                }))
    ]),

    # html.Hr(style={"margin-left": "20px","margin-right": "20px"}),
    
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div("Enter Text here:",
                    style={ 'fontSize':25, 
                            'textAlign':'left',
                            "margin-top": "45px",
                            "margin-bottom": "15px",
                            "margin-left": "27px","color": "white"

                            }),
                    dbc.Textarea(id='input',className="mb-3", size="lg",style={'fontSize':17,"margin-left": "27px","height": "470px","borderRadius": "10px", 'background-color':'#00415A',"color": "white"},placeholder="Text..."),
                    
                    dbc.Button('Submit', id='button1', n_clicks=0,style={"margin-left": "27px",'background-color':'#303841',"borderRadius": "5px"}),
            
                ], xs=6, sm=6, md=6, lg=6, xl=6, xxl=6,),

            dbc.Col(
                [

                    html.Div("Short Summarization: ",
                    style={ 'fontSize':25, 
                            'textAlign':'left',
                            "margin-top": "45px",
                            "margin-bottom": "15px",
                            "margin-left": "40px","color": "white"

                            }),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("", className="card-title"),
                                html.Div(id="output",style={'fontSize':17}), 
                           
                            ]
                        ),
                        style={"margin-left": "40px","borderRadius": "10px","backgroundColor": "#00415A"},
                    )
                ], xs=6, sm=6, md=5, lg=5, xl=5, xxl=5),
    ])
], fluid=True,style={'backgroundColor':'#001F2B'})




@app.callback(Output('output', 'children'),
    Input('button1', 'n_clicks'),
    State('input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        
        aa = data(value)
        
        return aa


if __name__ == "__main__":
    # app.run_server(debug=True, port=8888)
    app.run_server(debug=True)