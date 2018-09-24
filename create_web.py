from flask import Flask, render_template

# __name__ variable takes the value "__main__" when the script is executed
# It would take the value "__scrip1" if the script was imported
web_app=Flask(__name__) 


# python decorator. The output of the "home" function is mapped to the target of web_app.route
@web_app.route('/')
def home():
    return render_template("home.html")
# render_template will display the content of an HTML file. The file MUST be located in a 
# sub-folder named "templates"


@web_app.route('/about/')
def about():
    return render_template("about.html")


if __name__=="__main__":
    web_app.run(debug=True)

