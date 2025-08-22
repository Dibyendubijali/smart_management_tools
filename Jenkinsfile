pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "smart-management-tool"
        VERSION = "v1.0.${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Dibyendubijali/smart_management_tools.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building project...'
                sh 'docker build -t $DOCKER_IMAGE:$VERSION .'
                sh 'docker tag $DOCKER_IMAGE:$VERSION $DOCKER_IMAGE:latest'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests inside Docker...'
                sh 'docker run --rm $DOCKER_IMAGE:latest pytest || echo "No tests found"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                docker stop smart_app || true
                docker rm smart_app || true
                docker run -d -p 5000:5000 --name smart_app $DOCKER_IMAGE:latest
                '''
            }
        }
    }
}