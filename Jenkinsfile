pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Dibyendubijali/smart_management_tools.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building...'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}