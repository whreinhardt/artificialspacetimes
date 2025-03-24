This is an example demonstration of the simulation capabilities from the publication "Artificial Spacetimes for Reactive Control of Resource-Limited Robots" (https://arxiv.org/abs/2503.13355). To run this demonstration, the following steps must be completed:
1. Download "sim-mwe.py" and "structpre.mat" to the active path of your Python environment.
2. Install the necessary libraries, denoted by the import statements of sim-mwe.py.
3. Open MATLAB (any release) and install the Schwarz-Christoffel toolbox from Toby Driscoll.
4. Download the helper functions "evalinv_python.m" and "evaldiff_python.m" to the active path of the Python environment.
5. Run the simulation. To test out different geometries, create a new mapping function using the Schwarz-Christoffel toolbox and overwrite the structure in "structpre.mat"
