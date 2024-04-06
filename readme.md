# Knowledge Navigator

Knowledge Navigator is a Streamlit-based application designed to streamline the process of selecting, organizing, and encoding data from various sources, including websites, files, and GitHub repositories. The application facilitates model selection, data encoding, and integration with LangChain for enhanced question-answering capabilities.

## Features

- Data collection from multiple sources
- Data cleaning and organization
- Selection and configuration of embedding and language models
- Data encoding and storage in a vector database
- Integration with LangChain for question-answering
- State management for session continuity and data recovery

## File organization

```
streamlit_app/
│
├── .streamlit/                 # Streamlit configuration
│
├── pages/                      # Directory for pages
│   ├── 01_data_collection.py   # Data collection page
│   ├── 02_data_organization.py # Data organization page
│   ├── 03_model_selection.py   # Model selection page
│   ├── 04_encoding_storage.py  # Encoding and storage page
│   └── 05_testing_qa.py        # Testing and QA page
│
├── utils/                      # Utility functions and classes
│   ├── data_processing.py      # Data processing utilities
│   ├── model_utils.py          # Model-related utilities
│   └── storage_utils.py        # Storage and backup utilities
│
└── app.py                      # Main application entry point
```

## Installation

To set up Knowledge Navigator, ensure you have Python 3.6+ and pip installed on your system. Follow these steps:

```
git clone https://yourrepository.com/knowledge_navigator.git
cd knowledge_navigator
pip install -r requirements.txt
```

## Usage

To run the application:

```
streamlit run app.py
```

Navigate through the app using the sidebar to access different functionalities, from data collection to question-answering.

## Contributing

Contributions to Knowledge Navigator are welcome! Whether it's feature suggestions, bug reports, or code contributions, please feel free to reach out or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

ricklon@fubarlabs.org

Project Link: https://github.com/ricklon/knowledge_navigator
