pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\lokit_04l4u3w\\AppData\\Local\\Programs\\Python\\Python39\\python.exe"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Clone Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Lokithneo/ai-productivity-dashboard.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "%PYTHON% -m pip install -r requirements.txt"
            }
        }

        stage('Build Check') {
            steps {
                bat "%PYTHON% -m py_compile run.py"
            }
        }
    }
}