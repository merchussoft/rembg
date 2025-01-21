pipeline {
    agent any

    environment {
        IMAGENAME = "rembg:latest"
        CONTAINER_NAME  = "rembg"
    }

    stages {
        stage('Chackout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg.git'
            }
        }
    }
}