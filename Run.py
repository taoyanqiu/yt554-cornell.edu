#export FLASK_APP=yourapp
if __name__ == '__main__':
  #app.run_server(debug=True)
  #app.run('localhost', 5000)
  #export FLASK_ENV=development
  #flask run
  app.run_server(debug=True, use_reloader=False)