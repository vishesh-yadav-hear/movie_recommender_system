from flask import Flask, request, render_template_string
import pandas as pd
import pickle
import requests
import io

new_df = pickle.load(open('movies_df.pkl', 'rb'))
new_df = pd.DataFrame(new_df)
similerity = pickle.load(open('similerity.pkl','rb'))

similarity = pickle.load(io.BytesIO(response.content))
app = Flask(__name__)
def recommender(input_movie):
  movie_index = int(new_df[new_df['title'] == input_movie].index[0])
  distanses = similerity[movie_index]
  data = sorted(list(enumerate(distanses)),reverse=True,key = lambda x:x[1])[1:6]
  final_ans = []
  for i in data:
    final_ans.append(new_df.iloc[i[0]].title)
    print()
  return final_ans

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    if request.method == 'POST':
        input_movie = request.form.get('movie')
        output = recommender(input_movie)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Movie Recommender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                }
                input, button {
                    padding: 10px;
                    font-size: 16px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                #output {
                    margin-top: 20px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    min-height: 50px;
                }
            </style>
        </head>
        <body>
            <h1>Movie Recommender</h1>
            <form method="POST">
                <input type="text" name="movie" placeholder="Enter movie name" required>
                <button type="submit">Recommend</button>
            </form>
          {% if output %}
          <div id="output">{% for i in output %}{{ i }}<br>{% endfor %}</div>
          {% endif %}

        </body>
        </html>
    ''', output=output)




if __name__ == '__main__':
    app.run(debug=False)
