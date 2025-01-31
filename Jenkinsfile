pipeline {
    agent any
	
	environment {
        SCANNER_HOME = tool 'sonarqube'
    }

    stages {

        stage('notificacion slack') {
            steps {
                slackSend color: 'good', message: 'Se ha iniciado el pipeline de rembg'
            }
        }

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
        always {
            script {
                def color = (currentBuild.result == 'SUCCESS') ? 'good' : 'danger'
                def status = (currentBuild.result == 'SUCCESS') ? '✅ ÉXITO' : '❌ FALLÓ'
                def summary = """*${status}*
                    *Job:* ${env.JOB_NAME}
                    *Build Number:* ${env.BUILD_NUMBER}
                    *Branch:* ${env.BRANCH_NAME}
                    *Commit:* ${env.GIT_COMMIT}
                    *Ejecutado por:* ${env.USER}
                    *Ver detalles:* <${env.BUILD_URL}|Click aqui>
                """

                slackSend(color: color, message: summary)
            }
        }
    }
}