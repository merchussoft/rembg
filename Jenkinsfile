pipeline {
    agent any

    environment {
        IMAGENAME = "rembg:latest"
        CONTAINER_NAME  = "rembg"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script{
                    sh '''
                        echo "Building Docker image..."
                        docker build -t $IMAGENAME .
                    '''
                }
                
            }
        }

        stage('Deploy Docker Container') {
            steps {
                scripts {
                    sh '''
                        echo "Stopping and removing old container (if exists)..."
                        docker-compose down
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true

                        echo "Starting new container with Docker Compose..."
                        docker-compose up --build -d
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! The application has been deployed."
        }
        failure {
            echo "Pipeline failed! The application has not been deployed."
        }
    }
}