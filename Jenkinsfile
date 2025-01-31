pipeline {
    agent any
	
	environment {
        SCANNER_HOME = tool 'sonarqube'
        SONAR_URL = "http://192.168.1.50:9000"  // Reemplázalo con tu URL
    }

    stages {

        stage('notificacion slack') {
            steps {
                slackSend(color: 'good', message: '🚀 *Pipeline Iniciado* - Se ha iniciado la ejecución del pipeline para *rembg*')
            }
        }

        stage('Git Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/merchussoft/rembg.git'
                echo '✅ Git Checkout Completado'
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
                        -Dsonar.exclusions="**/Dockerfile"
					'''
                    echo '✅ Análisis SonarQube Completado'
                }
            }
        }

        stage("Esperar Quality Gate SonarQube") {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qualityGate = waitForQualityGate()
                        def status = qualityGate.status
                        def color = (status == 'OK') ? 'good' : 'danger'
                        def resultText = (status == 'OK') ? '✅ *PASÓ*' : '❌ *FALLÓ*'

                        def sumary = """🔍 *SonarQube Reporte*
                            📌 *Estado:* ${resultText}
                            🚦 *Quality Gate:* ${status}
                            🔗 *Ver detalles:* <${SONAR_URL}/dashboard?id=${env.JOB_NAME}|Click aqui>
                        """

                        slackSend(color: color, message: sumary)

                        if (status != 'OK') {
                            error "⛔ Quality Gate falló en SonarQube"
                        }
                    }
                }
            }
        }

        stage('stop and down and eraser volumes Docker Compose') {
            steps {

                sh '''
                    echo "Deteniendo y eliminando contenedores anteriores..."
                    docker compose down -v
                '''

            }
        }

        stage('deploy with Docker Compose') {
            steps {
                script {
                    sh '''
                        echo "Desplegando la aplicación con Docker..."
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
                    📌 *Job:* ${env.JOB_NAME}
                    🔢 *Build Number:* ${env.BUILD_NUMBER}
                    🌿 *Branch:* ${env.GIT_BRANCH}
                    🔗 *Commit:* ${env.GIT_COMMIT}
                    👤 *Ejecutado por:* ${env.BUILD_USER}
                    🔗 *Ver detalles:* <${env.BUILD_URL}|Click aqui>
                """

                slackSend(color: color, message: summary)
            }
        }
    }
}