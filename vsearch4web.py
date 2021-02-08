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
    When this function invokes, the "req" argument is assigned to the current
    Flask request object, while the "res" argument is assigned the results from
    calling search4letters.
    This function also appends the value of "req" and "res" to a log file named
    "vsearch.log".
    
    "...str(dir(req))..." produces a list of "req", then that list is converted
    to string, and then that string is saved to the log file along with "res"
    value.
    """
    with open('vsearch.log', 'a') as log:
        print(str(dir(req)), res, file=log)
    
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
    """
    Show the homepage or the page to entry what a user wants to search.
    """
    return render_template('entry.html',
                            the_title='Welcome to search4letters on the web!')
    
@app.route('/viewlog')
def view_the_log()-> str:
    """
    Show the log.
    
    See the escape function at the return statement.
    That function makes the "req" argument in log_request() function which
    results HTML behaves like a string, just like the "res" argument.
    By that, it enables web browser to display the result of "req" and "res".
    """
    with open('vsearch.log') as log:
        contents = log.read()
    return escape(contents)

if __name__ == '__main__':
    app.run(debug=True)

