from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Placeholder for user data and posts
users = {}
activities = []
polls = []
marketplace_items = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process signup form
        users[request.form['username']] = request.form['password']
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form
        if users.get(request.form['username']) == request.form['password']:
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', activities=activities, polls=polls, marketplace_items=marketplace_items)

@app.route('/activities', methods=['GET', 'POST'])
def activities_page():
    if request.method == 'POST':
        # Example of handling a posted activity
        activity_description = request.form['description']
        activities.append({'description': activity_description})
    return render_template('activities.html', activities=activities)

@app.route('/polls', methods=['GET', 'POST'])
def show_polls():
    if request.method == 'POST':
        poll_id = int(request.form['poll_id'])
        selected_option_text = request.form['option']
        # Find and update the selected option's vote count
        for option in polls[poll_id]['options']:
            if option['text'] == selected_option_text:
                option['votes'] += 1
                break
        return redirect(url_for('show_polls'))
    return render_template('polls.html', polls=polls)

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        options_texts = request.form.get('options').split(',')
        options = [{'text': text, 'votes': 0} for text in options_texts]
        polls.append({'question': question, 'options': options})
        return redirect(url_for('show_polls'))
    return render_template('create_poll.html')

@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace_page():
    if request.method == 'POST':
        # Example of handling a posted marketplace item
        item_name = request.form['name']
        item_description = request.form['description']
        item_image_url = request.form.get('image_url') # Optional image URL
        marketplace_items.append({'name': item_name, 'description': item_description, 'image_url': item_image_url})
    return render_template('marketplace.html', marketplace_items=marketplace_items)


if __name__ == '__main__':
    app.run(debug=True)