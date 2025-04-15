from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    # File Handling
    file = request.files['file']  # Get the uploaded file
    content = file.read().decode('utf-8')  # Read the file content
    
    # Configuring Parameters
    prog_mc_file = request.form.get('prog_mc_file') == 'true'
    pipelining_enabled = request.form.get('pipelining_enabled') == 'true'
    forwarding_enabled = request.form.get('forwarding_enabled') == 'true'
    print_registers_each_cycle = request.form.get('print_registers_each_cycle') == 'true'
    print_pipeline_registers = request.form.get('print_pipeline_registers') == 'true'
    print_specific_pipeline_registers = request.form.get('print_specific_pipeline_registers') == 'true'
    number = request.form.get('number')
    
    # Do something with the file and the boolean values
    demo = open('demofile.txt','w')
    demo.write(content)  # wrtie the uploaded program content to this file
    demo.close()
    f  = open("input.txt",'w')  # clear the existing input.txt file
    f.close()
    f = open('input.txt','a') # write the parameters to the input.txt file TRUE/FALSE and the pipline register to be printed
    f.write(str(pipelining_enabled)+'\n')
    f.write(str(forwarding_enabled)+'\n')
    f.write(str(print_registers_each_cycle)+'\n')
    f.write(str(print_pipeline_registers)+'\n')
    # f.write(str(print_specific_pipeline_registers[0]) + ' ' + str(print_specific_pipeline_registers[1]) + '\n')
    f.write(str(print_specific_pipeline_registers) + ' ' + str(number) + '\n')

    f.close()
    return jsonify({'message': 'File uploaded successfully'})


@app.route('/runScripts', methods=['POST'])
def run_Scripts():
    # print("HELLO0")
    # data = request.get_json()
    # arg = data.get('arg')
    # print(arg)
    # print("HELLO1")
    first = subprocess.run(['python','./main.py'])
    if first.returncode != 0:
        return jsonify({'error': 'Failed to execute first script'})
    
    # print("HELLO2")
    second = subprocess.run(['python','./jsonify.py'])
    if second.returncode != 0:
        return jsonify({'error' : 'Failed to execute second script'})
    # print("HELLO3")
    return jsonify({'request' : 'Both scripts executed successfully'})

if __name__=='__main__':
   app.run()

# Running the simulation using main.py
# This loads the program from demofile.txt and reads the configuration from input.txt
# Then it runs the simulation and outputs the results to output.txt
# Gnerate the output files cycle.txt, data.txt, reg.txt, stats.txt

# Now converting the Joutput to JSON 
# This script read the output files and convert them to JSON format
# Creates files for the frontend
# reg.json, data.json, cycle.json, stats.json
