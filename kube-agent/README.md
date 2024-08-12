# Kube Agent

### Kube Engineer

- Role: Manages and configures Kubernetes components and resources.
  - Tasks:
    - Manipulates Kubernetes resources (e.g., listing, describing, logging).
    - Extracts abnormal or unusual information based on user input.
    - Provides context for a Kubernetes application, detailing components and their configurations.

### Code Analyzer

- Role: Analyzes code from GitHub repositories.

- Tasks:
  - Fetches code from repositories.
  - Analyzes the logic of the code.
  - Identifies errors/warning messages and provides possible advice and a summary.

### Program Debugger

- Role: Debugs and patches code based on analysis.
- Tasks:
  - Attempts to patch fixes based on findings from the Code Analyzer.
  - Writes validations for the applied patches.

### User Application

- Role: Provides user-facing context for Kubernetes applications.
- Tasks:
  - Explains the system's components.
  - Guides configuration steps for components like CRD, ConfigMap, and Secret.
  - Clarifies the role of each component in the system