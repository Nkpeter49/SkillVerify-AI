from flask import Flask, render_template, request
from llm_service import generate_tailored_match
from verifier import verify_llm_output

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    master_resume = request.form.get('master_resume', '').strip()
    job_description = request.form.get('job_description', '').strip()

    if not master_resume or not job_description:
        return render_template('index.html', error='Please provide both resume and job description.')

    llm_data = generate_tailored_match(master_resume, job_description)

    if 'error' in llm_data:
        return render_template('index.html', error=llm_data['error'])

    audit_result = verify_llm_output(master_resume, llm_data)
    return render_template('result.html', result=audit_result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
