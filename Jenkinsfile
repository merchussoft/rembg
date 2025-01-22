pipeline {
    agent any
    tools {
        maven 'Maven'
    }
	
	environment {
        SONAR_HOST_URL = 'http://192.168.1.50:9000' // Cambia <SONARQUBE_SERVER> por la dirección de tu servidor SonarQube
        SONAR_AUTH_TOKEN = credentials('SONAR_AUTH_TOKEN') // ID del token almacenado en Jenkins Credentials
    }

    stages {
        stage('Git Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/merchussoft/rembg']])
                echo 'Git Checkout Completed'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
					mvn clean verify sonar:sonar \
						-Dsonar.projectKey=ProjectNameSonar \
						-Dsonar.projectName='ProjectNameSonar' \
						-Dsonar.host.url=${SONAR_HOST_URL} \
                         -Dsonar.login=${SONAR_AUTH_TOKEN}
					'''
                    echo 'SonarQube Analysis Completed'
                }
            }
        }
    }
}