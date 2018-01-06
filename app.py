from flask import Flask,render_template,abort
import os
import json

app=Flask(__name__)

class Files(object):
    def __init__(self):
        self.result=self._read_files()
    def _read_files(self):
        result={}
        for filename in os.listdir('/home/shiyanlou/files'):
            file_path=os.path.join('/home/shiyanlou/files',filename)
            with open(file_path) as f:
                result[filename[:-5]]=json.load(f)
        return result
    def get_title_list(self):
        return [item['title'] for item in self.result.values()]
    def get_by_filename(self,filename):
        return self.result.get(filename)

files=Files()




@app.route('/')
def index():
    title_list=files.get_title_list()
    return render_template('index.html',title_list=title_list)

@app.route('/files/<filename>')
def file(filename):
    fileobj=files.get_by_filename(filename)
    if not fileobj:
        abort(404)
    return render_template('file.html',file_item=fileobj)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


if __name__=='__main__':
    app.run()

