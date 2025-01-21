pipeline {
    agent any

    environment {
        IMAGENAME = "rembg:latest"
        CONTAINER_NAME  = "rembg"
    }

    stages {
        stage('Deploy Docker Container') {
            steps {
                scripts {
                    sh '''
                        echo "Stopping and removing old container (if exists)..."
                        docker-compose down | true

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