pipeline {
    agent any

    environment {
        IMAGENAME = "rembg:latest"
        CONTAINER_NAME  = "rembg"
    }

    stages {
        stage('limpiar-archivos-yu-directorios-antiguos') {
            steps {
                script{
                    sh '''
                        echo "Encuentra y borra archivos y directorios anteriores a 7 dias en el workspace del jenkins"
                        find $WORKSPACE -type f -mtime +7 -exec rm -f {} +
                        find $WORKSPACE -type f -mtime +7 -exec rm -rf {} +
                    '''
                }
                
            }
        }

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