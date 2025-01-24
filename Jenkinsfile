pipeline {
    agent any
	
	environment {
        SCANNER_HOME = tool 'sonarqube'
    }

    stages {

        stage('Git Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg.git'
                echo 'Git Checkout Completed'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: 'sonarqube', installationName: 'sonarqube') {
                    sh '''
					$SCANNER_HOME/bin/sonar-scanner \
						-Dsonar.projectKey=rembg \
						-Dsonar.projectName=rembg \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=/var/jenkins_home/workspace/rembg \
                        -Dsonar.sourceEncoding=UTF-8
					'''
                    echo 'SonarQube Analysis Completed'
                }
            }
        }

        stage('stop and down and eraser volumes Docker Compose') {
            steps {

                    sh '''
                        echo "tumbando los contenedores anteriores"
                        docker compose down -v
                    '''

            }
        }

        stage('deploy with Docker Compose') {
            steps {
                script {
                    sh '''
                        echo "desplegando la aplicaion con docker"
                        docker compose up --build -d
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