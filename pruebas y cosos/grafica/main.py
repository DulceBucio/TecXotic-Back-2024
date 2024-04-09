from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    if file.filename == '':
        return 'No file selected D:'
    
    if file and file.filename.endswith('.csv'):
        
        
        df = pd.read_csv(file)
        df.set_index('Day', inplace=True)
        df = df.transpose()
        
        receiver1 = df['Receiver 1'].tolist()
        receiver2 = df['Receiver 2'].tolist()
        receiver3 = df['Receiver 3'].tolist()
        
        days = list(range(1, len(receiver1) + 1))
        
        plt.figure(figsize=(10, 6))
        plt.plot(days, receiver1, label='Receiver 1', color='blue')
        plt.plot(days, receiver2, label='Receiver 2', color='green')
        plt.plot(days, receiver3, label='Receiver 3', color='red')
        plt.xlabel('Day')
        plt.ylabel('Value')
        plt.title('Data received over the days')
        plt.legend()
        plt.grid(True)
        
        plt.savefig('temp_plot.png')
        plt.close()
        
        # Retorna la ruta de la imagen
        return send_file('temp_plot.png', mimetype='image/png')

    return 'Format not supported. Please upload a CSV file :('

from flask import send_from_directory

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(app.root_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
