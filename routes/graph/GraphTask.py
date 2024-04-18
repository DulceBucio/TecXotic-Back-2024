from flask import Flask, request, send_file, Blueprint, current_app
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from flask import send_from_directory
import os

graph_blueprint = Blueprint('graph', __name__)
CORS(graph_blueprint)

@graph_blueprint.route('/upload', methods=['POST'])
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
        
        temp_directory = os.path.join(current_app.root_path, 'tmp')
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)

        plot_path = os.path.join(temp_directory, "temp_plot.png")
        plt.savefig(plot_path)
        plt.close()
        
        return send_file(plot_path, mimetype='image/png')

    return 'Format not supported. Please upload a CSV file :('

@graph_blueprint.route('/image/<filename>')
def get_image(filename):
    temp_directory = os.path.join(current_app.root_path, 'tmp')
    return send_from_directory(temp_directory, filename)

