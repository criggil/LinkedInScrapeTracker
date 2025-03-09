from flask import Flask, render_template, request, redirect, url_for
from modules.config_manager import ConfigManager
from modules.storage import Storage
from modules.post_filter import PostFilter

app = Flask(__name__)
config_manager = ConfigManager()
storage = Storage()
post_filter = PostFilter()

@app.route('/')
def index():
    searches = config_manager.get_all_searches()
    return render_template('index.html', searches=searches)

@app.route('/add_search', methods=['GET', 'POST'])
def add_search():
    if request.method == 'POST':
        name = request.form['name']
        search_type = request.form['type']
        notify = 'notify' in request.form
        
        criteria = {'type': search_type}
        if search_type == 'user':
            criteria['usernames'] = request.form['usernames'].split(',')
        else:
            criteria['keywords'] = request.form['keywords'].split(',')
        
        config_manager.add_search(name, criteria, notify)
        return redirect(url_for('index'))
    
    return render_template('add_search.html')

@app.route('/view_matches/<search_id>')
def view_matches(search_id):
    search = config_manager.get_search(search_id)
    matches = storage.get_matches(search_id)
    return render_template('view_matches.html', search=search, matches=matches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
