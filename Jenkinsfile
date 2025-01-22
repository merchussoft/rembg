pipeline {
    agent any

    environment {
        SONAR_HOST_URL = 'http://192.168.1.50:9000' // Cambia <SONARQUBE_SERVER> por la dirección de tu servidor SonarQube
        SONAR_AUTH_TOKEN = credentials('SONAR_AUTH_TOKEN') // ID del token almacenado en Jenkins Credentials
    }

    stages {
        stage('Chechout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg'
            }
        }

        stage('Sonaquebe analysis') {
            steps {
                script {
                    // Ejecutar el analisis del sonarqube
                    sh '''
                    sonar-scanner \
                        -Dsonar.projectKey=rembg \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
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