pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://192.168.1.50:9000' // URL de SonarQube
        SONAR_AUTH_TOKEN = credentials('squ_2e83746e904ad61771f54c3f27561b12f3c232cb') // Token almacenado en Jenkins
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') { // 'SonarQubeServer' debe ser el nombre configurado en Jenkins para SonarQube
                    sh '''
                    sonar-scanner \
                        -Dsonar.projectKey=rembg \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}