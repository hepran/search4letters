"""
Explanation of imported function:
1. render_template function returns a string of HTML when invoked.

2. request function ensures that every time the HTML form is used with different
values for phrase and letters.

3. escape function translates data into its HTML-escaped equivalent.
"""

from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    """
    Store and manipulate the search4letters's data.
    When this function invokes, it displays the formatted out as follows:
        [data from webapp]|[IP address]|[browser ID]|[result]
    and then appends to a log file named vsearch.log.
    """
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    
@app.route('/search4', methods=['POST'])
def do_seacrh() -> 'html':
    """
    Shows the search result page.
    
    "log_request(request, results)" is a function inside a function.
    That line of code arranges to log each web request to a the log file.
    """
    title = 'Here are your results:'
    phrase = request.form['phrase']
    letters = request.form['letters']    
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                            the_title=title,
                            the_phrase=phrase,
                            the_letters=letters,
                            the_results=results, )
    
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Show the homepage or the page to entry what a user wants to search."""
    return render_template('entry.html',
                            the_title='Welcome to search4letters on the web!')
    
@app.route('/viewlog')
def view_the_log()-> str:
    """Show the log."""
    with open('vsearch.log') as log:
        contents = log.readlines()
    return escape(''.join(contents))

if __name__ == '__main__':
    app.run(debug=True)

