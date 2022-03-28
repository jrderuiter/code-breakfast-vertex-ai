# Code Breakfast - Vertex AI + Kubeflow Pipelines

In this code breakfast, we'll introduce you to the basic components of Vertex AI and show you how to run (custom) training jobs on Vertex AI using the Kubeflow Pipeline SDK.


## Getting started

For this code breakfast, we'll use a cloud-based JupyterLab environment for developing and running code on Vertex AI. This JupyterLab environment runs on your own personal VM in Vertex Workbench. To find your VM and open JupyterLab, follow these steps:

1. Open the Google Cloud Console (http://console.cloud.google.com) in your browser.
2. In the console, select the project `gdd-cb-vertex`.
3. Next, navigate to the Vertex Workbench section in the console (under `Vertex AI > Workbench`).
4. In the Workbench section, find the VM with your name (e.g. `vwb-<your-user-name`).
5. Open JupyterLab by clicking on the `Open JupyterLab` button next to your VM name.

This should open a new tab in your browser with JupyterLab. To set up the code for the code breakfast, open a terminal in JupyterLab (under `File > New > Terminal`) and do the following:

1. Clone this repository using: `git clone https://github.com/godatadriven/code-breakfast-vertex-ai.git`.
2. Switch to the directory we just cloned: `cd code-breakfast-vertex-ai`.
3. Set up the projects Python environment using: `make python-init`

## Exercises

### Exercise 1 - Run the model locally

Open the notebook `notebooks/1-run-local.ipynb` and run through the exercises in the notebook.

### Exercise 2 - Run the model in Vertex Pipelines


Open the notebook `notebooks/2-run-pipeline.ipynb` and run through the exercises in the notebook.

## Deployment

The infrastructure for this code breakfast can be deployed from the corresponding Terraform repository.

## Contributing

If you'd like to contribute to the code breakfast, feel free to fork this repo and submit a PR with your changes! For an overview of open points that need to be picked up, check out our project board: https://github.com/godatadriven/code-breakfast-vertex-ai/projects/1
