from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def interview_form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    responses = [int(request.form.get(f'q{i+1}', 0)) for i in range(20)]
    suitability = calculate_suitability_score(responses)
    return render_template('results.html', suitability=suitability)

def calculate_suitability_score(responses):
    max_score = len(responses) * 4
    candidate_score = sum(responses)
    score_percentage = (candidate_score / max_score) * 100

    if score_percentage >= 75:
        return "Highly Suitable"
    elif score_percentage >= 50:
        return "Suitable"
    elif score_percentage >= 25:
        return "Moderately Suitable"
    elif score_percentage > 0:
        return "Slightly Suitable"
    else:
        return "Not Suitable"

if __name__ == '__main__':
    app.run(debug=True)
